# from django.conf import settings
# from django.db import models
# from services.models import Service, Package  # assume services app exists as earlier

# class Booking(models.Model):
#     STATUS_PENDING = 'pending'     # created but not paid / waiting admin confirmation
#     STATUS_PAID = 'paid'           # payment succeeded (gateway / manual confirmed)
#     STATUS_CONFIRMED = 'confirmed' # admin approved the booking (final)
#     STATUS_CANCELLED = 'cancelled' # user or admin cancelled
#     STATUS_REJECTED = 'rejected'   # admin rejected

#     STATUS_CHOICES = [
#         (STATUS_PENDING, 'Pending'),
#         (STATUS_PAID, 'Paid'),
#         (STATUS_CONFIRMED, 'Confirmed'),
#         (STATUS_CANCELLED, 'Cancelled'),
#         (STATUS_REJECTED, 'Rejected'),
#     ]

#     # optional authenticated user who made booking (null if anonymous tourist)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')

#     # required link to service (and optional package)
#     service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
#     package = models.ForeignKey(Package, on_delete=models.PROTECT, null=True, blank=True, related_name='bookings')

#     # contact & traveler details (collected from forms)
#     given_name = models.CharField(max_length=150)
#     surname = models.CharField(max_length=150)
#     other_names = models.CharField(max_length=150, blank=True)
#     contact_number = models.CharField(max_length=40)
#     email = models.EmailField()
#     full_contact_address = models.TextField(blank=True)

#     # booking detail fields
#     num_adults = models.PositiveIntegerField(default=1)
#     num_children = models.PositiveIntegerField(default=0)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     notes = models.TextField(blank=True)

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
#     is_tnc_accepted = models.BooleanField(default=False)  # tourist accepted terms

#     # admin fields
#     admin_note = models.TextField(blank=True)  # reason for rejection/notes
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # convenience property
#     @property
#     def total_price(self):
#         # priority: package.price if exists otherwise service.price
#         if self.package:
#             return self.package.price
#         return self.service.price

#     def __str__(self):
#         return f"Booking#{self.pk} {self.service.title} for {self.given_name} {self.surname}"

# # add at bottom of bookings/models.py

# class Notification(models.Model):
#     """
#     Simple notification table (in-app). recipient can be a User (staff/operator) or null for global/admin.
#     """
#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification#{self.pk} to {self.recipient} - {self.message[:30]}..."

# class Booking(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     package = models.ForeignKey('services.Package', on_delete=models.CASCADE)
#     status = models.CharField(
#         max_length=20,
#         choices=[
#             ('pending', 'Pending'),
#             ('confirmed', 'Confirmed'),
#             ('cancelled', 'Cancelled'),
#         ],
#         default='pending'
#     )
#     payment_status = models.CharField(
#         max_length=20,
#         choices=[
#             ('unpaid', 'Unpaid'),
#             ('paid', 'Paid'),
#             ('pending_verification', 'Pending Verification'),
#         ],
#         default='unpaid'
#     )
#     booking_date = models.DateTimeField(auto_now_add=True)

from django.conf import settings
from django.db import models
from services.models import Service, Package  # services app assumed to exist


class Booking(models.Model):
    STATUS_PENDING = 'pending'     # created but not paid / waiting admin confirmation
    STATUS_PAID = 'paid'           # payment succeeded (gateway / manual confirmed)
    STATUS_CONFIRMED = 'confirmed' # admin approved the booking (final)
    STATUS_CANCELLED = 'cancelled' # user or admin cancelled
    STATUS_REJECTED = 'rejected'   # admin rejected

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PAID, 'Paid'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    # optional authenticated user who made booking (null if anonymous tourist)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    # required link to service (and optional package)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.PROTECT, null=True, blank=True, related_name='bookings')

    # contact & traveler details (collected from forms)
    given_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    other_names = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=40)
    email = models.EmailField()
    full_contact_address = models.TextField(blank=True)

    # booking detail fields
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # payment status (used elsewhere in code)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', 'Unpaid'),
            ('paid', 'Paid'),
            ('pending_verification', 'Pending Verification'),
        ],
        default='unpaid'
    )

    is_tnc_accepted = models.BooleanField(default=False)  # tourist accepted terms

    # admin fields
    admin_note = models.TextField(blank=True)  # reason for rejection/notes

    # timestamps
    booking_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # convenience property
    @property
    def total_price(self):
        # priority: package.price if exists otherwise service.price
        if self.package:
            return self.package.price
        return self.service.price

    def __str__(self):
        return f"Booking#{self.pk} {self.service.title} for {self.given_name} {self.surname}"


class Notification(models.Model):
    """
    Simple notification table (in-app). recipient can be a User (staff/operator) or null for global/admin.
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

    def __str__(self):
        return f"Notification#{self.pk} to {self.recipient} - {self.message[:30]}..."
