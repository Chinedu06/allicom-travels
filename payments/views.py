# # # import json
# # # import logging
# # # import requests
# # # from django.conf import settings
# # # from django.utils import timezone
# # # from django.http import JsonResponse, HttpResponse
# # # from django.views.decorators.csrf import csrf_exempt
# # # from django.views.decorators.http import require_POST

# # # from rest_framework import generics, viewsets, permissions
# # # from rest_framework.decorators import api_view, permission_classes, action
# # # from rest_framework.response import Response

# # # from bookings.models import Booking
# # # from .models import Transaction, Payment
# # # from .serializers import (
# # #     PaymentSerializer,
# # #     TransactionSerializer,
# # #     BankTransferUploadSerializer
# # # )

# # # from .services import FlutterwaveService
# # # from .utils import safe_get_txn

# # # logger = logging.getLogger("payments")


# # # # ============================================================
# # # # 1️⃣ INITIATE PAYMENT  (Flutterwave, Bank, Mock)
# # # # ============================================================

# # # @api_view(["POST"])
# # # @permission_classes([permissions.AllowAny])
# # # def initiate_payment(request):
# # #     booking_id = request.data.get("booking")
# # #     provider = request.data.get("provider")

# # #     if not booking_id or not provider:
# # #         return Response({"detail": "booking and provider are required"}, status=400)

# # #     try:
# # #         booking = Booking.objects.get(pk=booking_id)
# # #     except Booking.DoesNotExist:
# # #         return Response({"detail": "Booking not found"}, status=404)

# # #     amount = booking.total_price

# # #     customer_email = (
# # #         getattr(booking, "customer_email", None)
# # #         or getattr(booking, "email", None)
# # #         or getattr(getattr(booking, "user", None), "email", None)
# # #         or "noemail@example.com"
# # #     )
# # #     customer_name = (
# # #         getattr(booking, "customer_name", None)
# # #         or getattr(getattr(booking, "user", None), "get_full_name", lambda: None)()
# # #         or "Unknown Customer"
# # #     )

# # #     txn = Transaction.objects.create(
# # #         booking=booking,
# # #         provider=provider,
# # #         amount=amount,
# # #         reference=f"ALC-{timezone.now().strftime('%Y%m%d%H%M%S%f')}",
# # #         status=Transaction.STATUS_INIT,
# # #     )

# # #     # FLUTTERWAVE
# # #     if provider == Transaction.PROVIDER_FLUTTERWAVE:
# # #         payload = {
# # #             "tx_ref": txn.reference,
# # #             "amount": str(amount),
# # #             "currency": "NGN",
# # #             "redirect_url": f"{settings.BASE_URL}/api/payments/redirect/",
# # #             "customer": {"email": customer_email, "name": customer_name},
# # #         }
# # #         headers = {
# # #             "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
# # #             "Content-Type": "application/json"
# # #         }

# # #         try:
# # #             resp = requests.post("https://api.flutterwave.com/v3/payments",
# # #                                  json=payload, headers=headers, timeout=10)
# # #             resp_data = resp.json()

# # #             if resp.status_code in (200, 201) and resp_data.get("status") == "success":
# # #                 txn.status = Transaction.STATUS_PENDING
# # #                 txn.save(update_fields=["status"])
# # #                 return Response({
# # #                     "payment_url": resp_data["data"]["link"],
# # #                     "transaction_id": txn.id,
# # #                     "reference": txn.reference
# # #                 })
# # #             else:
# # #                 txn.status = Transaction.STATUS_FAILED
# # #                 txn.save(update_fields=["status"])
# # #                 return Response({"detail": "Failed to initiate payment."}, status=400)

# # #         except Exception as e:
# # #             txn.status = Transaction.STATUS_FAILED
# # #             txn.save(update_fields=["status"])
# # #             return Response({"detail": str(e)}, status=500)

# # #     # BANK TRANSFER
# # #     elif provider == Transaction.PROVIDER_BANK:
# # #         txn.status = Transaction.STATUS_PENDING
# # #         txn.save()
# # #         return Response({
# # #             "transaction_id": txn.id,
# # #             "detail": "Upload bank receipt using /api/payments/upload-receipt/"
# # #         })

