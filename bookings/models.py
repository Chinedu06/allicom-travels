# # bookings/models.py
# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone

# User = get_user_model()


# class Booking(models.Model):
#     """
#     Main booking model — represents a user booking a service.
#     Now updated to include full payment lifecycle awareness.
#     """

#     # ----------------------------
#     # Booking Statuses
#     # ----------------------------
#     STATUS_PENDING = 'pending'
#     STATUS_CONFIRMED = 'confirmed'
#     STATUS_CANCELLED = 'cancelled'

#     STATUS_CHOICES = [
#         (STATUS_PENDING, 'Pending'),
#         (STATUS_CONFIRMED, 'Confirmed'),
#         (STATUS_CANCELLED, 'Cancelled'),
#     ]

#     # ----------------------------
#     # Payment Statuses
#     # ----------------------------
#     PAY_UNPAID = 'unpaid'
#     PAY_PAID = 'paid'
#     PAY_REFUNDED = 'refunded'

#     PAYMENT_STATUS_CHOICES = [
#         (PAY_UNPAID, 'Unpaid'),
#         (PAY_PAID, 'Paid'),
#         (PAY_REFUNDED, 'Refunded'),
#     ]

#     # ----------------------------
#     # Fields
#     # ----------------------------
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey('services.Service', on_delete=models.CASCADE)

#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
#     )

#     payment_status = models.CharField(
#         max_length=20,
#         choices=PAYMENT_STATUS_CHOICES,
#         default=PAY_UNPAID
#     )

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     # Optional: extra info
#     details = models.JSONField(blank=True, null=True)

#     def __str__(self):
#         return f"Booking #{self.pk} - {self.user} ({self.status})"

#     # ----------------------------
#     # Helper Methods
#     # ----------------------------
#     def mark_confirmed(self):
#         self.status = self.STATUS_CONFIRMED
#         self.updated_at = timezone.now()
#         self.save(update_fields=['status', 'updated_at'])

#     def mark_cancelled(self):
#         self.status = self.STATUS_CANCELLED
#         self.updated_at = timezone.now()
#         self.save(update_fields=['status', 'updated_at'])

#     def mark_payment_paid(self):
#         self.payment_status = self.PAY_PAID
#         self.updated_at = timezone.now()
#         self.save(update_fields=['payment_status', 'updated_at'])

#     def mark_payment_failed(self):
#         self.payment_status = self.PAY_UNPAID
#         self.updated_at = timezone.now()
#         self.save(update_fields=['payment_status', 'updated_at'])


# class Notification(models.Model):
#     """
#     System notifications — visible to admin and users.
#     Payment updates, booking changes, etc.
#     """
#     recipient = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=True, blank=True
#     )
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Notification to {self.recipient or 'Admin'}"

#     @property
#     def short_message(self):
#         return (self.message[:50] + "...") if len(self.message) > 50 else self.message

# bookings/models.py
# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from services.models import Service, Package

# User = get_user_model()


# class Booking(models.Model):
#     """
#     Full restored Booking model with:
#     - tourist personal details
#     - package selection
#     - proof document upload
#     - booking lifecycle
#     - payment lifecycle
#     """

#     # ----------------------------
#     # Booking Statuses
#     # ----------------------------
#     STATUS_PENDING = "pending"
#     STATUS_CONFIRMED = "confirmed"
#     STATUS_REJECTED = "rejected"
#     STATUS_CANCELLED = "cancelled"

#     STATUS_CHOICES = [
#         (STATUS_PENDING, "Pending"),
#         (STATUS_CONFIRMED, "Confirmed"),
#         (STATUS_REJECTED, "Rejected"),
#         (STATUS_CANCELLED, "Cancelled"),
#     ]

#     # ----------------------------
#     # Payment Statuses
#     # ----------------------------
#     PAY_UNPAID = "unpaid"
#     PAY_PAID = "paid"
#     PAY_REFUNDED = "refunded"

#     PAYMENT_STATUS_CHOICES = [
#         (PAY_UNPAID, "Unpaid"),
#         (PAY_PAID, "Paid"),
#         (PAY_REFUNDED, "Refunded"),
#     ]

