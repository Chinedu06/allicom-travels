# from rest_framework import serializers
# from .models import Booking, Notification
# from services.models import Service, Package

# class BookingCreateSerializer(serializers.ModelSerializer):
#     # Allow package id as optional (frontend sends package id)
#     package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False, allow_null=True)

#     class Meta:
#         model = Booking
#         fields = [
#             "id", "user", "service", "package",
#             "given_name", "surname", "other_names",
#             "contact_number", "email", "full_contact_address",
#             "num_adults", "num_children", "start_date", "end_date", "notes",
#             "is_tnc_accepted", "status", "created_at",
#         ]
#         read_only_fields = ("id", "status", "created_at", "user")

#     def validate(self, attrs):
#         # ensure terms accepted
#         if not attrs.get("is_tnc_accepted", False):
#             raise serializers.ValidationError("Tourist must accept terms and conditions.")
#         # ensure service exists (DRF will handle based on PK)
#         service = attrs.get("service")
#         package = attrs.get("package")
#         if package and package.service_id != service.id:
#             raise serializers.ValidationError("Selected package does not belong to the chosen service.")
#         return attrs

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
#     class Meta:
#         model = Notification
#         fields = ('id','message','is_read','created_at')

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'
#         read_only_fields = ('user', 'status', 'payment_status')



from rest_framework import serializers
from .models import Booking, Notification
from services.models import Service, Package
import os

ALLOWED_CONTENT_TYPES = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
]


class BookingCreateSerializer(serializers.ModelSerializer):
    # Allow package id as optional (frontend sends package id)
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False, allow_null=True)

    # file upload field (required)
    proof_document = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = Booking
        fields = [
            "id", "user", "service", "package",
            "given_name", "surname", "other_names",
            "contact_number", "email", "full_contact_address",
            "num_adults", "num_children", "start_date", "end_date", "notes",
            "is_tnc_accepted", "status", "created_at", "proof_document",
        ]
        read_only_fields = ("id", "status", "created_at", "user")

    def validate(self, attrs):
        # ensure terms accepted
        if not attrs.get("is_tnc_accepted", False):
            raise serializers.ValidationError("Tourist must accept terms and conditions.")

        service = attrs.get("service")
        package = attrs.get("package")
        if package and package.service_id != service.id:
            raise serializers.ValidationError("Selected package does not belong to the chosen service.")

        # proof_document presence validated by required=True; now validate type
        proof = attrs.get('proof_document')
        if not proof:
            raise serializers.ValidationError({"proof_document": "This file is required."})

        content_type = getattr(proof, 'content_type', None)
        # some WSGI setups might not set content_type; fall back to extension check
        if content_type:
            if content_type not in ALLOWED_CONTENT_TYPES:
                raise serializers.ValidationError({"proof_document": "Unsupported file type. Upload a PDF or image."})
        else:
            # fallback: check file extension
            ext = os.path.splitext(proof.name)[1].lower()
            if ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp']:
                raise serializers.ValidationError({"proof_document": "Unsupported file extension. Use PDF or image."})

        return attrs

    def create(self, validated_data):
        proof = validated_data.pop('proof_document', None)
        # user is set in view.perform_create
        booking = Booking.objects.create(**validated_data)
        if proof:
            booking.proof_document.save(proof.name, proof, save=True)
        return booking


class BookingDetailSerializer(serializers.ModelSerializer):
    package = serializers.SerializerMethodField()
    service = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = "__all__"

    def get_package(self, obj):
        if not obj.package:
            return None
        return {
            "id": obj.package.id,
            "name": obj.package.name,
            "price": str(obj.package.price)
        }


class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'message', 'is_read', 'created_at')

    def get_recipient(self, obj):
        # return minimal recipient info or None for global/admin messages
        if obj.recipient is None:
            return None
        return {
            "id": obj.recipient.id,
            "username": getattr(obj.recipient, "username", None),
            "email": getattr(obj.recipient, "email", None)
        }



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'status', 'payment_status')