# # #     # MOCK OR OTHER PROVIDERS
# # #     else:
# # #         txn.status = Transaction.STATUS_PENDING
# # #         txn.save()
# # #         return Response({
# # #             "payment_url": f"https://pay.mock/{provider}/{txn.reference}",
# # #             "transaction_id": txn.id,
# # #             "reference": txn.reference
# # #         })


# # # # ============================================================
# # # # 2️⃣ BANK RECEIPT UPLOAD
# # # # ============================================================

# # # @api_view(["POST"])
# # # @permission_classes([permissions.IsAuthenticated])
# # # def upload_bank_receipt(request):
# # #     txid = request.data.get("transaction_id")
# # #     txn = Transaction.objects.get(pk=txid)

# # #     serializer = BankTransferUploadSerializer(txn, data=request.data, partial=True)

# # #     if serializer.is_valid():
# # #         serializer.save(provider=Transaction.PROVIDER_BANK,
# # #                         status=Transaction.STATUS_PENDING)
# # #         return Response({"detail": "Receipt uploaded. Awaiting admin verification."})

# # #     return Response(serializer.errors, status=400)


# # # # ============================================================
# # # # 3️⃣ REDIRECT HANDLER
# # # # ============================================================

# # # @csrf_exempt
# # # def flutterwave_redirect_view(request):
# # #     data = request.GET.dict() if request.method == "GET" else request.POST.dict()

# # #     tx_ref = data.get("tx_ref")
# # #     status = data.get("status")

# # #     if not tx_ref:
# # #         return JsonResponse({"error": "Missing tx_ref"}, status=400)

# # #     txn = safe_get_txn(tx_ref)
# # #     if not txn:
# # #         return JsonResponse({"error": "Transaction not found"}, status=404)

# # #     txn.meta = {"redirect_status": status, "redirect_raw": data}
# # #     txn.save(update_fields=["meta"])

# # #     verified = FlutterwaveService.verify_transaction(txn)

# # #     if verified:
# # #         return JsonResponse({"status": "success", "tx_ref": tx_ref})
# # #     return JsonResponse({"status": "failed", "tx_ref": tx_ref})


# # # # ============================================================
# # # # 4️⃣ WEBHOOK HANDLER
# # # # ============================================================

# # # @csrf_exempt
# # # @require_POST
# # # def flutterwave_webhook_view(request):
# # #     received_hash = request.headers.get("verif-hash")
# # #     if received_hash != settings.FLW_SECRET_HASH:
# # #         return HttpResponse("ok")

# # #     try:
# # #         data = json.loads(request.body.decode())
# # #     except:
# # #         return HttpResponse("ok")

# # #     tx_ref = data.get("tx_ref")
# # #     status = data.get("status")

# # #     txn = safe_get_txn(tx_ref)
# # #     if not txn:
# # #         return HttpResponse("ok")

# # #     txn.meta = {"webhook_status": status, "webhook_raw": data}
# # #     txn.save(update_fields=["meta"])

# # #     if status == "successful":
# # #         FlutterwaveService.verify_transaction(txn)

# # #     return HttpResponse("ok")


# # # # ============================================================
# # # # 5️⃣ VIEWSETS
# # # # ============================================================

# # # class TransactionViewSet(viewsets.ModelViewSet):
# # #     queryset = Transaction.objects.all().order_by("-created_at")
# # #     serializer_class = TransactionSerializer


# # # class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
# # #     queryset = Payment.objects.all().order_by("-paid_at")
# # #     serializer_class = PaymentSerializer


# # # class PaymentCreateView(generics.CreateAPIView):
# # #     serializer_class = PaymentSerializer
# # #     permission_classes = [permissions.IsAuthenticated]

# # #     def perform_create(self, serializer):
# # #         payment = serializer.save()
# # #         booking = payment.booking
# # #         booking.payment_status = "paid"
# # #         booking.status = Booking.STATUS_CONFIRMED
# # #         booking.save(update_fields=["payment_status", "status"])

# # # payments/views.py
# # import json
# # import logging
# # import requests

# # from django.conf import settings
# # from django.http import JsonResponse, HttpResponse
# # from django.shortcuts import get_object_or_404, redirect
# # from django.urls import reverse
# # from django.views.decorators.csrf import csrf_exempt

# # from bookings.models import Booking
# # from payments.models import Transaction

# # logger = logging.getLogger("payments")


