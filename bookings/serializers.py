# # from rest_framework import serializers
# # from .models import Booking, Notification
# # from services.models import Service, Package

# # class BookingCreateSerializer(serializers.ModelSerializer):
# #     # Allow package id as optional (frontend sends package id)
# #     package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False, allow_null=True)

# #     class Meta:
# #         model = Booking
# #         fields = [
# #             "id", "user", "service", "package",
# #             "given_name", "surname", "other_names",
# #             "contact_number", "email", "full_contact_address",
# #             "num_adults", "num_children", "start_date", "end_date", "notes",
# #             "is_tnc_accepted", "status", "created_at",
# #         ]
# #         read_only_fields = ("id", "status", "created_at", "user")

# #     def validate(self, attrs):
# #         # ensure terms accepted
# #         if not attrs.get("is_tnc_accepted", False):
# #             raise serializers.ValidationError("Tourist must accept terms and conditions.")
# #         # ensure service exists (DRF will handle based on PK)
# #         service = attrs.get("service")
# #         package = attrs.get("package")
# #         if package and package.service_id != service.id:
# #             raise serializers.ValidationError("Selected package does not belong to the chosen service.")
# #         return attrs

# # class BookingDetailSerializer(serializers.ModelSerializer):
# #     package = serializers.SerializerMethodField()
# #     service = serializers.StringRelatedField()
# #     class Meta:
# #         model = Booking
# #         fields = "__all__"

# #     def get_package(self, obj):
# #         if not obj.package:
# #             return None
# #         return {
# #             "id": obj.package.id,
# #             "name": obj.package.name,
# #             "price": str(obj.package.price)
# #         }

# # class NotificationSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Notification
# #         fields = ('id','message','is_read','created_at')

# # class BookingSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Booking
# #         fields = '__all__'
# #         read_only_fields = ('user', 'status', 'payment_status')



# from rest_framework import serializers
# from .models import Booking, Notification
# from services.models import Service, Package
# import os

# ALLOWED_CONTENT_TYPES = [
#     'application/pdf',
#     'image/jpeg',
#     'image/png',
#     'image/gif',
#     'image/webp',
# ]


# class BookingCreateSerializer(serializers.ModelSerializer):
#     # Allow package id as optional (frontend sends package id)
#     package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False, allow_null=True)

#     # file upload field (required)
#     proof_document = serializers.FileField(write_only=True, required=True)

#     class Meta:
#         model = Booking
#         fields = [
#             "id", "user", "service", "package",
#             "given_name", "surname", "other_names",
#             "contact_number", "email", "full_contact_address",
#             "num_adults", "num_children", "start_date", "end_date", "notes",
#             "is_tnc_accepted", "status", "created_at", "proof_document",
#         ]
#         read_only_fields = ("id", "status", "created_at", "user")

#     def validate(self, attrs):
#         # ensure terms accepted
#         if not attrs.get("is_tnc_accepted", False):
#             raise serializers.ValidationError("Tourist must accept terms and conditions.")

#         service = attrs.get("service")
#         package = attrs.get("package")
#         if package and package.service_id != service.id:
#             raise serializers.ValidationError("Selected package does not belong to the chosen service.")

#         # proof_document presence validated by required=True; now validate type
#         proof = attrs.get('proof_document')
#         if not proof:
#             raise serializers.ValidationError({"proof_document": "This file is required."})

#         content_type = getattr(proof, 'content_type', None)
#         # some WSGI setups might not set content_type; fall back to extension check
#         if content_type:
#             if content_type not in ALLOWED_CONTENT_TYPES:
#                 raise serializers.ValidationError({"proof_document": "Unsupported file type. Upload a PDF or image."})
#         else:
#             # fallback: check file extension
#             ext = os.path.splitext(proof.name)[1].lower()
#             if ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp']:
#                 raise serializers.ValidationError({"proof_document": "Unsupported file extension. Use PDF or image."})

#         return attrs

#     def create(self, validated_data):
#         proof = validated_data.pop('proof_document', None)
#         # user is set in view.perform_create
#         booking = Booking.objects.create(**validated_data)
#         if proof:
#             booking.proof_document.save(proof.name, proof, save=True)
#         return booking


# class BookingDetailSerializer(serializers.ModelSerializer):
#     package = serializers.SerializerMethodField()
#     service = serializers.StringRelatedField()

#     class Meta:
#         model = Booking
#         fields = "__all__"

#     def get_package(self, obj):
#         if not obj.package:
#             return None
#         return {
#             "id": obj.package.id,
#             "name": obj.package.name,
#             "price": str(obj.package.price)
#         }


# class NotificationSerializer(serializers.ModelSerializer):
#     recipient = serializers.SerializerMethodField()

#     class Meta:
#         model = Notification
#         fields = ('id', 'recipient', 'message', 'is_read', 'created_at')

#     def get_recipient(self, obj):
#         # return minimal recipient info or None for global/admin messages
#         if obj.recipient is None:
#             return None
#         return {
#             "id": obj.recipient.id,
#             "username": getattr(obj.recipient, "username", None),
#             "email": getattr(obj.recipient, "email", None)
#         }



# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'
#         read_only_fields = ('user', 'status', 'payment_status')

from rest_framework import serializers
from .models import Booking, Notification
from services.models import Package, Service


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing bookings.
    Includes full personal details + package + service.
    """

    service_title = serializers.CharField(source="service.title", read_only=True)
    package_name = serializers.CharField(source="package.name", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "service",
            "service_title",
            "package",
            "package_name",

            # Personal details
            "given_name",
            "surname",
            "other_names",
            "contact_number",
            "email",
            "full_contact_address",

            # Travelers
            "num_adults",
            "num_children",

            # Trip dates
            "start_date",
            "end_date",

            # Notes
            "notes",
            "admin_note",

            # Status + Payment
            "status",
            "payment_status",

            # Timestamps
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "status",
            "payment_status",
            "created_at",
            "updated_at",
            "admin_note",
            "user",
        )

    # ============================================
    # VALIDATION
    # ============================================

    def validate(self, attrs):
        service = attrs.get("service") or self.instance.service
        package = attrs.get("package")

        # Make sure the package belongs to the service
        if package and package.service_id != service.id:
            raise serializers.ValidationError(
                {"package": "This package does not belong to the selected service."}
            )

        # Dates validation
        start = attrs.get("start_date")
        end = attrs.get("end_date")

        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        return attrs

    def create(self, validated_data):
        """Attach the requesting user automatically."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user

        return super().create(validated_data)


# ======================================================
# NOTIFICATIONS
# ======================================================

class NotificationSerializer(serializers.ModelSerializer):
    recipient_username = serializers.CharField(source="recipient.username", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "recipient_username",
            "message",
            "is_read",
            "created_at",
        ]
        read_only_fields = ("created_at",)
