# # # payments/services.py
# # import logging
# # import requests
# # from django.conf import settings
# # from django.utils import timezone

# # from .models import Transaction
# # from bookings.models import Booking

# # logger = logging.getLogger("payments")


# # # ------------------------------------------
# # # 1. Flutterwave Verification (Server → Server)
# # # ------------------------------------------

# # def verify_flutterwave_transaction(flw_transaction_id):
# #     """
# #     Performs server-to-server verification to Flutterwave.
# #     Called by both: webhook + redirect handlers.
# #     """
# #     url = f"https://api.flutterwave.com/v3/transactions/{flw_transaction_id}/verify"

# #     headers = {
# #         "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
# #         "Content-Type": "application/json",
# #     }

# #     logger.info(f"[VERIFY] Sending S2S verify to Flutterwave for ID={flw_transaction_id}")

# #     try:
# #         response = requests.get(url, headers=headers, timeout=15)
# #         data = response.json()
# #     except Exception as e:
# #         logger.exception(f"[VERIFY] Network error verifying transaction: {e}")
# #         return None

# #     logger.info(f"[VERIFY] Flutterwave response: {data}")

# #     if "status" not in data:
# #         return None

# #     if data.get("status") != "success":
# #         return None

# #     # return verification result payload
# #     return data.get("data")


# # # ------------------------------------------
# # # 2. Payload extractors
# # # ------------------------------------------

# # def extract_webhook_payload(request):
# #     """
# #     Safely extracts JSON fields from Flutterwave webhook.
# #     Returns (tx_ref, flw_transaction_id, flw_ref, full_json).
# #     """
# #     try:
# #         payload = request.data
# #     except Exception:
# #         try:
# #             payload = request.body.decode()
# #         except Exception:
# #             payload = {}

# #     logger.info(f"[WEBHOOK] Raw payload: {payload}")

# #     tx_ref = payload.get("txRef") or payload.get("tx_ref")
# #     flw_id = payload.get("id") or payload.get("transaction_id")
# #     flw_ref = payload.get("flwRef") or payload.get("flw_ref")

# #     return tx_ref, flw_id, flw_ref, payload


# # def extract_redirect_payload(request):
# #     """
# #     Extracts payload from redirect GET/POST.
# #     Returns (status, tx_ref, transaction_id, flw_ref)
# #     """
# #     data = request.GET.dict() if request.method == "GET" else request.POST.dict()

# #     logger.info(f"[REDIRECT] Raw payload: {data}")

# #     return (
# #         data.get("status"),
# #         data.get("tx_ref"),
# #         data.get("transaction_id"),
# #         data.get("flw_ref"),
# #     )


# # # ------------------------------------------
# # # 3. Safely Update Transaction (Idempotent)
# # # ------------------------------------------

# # def safe_update_transaction(reference, flutterwave_id, flw_ref, verification_data):
# #     """
# #     Safely updates a transaction record based on Flutterwave verification result.

# #     This function is **IDEMPOTENT**:
# #     - calling multiple times will not double-confirm payments
# #     - prevents corrupting booking/payment
# #     """
# #     try:
# #         txn = Transaction.objects.select_related("booking").get(reference=reference)
# #     except Transaction.DoesNotExist:
# #         logger.warning(f"[TXN] No transaction found for reference={reference}. Ignored.")
# #         return None

# #     logger.info(f"[TXN] Loaded Transaction: {txn}")

# #     # Attach metadata for audit
# #     txn.meta = verification_data
# #     txn.provider = Transaction.PROVIDER_FLUTTERWAVE
# #     txn.provider_reference = flutterwave_id
# #     txn.save(update_fields=["meta", "provider", "updated_at"])

# #     # If Flutterwave says the transaction failed
# #     if verification_data.get("status") != "successful":
# #         logger.warning(f"[TXN] Transaction failed in verification: {reference}")
# #         txn.status = Transaction.STATUS_FAILED
# #         txn.save(update_fields=["status", "updated_at"])
# #         return txn

# #     # SUCCESS CASE
# #     txn.mark_successful()
# #     logger.info(f"[TXN] Transaction marked successful → Booking confirmed")

# #     return txn


# # payments/services.py
# import os
# import logging
# import requests
# from django.utils import timezone

# logger = logging.getLogger('payments')

# FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY", "")
# FLW_VERIFY_URL_TEMPLATE = "https://api.flutterwave.com/v3/transactions/{tx_ref}/verify"
# # fallback in case FLW_SECRET_KEY is not set
# if not FLW_SECRET_KEY:
#     logger.warning("FLW_SECRET_KEY not set in environment; verification requests will likely fail.")


# class FlutterwaveService:
#     """
#     Lightweight helper for calling Flutterwave verify endpoint.
#     Methods return a dict { 'ok': bool, 'status': str, 'data': dict, 'raw': dict }
#     """
#     @staticmethod
#     def verify_transaction(tx_ref: str, timeout: int = 10) -> dict:
#         if not tx_ref:
#             return {"ok": False, "error": "empty_tx_ref"}

#         url = FLW_VERIFY_URL_TEMPLATE.format(tx_ref=tx_ref)
#         headers = {"Authorization": f"Bearer {FLW_SECRET_KEY}"}
#         try:
#             resp = requests.get(url, headers=headers, timeout=timeout)
#         except requests.RequestException as exc:
#             logger.exception("Flutterwave verify request failed for %s", tx_ref)
#             return {"ok": False, "error": "request_exception", "exception": str(exc)}