# # # -------------------------------------------------------
# # # 1. Initialize Flutterwave Payment
# # # -------------------------------------------------------
# # def initiate_flutterwave_payment(request, booking_id):
# #     """
# #     Creates a Flutterwave payment session and returns the redirect URL.
# #     """
# #     booking = get_object_or_404(Booking, id=booking_id)

# #     if booking.payment_status == Booking.PAY_PAID:
# #         return JsonResponse({"error": "Booking already paid."}, status=400)

# #     # Generate unique reference
# #     reference = f"ALC-{booking.id}-{Transaction.objects.count() + 1}"

# #     # Create Transaction record
# #     txn = Transaction.objects.create(
# #         booking=booking,
# #         reference=reference,
# #         provider=Transaction.PROVIDER_FLUTTERWAVE,
# #         amount=booking.service.amount,
# #         status=Transaction.STATUS_INIT
# #     )

# #     callback_url = request.build_absolute_uri(
# #         reverse("flutterwave-callback")
# #     )

# #     payload = {
# #         "tx_ref": reference,
# #         "amount": float(booking.service.amount),
# #         "currency": "NGN",
# #         "redirect_url": callback_url,
# #         "payment_options": "card",
# #         "customer": {
# #             "email": booking.user.email,
# #             "name": booking.user.get_full_name() or booking.user.username,
# #         },
# #         "customizations": {
# #             "title": "Allicom Travels Payment",
# #             "description": f"Payment for booking #{booking.id}"
# #         }
# #     }

# #     headers = {
# #         "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
# #         "Content-Type": "application/json"
# #     }

# #     try:
# #         response = requests.post(
# #             "https://api.flutterwave.com/v3/payments",
# #             headers=headers,
# #             json=payload
# #         )
# #         res = response.json()

# #         logger.info(f"[FW INIT] Response: {json.dumps(res, indent=2)}")

# #         if res.get("status") != "success":
# #             txn.mark_failed("Flutterwave init error")
# #             return JsonResponse({"error": "Failed to initialize payment"}, status=400)

# #         payment_link = res["data"]["link"]
# #         return redirect(payment_link)

# #     except Exception as e:
# #         logger.exception(f"[FW INIT] Error: {e}")
# #         txn.mark_failed("Exception during FW init")
# #         return JsonResponse({"error": "Payment initialization failed"}, status=500)


# # # -------------------------------------------------------
# # # 2. Flutterwave Redirect Callback
# # # -------------------------------------------------------
# # def flutterwave_callback(request):
# #     """
# #     Handles user redirect after FW payment.
# #     """
# #     status = request.GET.get("status")
# #     tx_ref = request.GET.get("tx_ref")
# #     flw_tx_id = request.GET.get("transaction_id")

# #     logger.info(f"[FW CALLBACK] status={status}, tx_ref={tx_ref}, id={flw_tx_id}")

# #     txn = get_object_or_404(Transaction, reference=tx_ref)

# #     # Store FW transaction ID
# #     txn.flutterwave_id = flw_tx_id
# #     txn.save(update_fields=["flutterwave_id"])

# #     if status == "successful":
# #         return redirect(reverse("verify-flutterwave", args=[tx_ref]))

# #     if status in ["cancelled", "failed"]:
# #         txn.mark_failed("User cancelled or FW returned failed")
# #         return HttpResponse("Payment Failed or Cancelled")

# #     return HttpResponse("Unknown payment state.")


# # # -------------------------------------------------------
# # # 3. Server-to-Server Payment Verification
# # # -------------------------------------------------------
# # def verify_flutterwave(request, tx_ref):
# #     """
# #     Confirms Flutterwave transaction using the verify API.
# #     """
# #     txn = get_object_or_404(Transaction, reference=tx_ref)

# #     if txn.status == Transaction.STATUS_SUCCESS:
# #         return HttpResponse("Payment already verified.")

# #     if not txn.flutterwave_id:
# #         return HttpResponse("Missing Flutterwave ID. Cannot verify.", status=400)

# #     url = f"https://api.flutterwave.com/v3/transactions/{txn.flutterwave_id}/verify"

# #     headers = {
# #         "Authorization": f"Bearer {settings.FLW_SECRET_KEY}"
# #     }

# #     try:
# #         resp = requests.get(url, headers=headers)
# #         data = resp.json()