#     # ----------------------------
#     # Relationships
#     # ----------------------------
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     package = models.ForeignKey(
#         Package, on_delete=models.SET_NULL, null=True, blank=True
#     )

#     # ----------------------------
#     # Tourist Personal Details
#     # ----------------------------
#     given_name = models.CharField(max_length=120)
#     surname = models.CharField(max_length=120)
#     other_names = models.CharField(max_length=200, blank=True)
#     contact_number = models.CharField(max_length=100)
#     email = models.EmailField()
#     full_contact_address = models.TextField()

#     # ----------------------------
#     # Booking Metadata
#     # ----------------------------
#     num_adults = models.PositiveIntegerField(default=1)
#     num_children = models.PositiveIntegerField(default=0)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     notes = models.TextField(blank=True)
#     admin_note = models.TextField(blank=True)

#     proof_document = models.FileField(
#         upload_to="booking_proofs/", null=True, blank=True
#     )

#     # ----------------------------
#     # Status Fields
#     # ----------------------------
#     status = models.CharField(
#         max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING
#     )
#     payment_status = models.CharField(
#         max_length=30, choices=PAYMENT_STATUS_CHOICES, default=PAY_UNPAID
#     )

#     is_tnc_accepted = models.BooleanField(default=False)

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Booking #{self.pk} - {self.given_name} {self.surname}"

#     # ----------------------------
#     # Helper Methods
#     # ----------------------------
#     def mark_confirmed(self):
#         self.status = self.STATUS_CONFIRMED
#         self.updated_at = timezone.now()
#         self.save(update_fields=["status", "updated_at"])

#     def mark_cancelled(self):
#         self.status = self.STATUS_CANCELLED
#         self.updated_at = timezone.now()
#         self.save(update_fields=["status", "updated_at"])

#     def mark_payment_paid(self):
#         self.payment_status = self.PAY_PAID
#         self.updated_at = timezone.now()
#         self.save(update_fields=["payment_status", "updated_at"])

#     def mark_payment_failed(self):
#         self.payment_status = self.PAY_UNPAID
#         self.updated_at = timezone.now()
#         self.save(update_fields=["payment_status", "updated_at"])


# class Notification(models.Model):
#     """
#     Notification system for admin and users.
#     Shows booking events, payment events, system alerts.
#     """
#     recipient = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=True, blank=True
#     )
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"Notification to {self.recipient or 'Admin'}"

#     @property
#     def short_message(self):
#         return (
#             self.message[:50] + "..."
#             if len(self.message) > 50
#             else self.message
#         )

# bookings/models.py
from django.db import models
from django.conf import settings
from services.models import Service, Package
from django.utils import timezone


class Booking(models.Model):
    """
    RESTORED Booking model with full travel details, package selection,
    traveler info, dates, and admin workflow.
    """

    # ----------------------------
    # Booking Statuses
    # ----------------------------
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    # ----------------------------
    # Payment Statuses
    # ----------------------------
    PAYMENT_UNPAID = 'unpaid'
    PAYMENT_PAID = 'paid'
    PAYMENT_PENDING = 'pending_verification'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_UNPAID, 'Unpaid'),
        (PAYMENT_PAID, 'Paid'),
        (PAYMENT_PENDING, 'Pending Verification'),
    ]

    # ----------------------------
    # User & Service
    # ----------------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    # ⭐ RESTORED — Package linking support
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    # ----------------------------
    # Traveler & Contact Information
    # ----------------------------
    given_name = models.CharField(max_length=150)           # RESTORED
    surname = models.CharField(max_length=150)              # RESTORED
    other_names = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=40)        # RESTORED
    email = models.EmailField()                             # RESTORED
    full_contact_address = models.TextField(blank=True)     # RESTORED

    # ----------------------------
    # Booking Details
    # ----------------------------
    num_adults = models.PositiveIntegerField(default=1)      # RESTORED
    num_children = models.PositiveIntegerField(default=0)    # RESTORED
    start_date = models.DateField()                          # RESTORED
    end_date = models.DateField(null=True, blank=True)       # RESTORED
    notes = models.TextField(blank=True)                     # RESTORED

    # ----------------------------
    # Statuses
    # ----------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_UNPAID
    )

    is_tnc_accepted = models.BooleanField(default=False)     # RESTORED

    # Optional file upload (proof of booking, receipts, etc.)
    proof_document = models.FileField(
        upload_to='bookings/proofs/',
        null=True,
        blank=True
    )

    # ----------------------------
    # Admin Fields
    # ----------------------------
    admin_note = models.TextField(blank=True)               # RESTORED

    # ----------------------------
    # Timestamps
    # ----------------------------
    booking_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ----------------------------
    # Helpers
    # ----------------------------
    @property
    def total_price(self):
        """Package price overrides service price."""
        if self.package:
            return self.package.price
        return self.service.price

    def __str__(self):
        return f"Booking#{self.pk} {self.service.title} for {self.given_name} {self.surname}"


class Notification(models.Model):
    """
    Simple system notification table.
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification#{self.pk} to {self.recipient} - {self.message[:30]}..."
