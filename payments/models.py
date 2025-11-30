# # payments/models.py
# import logging
# import requests
# from django.conf import settings
# from django.db import models
# from django.utils import timezone
# from bookings.models import Booking

# logger = logging.getLogger("payments")


# class Transaction(models.Model):
#     """
#     Stores all raw transaction records (from gateways, banks, etc.).
#     Used for audit logging, retries, webhooks, and reconciliation.
#     """

#     # ----------------------------
#     # Providers
#     # ----------------------------
#     PROVIDER_FLUTTERWAVE = 'flutterwave'
#     PROVIDER_INTERSWITCH = 'interswitch'
#     PROVIDER_BANK = 'bank_transfer'

#     PROVIDER_CHOICES = [
#         (PROVIDER_FLUTTERWAVE, 'Flutterwave'),
#         (PROVIDER_INTERSWITCH, 'Interswitch'),
#         (PROVIDER_BANK, 'Bank Transfer'),
#     ]

#     # ----------------------------
#     # Status Codes
#     # ----------------------------
#     STATUS_INIT = 'init'
#     STATUS_PENDING = 'pending'
#     STATUS_SUCCESS = 'success'
#     STATUS_FAILED = 'failed'

#     STATUS_CHOICES = [
#         (STATUS_INIT, 'Initialized'),
#         (STATUS_PENDING, 'Pending'),
#         (STATUS_SUCCESS, 'Success'),
#         (STATUS_FAILED, 'Failed'),
#     ]

#     # ----------------------------
#     # Fields
#     # ----------------------------
#     booking = models.ForeignKey(
#         Booking, on_delete=models.CASCADE, related_name='transactions'
#     )

#     reference = models.CharField(max_length=255, unique=True)
#     provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default=STATUS_INIT
#     )

#     flutterwave_id = models.CharField(
#         max_length=100, blank=True, null=True,
#         help_text="The `id` returned by Flutterwave"
#     )

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Extra data (webhook dumps, API responses, logs, metadata)
#     meta = models.JSONField(blank=True, null=True)

#     class Meta:
#         ordering = ['-created_at']

#     # ----------------------------
#     # String Representation
#     # ----------------------------
#     def __str__(self):
#         return f"{self.reference} ({self.status})"

#     # ----------------------------
#     # Status Helpers
#     # ----------------------------
#     def mark_successful(self):
#         """
#         Idempotent success handler.
#         Safe to call multiple times.
#         """
#         if self.status == self.STATUS_SUCCESS:
#             return  # already successful — do NOT duplicate actions

#         logger.info(f"[Transaction] Marking successful: {self.reference}")

#         self.status = self.STATUS_SUCCESS
#         self.save(update_fields=['status', 'updated_at'])

#         # Sync payment + booking
#         self.sync_payment_from_transaction()

#     def mark_failed(self, reason=""):
#         """
#         Marks the transaction as failed (idempotent).
#         """
#         if self.status == self.STATUS_FAILED:
#             return

#         logger.warning(f"[Transaction] Marking FAILED: {self.reference} — {reason}")

#         self.status = self.STATUS_FAILED
#         self.save(update_fields=['status', 'updated_at'])

#     # ----------------------------
#     # Payment Sync Logic
#     # ----------------------------
#     def sync_payment_from_transaction(self):
#         """
#         When FW confirms 'success', update the Payment + Booking.
#         """
#         from payments.models import Payment

#         logger.info(f"[Payment Sync] Syncing payment for Txn: {self.reference}")

#         Payment.objects.update_or_create(
#             booking=self.booking,
#             defaults={
#                 'amount': self.amount,
#                 'provider': self.provider,
#                 'status': 'paid',
#                 'reference': self.reference,
#                 'paid_at': timezone.now(),
#             }
#         )

#         # Update booking
#         b = self.booking
#         b.payment_status = 'paid'
#         b.status = Booking.STATUS_CONFIRMED
#         b.save(update_fields=['payment_status', 'status', 'updated_at'])

#     # ----------------------------
#     # Flutterwave Retry Verification
#     # ----------------------------
#     def verify_again(self):
#         """
#         Calls Flutterwave's live verify endpoint to re-confirm a transaction.
#         Used by admin actions & manual retry operations.

#         Returns a dict:
#         {
#             "action": "success" | "failed" | "ignored",
#             "fw_status": "successful" | "failed" | "pending" | None,
#             "response": <full FW API JSON>
#         }
#         """

#         if self.provider != self.PROVIDER_FLUTTERWAVE:
#             return {"action": "ignored", "error": "not_flutterwave"}

#         if not self.flutterwave_id:
#             return {"action": "ignored", "error": "no_flutterwave_id"}