# #         logger.info("[FW VERIFY] Response: %s", json.dumps(data, indent=2))

# #         fw_status = data.get("data", {}).get("status")

# #         if fw_status == "successful":
# #             txn.mark_successful()
# #             return HttpResponse("Payment Verified Successfully")

# #         else:
# #             txn.mark_failed("Verification returned non-success state")
# #             return HttpResponse("Payment Verification Failed")

# #     except Exception as e:
# #         logger.exception("[FW VERIFY] Error verifying FW payment")
# #         return HttpResponse("Error verifying payment", status=500)


# # # -------------------------------------------------------
# # # 4. Flutterwave Webhook (optional)
# # # -------------------------------------------------------
# # @csrf_exempt
# # def flutterwave_webhook(request):
# #     """
# #     Handles webhook notifications from Flutterwave.
# #     """
# #     try:
# #         payload = json.loads(request.body.decode("utf-8"))
# #         logger.info("[FW WEBHOOK] Payload: %s", json.dumps(payload, indent=2))

# #         tx_ref = payload.get("data", {}).get("tx_ref")
# #         fw_status = payload.get("data", {}).get("status")

# #         txn = Transaction.objects.filter(reference=tx_ref).first()

# #         if not txn:
# #             return JsonResponse({"error": "Transaction not found"}, status=404)

# #         if fw_status == "successful":
# #             txn.mark_successful()
# #         else:
# #             txn.mark_failed(f"Webhook status {fw_status}")

# #         return JsonResponse({"status": "ok"})

# #     except Exception as e:
# #         logger.exception("[FW WEBHOOK] Error")
# #         return JsonResponse({"error": "Internal error"}, status=500)

# # payments/views.py
# import logging
# from django.shortcuts import get_object_or_404
# from django.utils import timezone

# from rest_framework import viewsets, status, generics, permissions
# from rest_framework.decorators import api_view, permission_classes, action
# from rest_framework.response import Response

# from .models import Transaction, Payment
# from .serializers import (
#     TransactionSerializer,
#     PaymentSerializer,
#     BankTransferUploadSerializer,
# )
# from bookings.models import Booking

# logger = logging.getLogger("payments")


# # -------------------------------
# # Functional / simple endpoints
# # -------------------------------
# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def initiate_payment(request):
#     """
#     Create a Transaction for a booking and return data the frontend (or client)
#     can use to redirect the user to a payment provider. For redirect flow:
#       - create Transaction (status = init)
#       - return payment_url (or provider reference) to client

#     Expected POST JSON:
#       {
#         "booking": <booking_id>,
#         "provider": "flutterwave" | "interswitch" | "bank_transfer"
#       }
#     """
#     data = request.data
#     booking_id = data.get("booking")
#     provider = data.get("provider")

#     if not booking_id or not provider:
#         return Response({"detail": "booking and provider are required"}, status=400)

#     booking = get_object_or_404(Booking, pk=booking_id)

#     # derive amount from booking total_price property (package/service)
#     amount = getattr(booking, "total_price", None) or 0

#     # create transaction reference (simple unique-ish reference)
#     import uuid
#     reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"

#     txn = Transaction.objects.create(
#         booking=booking,
#         reference=reference,
#         amount=amount,
#         provider=provider,
#         status=Transaction.STATUS_INIT,
#     )

#     # For a real provider you'd call their API and get a redirect/payment link.
#     # For now we return a mock payment_url (consistent with earlier code)
#     if provider == Transaction.PROVIDER_FLUTTERWAVE:
#         # In production, create a payment session and store provider id (flutterwave_id)
#         payment_url = f"https://pay.flutterwave.mock/checkout/{txn.reference}"
#         return Response(
#             {"payment_url": payment_url, "transaction_id": txn.id, "reference": txn.reference}
#         )

#     if provider == Transaction.PROVIDER_INTERSWITCH:
#         payment_url = f"https://pay.interswitch.mock/redirect/{txn.reference}"
#         return Response(
#             {"payment_url": payment_url, "transaction_id": txn.id, "reference": txn.reference}
#         )

#     # bank transfer: client should upload receipt against txn.id
#     txn.status = Transaction.STATUS_PENDING
#     txn.save(update_fields=["status", "updated_at"])
#     return Response(
#         {
#             "transaction_id": txn.id,
#             "detail": "Use this transaction_id to upload bank receipt to /api/payments/upload-receipt/",
#         }
#     )