#         try:
#             data = resp.json()
#         except Exception:
#             logger.exception("Invalid JSON from Flutterwave for %s (status=%s)", tx_ref, resp.status_code)
#             data = {"raw_text": resp.text}

#         # Normalized check: success + gateway status
#         ok = (resp.status_code in (200, 201) and data.get("status") == "success")
#         gateway_status = None
#         if isinstance(data.get("data"), dict):
#             gateway_status = data["data"].get("status") or data["data"].get("payment_status")

#         return {
#             "ok": ok,
#             "http_status": resp.status_code,
#             "status_field": data.get("status"),
#             "gateway_status": gateway_status,
#             "data": data.get("data"),
#             "raw": data,
#         }


# def retry_gateway_verification(txn):
#     """
#     Given a Transaction instance, attempt to verify it with the payment provider.
#     - For Flutterwave we call the verify endpoint using txn.reference (tx_ref).
#     - Idempotently update txn.status and meta.
#     - Return a dict describing the result.
#     """
#     if not txn:
#         return {"ok": False, "error": "missing_transaction"}

#     # prefer our reference
#     tx_ref = getattr(txn, "reference", None)
#     log = logger

#     if not tx_ref:
#         log.warning("Transaction has no reference; cannot verify via Flutterwave: txn_id=%s", getattr(txn, "id", None))
#         return {"ok": False, "error": "no_reference", "transaction_id": txn.id if hasattr(txn, "id") else None}

#     log.info("Retrying gateway verification for txn=%s reference=%s", txn.id, tx_ref)

#     # Use the service to verify
#     result = FlutterwaveService.verify_transaction(tx_ref)

#     # persist metadata about the attempt
#     meta = txn.meta or {}
#     meta.setdefault("verification_history", [])
#     meta["verification_history"].append({
#         "checked_at": timezone.now().isoformat(),
#         "result": result,
#     })

#     # If the external verification indicates success, mark transaction successful
#     if result.get("ok") and (result.get("gateway_status") or "").lower() in ("successful", "success", "completed"):
#         try:
#             # update meta, then mark success via the model helper (idempotent)
#             txn.meta = meta
#             txn.save(update_fields=["meta", "updated_at"])
#             txn.mark_successful()
#             log.info("Transaction %s marked successful after external verification.", txn.reference)
#             return {"ok": True, "action": "marked_success", "transaction_id": txn.id, "reference": txn.reference, "gateway": result}
#         except Exception as e:
#             log.exception("Error while marking transaction successful for %s: %s", txn.reference, e)
#             return {"ok": False, "error": "mark_success_exception", "exception": str(e), "gateway": result}
#     else:
#         # Not successful according to gateway: mark failed and persist the gateway payload for inspection
#         try:
#             txn.status = txn.STATUS_FAILED if hasattr(txn, "STATUS_FAILED") else "failed"
#             txn.meta = meta
#             txn.save(update_fields=["status", "meta", "updated_at"])
#             log.info("Transaction %s marked failed after external verification. gateway_status=%s", txn.reference, result.get("gateway_status"))
#             return {"ok": False, "action": "marked_failed", "transaction_id": txn.id, "reference": txn.reference, "gateway": result}
#         except Exception as e:
#             log.exception("Error while marking transaction failed for %s: %s", txn.reference, e)
#             return {"ok": False, "error": "mark_failed_exception", "exception": str(e), "gateway": result}

import logging
import requests
from django.conf import settings
from django.utils import timezone

from .models import Transaction

logger = logging.getLogger("payments")


# ---------------------------------------------------------
# FLUTTERWAVE VERIFY CALL (USED BY WEBHOOK + RETRY)
# ---------------------------------------------------------
def verify_flutterwave_transaction(txn: Transaction):
    """
    Calls Flutterwave's v3 verify API for a given Transaction.
    Returns the parsed API data or None on failure.
    """

    if not txn.flutterwave_id:
        logger.warning(f"[FW VERIFY] No flutterwave_id for txn {txn.reference}")
        return None

    url = f"https://api.flutterwave.com/v3/transactions/{txn.flutterwave_id}/verify"

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    logger.info(f"[FW VERIFY] Verifying FW transaction {txn.flutterwave_id}")

    try:
        resp = requests.get(url, headers=headers)
        data = resp.json()
    except Exception as e:
        logger.exception(f"[FW VERIFY] Network error: {e}")
        return None

    # Save raw data for audit
    txn.meta = {
        **(txn.meta or {}),
        "last_fw_verify": data,
        "last_verify_time": str(timezone.now()),
    }
    txn.save(update_fields=["meta"])

    return data


# ---------------------------------------------------------
# RETRY GATEWAY VERIFICATION (ADMIN ACTION)
# ---------------------------------------------------------
def retry_gateway_verification(txn: Transaction):
    """
    Unified verification entrypoint.
    Works for Flutterwave and can be extended for more gateways.
    Returns a simple result string.
    """

    if txn.provider != Transaction.PROVIDER_FLUTTERWAVE:
        return "IGNORED — only Flutterwave supported for retry right now."

    data = verify_flutterwave_transaction(txn)

    if not data:
        return "FAILED — could not verify transaction"

    fw_status = data.get("data", {}).get("status")

    if fw_status == "successful":
        txn.mark_successful()
        return "SUCCESS — transaction marked successful"

    elif fw_status in ["failed", "cancelled"]:
        txn.mark_failed("Gateway returned failed/cancelled")
        return "FAILED — gateway returned failed/cancelled"

    else:
        return f"PENDING — gateway status = {fw_status}"