#         FLW_SECRET_KEY = settings.FLW_SECRET_KEY

#         url = f"https://api.flutterwave.com/v3/transactions/{self.flutterwave_id}/verify"

#         headers = {
#             "Authorization": f"Bearer {FLW_SECRET_KEY}",
#             "Content-Type": "application/json",
#         }

#         logger.info(f"[Retry Verify] Verifying FW Txn ID {self.flutterwave_id}")

#         try:
#             resp = requests.get(url, headers=headers)
#             data = resp.json()
#         except Exception as e:
#             logger.exception(f"[Retry Verify] Request error: {e}")
#             return {"action": "ignored", "error": "request_failed"}

#         fw_status = data.get("data", {}).get("status")

#         # Store full metadata for audit
#         self.meta = {
#             **(self.meta or {}),
#             "retry_verify_response": data,
#             "retry_timestamp": str(timezone.now()),
#         }
#         self.save(update_fields=['meta'])

#         # Process the FW status
#         if fw_status == "successful":
#             self.mark_successful()
#             return {"action": "success", "fw_status": fw_status, "response": data}

#         elif fw_status in ["failed", "cancelled"]:
#             self.mark_failed(reason="FW verification returned failed/cancelled")
#             return {"action": "failed", "fw_status": fw_status, "response": data}

#         else:
#             return {"action": "ignored", "fw_status": fw_status, "response": data}


# class Payment(models.Model):
#     """
#     Represents the final payment record for a booking.
#     Only created when a successful transaction occurs.
#     """
#     booking = models.OneToOneField(
#         Booking, on_delete=models.CASCADE, related_name='payment'
#     )

#     reference = models.CharField(max_length=255, blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     provider = models.CharField(max_length=50, blank=True, null=True)
#     status = models.CharField(max_length=20, default='unpaid')  # unpaid, paid, refunded
#     paid_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"Payment for {self.booking} - {self.status}"

#     @property
#     def is_paid(self):
#         return self.status == 'paid'

# payments/models.py
import logging
from django.conf import settings
from django.db import models
from django.utils import timezone
from bookings.models import Booking

logger = logging.getLogger("payments")


class Transaction(models.Model):
    """
    Stores all raw transaction records (from gateways, banks, etc.)
    Used for audit, retries, and reconciliation.
    """
    PROVIDER_FLUTTERWAVE = "flutterwave"
    PROVIDER_INTERSWITCH = "interswitch"
    PROVIDER_BANK = "bank_transfer"

    PROVIDER_CHOICES = [
        (PROVIDER_FLUTTERWAVE, "Flutterwave"),
        (PROVIDER_INTERSWITCH, "Interswitch"),
        (PROVIDER_BANK, "Bank Transfer"),
    ]

    STATUS_INIT = "init"
    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_INIT, "Initialized"),
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="transactions")
    reference = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    provider_reference = models.CharField(max_length=255, blank=True, null=True)  # provider's id / ref
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_INIT)

    # optional: store provider-specific id (flutterwave id, etc.)
    flutterwave_id = models.CharField(max_length=100, blank=True, null=True)

    # Upload for bank receipts (optional)
    receipt = models.FileField(upload_to="payment_receipts/", null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    meta = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} ({self.status})"

    def mark_successful(self):
        """
        Idempotent success handling: create/update Payment and mark booking paid.
        """
        if self.status == self.STATUS_SUCCESS:
            return

        logger.info(f"[Transaction] Marking successful: {self.reference}")
        self.status = self.STATUS_SUCCESS
        self.save(update_fields=["status", "updated_at"])

        # sync/create payment
        self.sync_payment_from_transaction()

    def mark_failed(self, reason=""):
        if self.status == self.STATUS_FAILED:
            return
        logger.warning(f"[Transaction] Marking failed: {self.reference} — {reason}")
        self.status = self.STATUS_FAILED
        self.save(update_fields=["status", "updated_at"])

    def sync_payment_from_transaction(self):
        """
        Create or update Payment record from this transaction.
        """
        from payments.models import Payment  # local import to avoid circular at top-level

        Payment.objects.update_or_create(
            booking=self.booking,
            defaults={
                "amount": self.amount,
                "provider": self.provider,
                "status": "paid",
                "reference": self.reference,
                "paid_at": timezone.now(),
            },
        )

        # Update booking
        b = self.booking
        b.payment_status = "paid"
        b.status = Booking.STATUS_CONFIRMED
        b.save(update_fields=["payment_status", "status", "updated_at"])


class Payment(models.Model):
    """
    Final confirmed payment record for a booking.
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    reference = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    provider = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default="unpaid")  # unpaid, paid, refunded
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.booking} - {self.status}"

    @property
    def is_paid(self):
        return self.status == "paid"