# @api_view(["POST"])
# @permission_classes([permissions.AllowAny])
# def gateway_webhook_verify(request):
#     """
#     Generic webhook endpoint for payment providers.
#     Expected JSON (example):
#       {
#         "provider": "flutterwave",
#         "provider_reference": "<provider_txn_id>",
#         "transaction_reference": "<our_txn_ref_or_null>",
#         "status": "success" | "failed" | "cancelled"
#       }

#     Behavior:
#       - try to locate Transaction by provider_reference -> reference
#       - idempotently update txn.status and call txn.mark_successful() for success
#     """
#     data = request.data
#     provider = data.get("provider")
#     provider_reference = data.get("provider_reference")
#     status_str = data.get("status")
#     our_ref = data.get("transaction_reference")

#     if not provider_reference and not our_ref:
#         return Response({"detail": "provider_reference or transaction_reference required"}, status=400)

#     txn = None

#     # Prefer lookup by provider_reference where stored (flutterwave_id etc.)
#     if provider_reference:
#         txn = Transaction.objects.filter(provider=provider, flutterwave_id=provider_reference).first()
#         if not txn:
#             # fallback to searching provider_reference in meta
#             txn = Transaction.objects.filter(meta__provider_reference=provider_reference).first()

#     if not txn and our_ref:
#         txn = Transaction.objects.filter(reference=our_ref).first()

#     if not txn:
#         logger.warning("Webhook for unknown transaction provider_reference=%s provider=%s", provider_reference, provider)
#         return Response({"detail": "transaction not found"}, status=404)

#     # If provider sent a provider_reference and we didn't yet store it, save it
#     if provider_reference and not txn.flutterwave_id:
#         txn.flutterwave_id = provider_reference
#         txn.save(update_fields=["flutterwave_id", "updated_at"])

#     # Idempotent update
#     if status_str in ("success", "successful"):
#         if txn.status != Transaction.STATUS_SUCCESS:
#             txn.status = Transaction.STATUS_SUCCESS
#             txn.save(update_fields=["status", "updated_at"])
#             try:
#                 txn.mark_successful()
#             except Exception:
#                 logger.exception("Error running mark_successful for txn %s", txn.reference)
#         else:
#             logger.info("Webhook received for already successful txn %s", txn.reference)
#         return Response({"detail": "verified and booking confirmed"}, status=200)
#     else:
#         # mark failed/cancelled
#         if txn.status != Transaction.STATUS_FAILED:
#             txn.status = Transaction.STATUS_FAILED
#             txn.save(update_fields=["status", "updated_at"])
#         return Response({"detail": "marked failed"}, status=200)


# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def upload_bank_receipt(request):
#     """
#     Upload a receipt file for bank transfer transactions.
#     Expected form-data:
#       - transaction_id
#       - receipt (file)
#     """
#     txid = request.data.get("transaction_id")
#     if not txid:
#         return Response({"detail": "transaction_id required"}, status=400)

#     txn = get_object_or_404(Transaction, pk=txid)

#     serializer = BankTransferUploadSerializer(instance=txn, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save(provider=Transaction.PROVIDER_BANK, status=Transaction.STATUS_PENDING)
#         return Response({"detail": "receipt uploaded, admin will verify."})
#     return Response(serializer.errors, status=400)


# # -------------------------------
# # Class-based views (ViewSets)
# # -------------------------------
# class TransactionViewSet(viewsets.ModelViewSet):
#     """
#     Full CRUD for Transaction (admin use). Includes an action to manually verify
#     a transaction by calling mark_successful().
#     """
#     queryset = Transaction.objects.all().order_by("-created_at")
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAdminUser]

#     @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
#     def verify(self, request, pk=None):
#         transaction = self.get_object()
#         try:
#             transaction.mark_successful()
#             return Response({"detail": "Transaction verified and synced."}, status=200)
#         except Exception as e:
#             logger.exception("Error verifying txn %s", transaction.reference)
#             return Response({"detail": f"Error: {e}"}, status=500)


# class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Read-only viewset for payment records (admins/support).
#     """
#     queryset = Payment.objects.all().order_by("-paid_at")
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAdminUser]

