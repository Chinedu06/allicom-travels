from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for Allicom Travels.
    Roles: admin, operator
    """
    ROLE_ADMIN = 'admin'
    ROLE_OPERATOR = 'operator'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_OPERATOR, 'Tour Operator'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_OPERATOR,
        help_text="Designates the role of the user in the platform."
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Admin approval for Operators

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
