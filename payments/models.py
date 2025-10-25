# from django.conf import settings
# from django.db import models
# from bookings.models import Booking

# class Transaction(models.Model):
#     PROVIDER_FLUTTERWAVE = 'flutterwave'
#     PROVIDER_INTERSWITCH = 'interswitch'
#     PROVIDER_BANK = 'bank_transfer'

#     PROVIDER_CHOICES = [
#         (PROVIDER_FLUTTERWAVE, 'Flutterwave'),
#         (PROVIDER_INTERSWITCH, 'Interswitch'),
#         (PROVIDER_BANK, 'Bank Transfer'),
#     ]

#     STATUS_INIT = 'init'
#     STATUS_SUCCESS = 'success'
#     STATUS_FAILED = 'failed'
#     STATUS_PENDING = 'pending'  # bank transfer waiting for admin confirm

#     STATUS_CHOICES = [
#         (STATUS_INIT, 'Initialized'),
#         (STATUS_PENDING, 'Pending'),
#         (STATUS_SUCCESS, 'Success'),
#         (STATUS_FAILED, 'Failed'),
#     ]

#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
#     provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
#     provider_reference = models.CharField(max_length=255, blank=True, null=True)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_INIT)
#     receipt = models.FileField(upload_to='payment_receipts/', null=True, blank=True)  # for bank transfer uploads
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Txn#{self.pk} {self.provider} - {self.status}"

# class Payment(models.Model):
#     booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE)
#     reference = models.CharField(max_length=100, unique=True)
#     provider = models.CharField(
#         max_length=20,
#         choices=[
#             ('flutterwave', 'Flutterwave'),
#             ('interswitch', 'Interswitch'),
#             ('bank_transfer', 'Bank Transfer'),
#         ]
#     )
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(
#         max_length=20,
#         choices=[
#             ('pending', 'Pending'),
#             ('successful', 'Successful'),
#             ('failed', 'Failed'),
#         ],
#         default='pending'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.utils import timezone
from bookings.models import Booking


class Transaction(models.Model):
    """
    Stores all raw transaction records (from gateways, banks, etc.)
    Used for audit, retries, and reconciliation.
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    reference = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=50)  # e.g., 'flutterwave', 'paystack', 'bank_transfer'
    status = models.CharField(max_length=20, default='pending')  # pending, success, failed
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    meta = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference} ({self.status})"

    def mark_successful(self):
        """
        Called when transaction is verified as successful.
        """
        self.status = 'success'
        self.save()
        self.sync_payment_from_transaction()

    def sync_payment_from_transaction(self):
        """
        Updates or creates a Payment record for this transaction.
        """
        Payment.objects.update_or_create(
            booking=self.booking,
            defaults={
                'amount': self.amount,
                'provider': self.provider,
                'status': 'paid',
                'reference': self.reference,
                'paid_at': timezone.now(),
            }
        )


class Payment(models.Model):
    """
    Represents the final confirmed payment record for a booking.
    One Payment per booking.
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    reference = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provider = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='unpaid')  # unpaid, paid, refunded
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.booking} - {self.status}"

    @property
    def is_paid(self):
        return self.status == 'paid'