import logging
import uuid
from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.urls import reverse

from bookings.models import Booking
from .models import Transaction
# from .services import verify_flutterwave_payment
# from claude
from .services import verify_flutterwave_transaction

logger = logging.getLogger("payments")


# =====================================================================
# 1) Initialize Payment (Flutterwave)
# =====================================================================
def initialize_payment(request, booking_id):
    """
    1. User clicks "Pay Now"
    2. We create a Transaction
    3. Redirect user to Flutterwave checkout
    """

    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseBadRequest("Invalid booking ID")

    # Amount must come from booking/service/package (not user)
    amount = Decimal(booking.service.price)

    # Create transaction
    reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    txn = Transaction.objects.create(
        booking=booking,
        reference=reference,
        amount=amount,
        provider=Transaction.PROVIDER_FLUTTERWAVE,
        status=Transaction.STATUS_INIT,
    )

    logger.info(f"[Init Payment] Created Txn {reference} for Booking {booking.id}")

    # Flutterwave redirect
    redirect_url = settings.FLUTTERWAVE_REDIRECT_URL.format(reference=reference)

    return JsonResponse({
        "payment_url": redirect_url,
        "reference": reference,
        "status": "ok"
    })


# =====================================================================
# 2) Flutterwave Redirect Success Handler
# =====================================================================
def payment_success(request):
    """
    2. User returns from Flutterwave after paying.
    Example callback: /payments/success?status=successful&tx_ref=TXN-123
    """

    reference = request.GET.get("tx_ref") or request.GET.get("reference")

    if not reference:
        return HttpResponseBadRequest("Missing tx_ref")

    try:
        txn = Transaction.objects.get(reference=reference)
    except Transaction.DoesNotExist:
        return HttpResponseBadRequest("Unknown transaction")

    # Immediately verify via API
    # verify_flutterwave_payment(txn)
    # from claude
    verify_flutterwave_transaction(txn)

    # After verification, redirect to frontend success page
    frontend_url = settings.PAYMENT_FRONTEND_SUCCESS_URL.format(reference=reference)

    return redirect(frontend_url)


# =====================================================================
# 3) Flutterwave Redirect Failure Handler
# =====================================================================
def payment_cancelled(request):
    """
    Called when user cancels payment or fails at checkout.
    """
    reference = request.GET.get("tx_ref") or "(unknown)"

    logger.warning(f"[Payment Cancelled] User cancelled payment for {reference}")

    frontend_url = settings.PAYMENT_FRONTEND_CANCELLED_URL

    return redirect(frontend_url)


# =====================================================================
# 4) Flutterwave Webhook (MOST IMPORTANT)
# =====================================================================
@csrf_exempt
def flutterwave_webhook(request):
    """
    4. Flutterwave webhook verification (server → server)
    This is REQUIRED for real payments.
    """

    if request.method != "POST":
        return HttpResponse("Invalid method", status=405)

    try:
        payload = request.body.decode("utf-8")
        import json
        data = json.loads(payload)
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    logger.info(f"[FW Webhook] Received: {data}")

    reference = data.get("data", {}).get("tx_ref")

    if not reference:
        return HttpResponseBadRequest("Missing tx_ref")

    try:
        txn = Transaction.objects.get(reference=reference)
    except Transaction.DoesNotExist:
        return HttpResponseBadRequest("Unknown reference")

    # Save raw webhook metadata
    txn.meta = {
        **(txn.meta or {}),
        "webhook": data,
    }
    txn.save(update_fields=["meta"])

    # If payment is successful, verify with API
    if data.get("data", {}).get("status") == "successful":
        # verify_flutterwave_payment(txn)
        # from claude
        verify_flutterwave_transaction(txn)

    return HttpResponse("Webhook OK", status=200)


# =====================================================================
# 5) Debug Endpoint — Check Payment Status (optional)
# =====================================================================
def check_payment_status(request, reference):
    """
    Small optional endpoint used by frontend or mobile apps.
    """
    try:
        txn = Transaction.objects.get(reference=reference)
        booking = txn.booking
    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Invalid reference"}, status=404)

    return JsonResponse({
        "reference": txn.reference,
        "status": txn.status,
        "provider": txn.provider,
        "amount": float(txn.amount),
        "booking_status": booking.status,
        "payment_status": booking.payment_status,
    })
