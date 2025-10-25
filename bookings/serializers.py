from rest_framework import serializers
from .models import Booking, Notification
from services.models import Service, Package

class BookingCreateSerializer(serializers.ModelSerializer):
    # Allow package id as optional (frontend sends package id)
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Booking
        fields = [
            "id", "user", "service", "package",
            "given_name", "surname", "other_names",
            "contact_number", "email", "full_contact_address",
            "num_adults", "num_children", "start_date", "end_date", "notes",
            "is_tnc_accepted", "status", "created_at",
        ]
        read_only_fields = ("id", "status", "created_at", "user")

    def validate(self, attrs):
        # ensure terms accepted
        if not attrs.get("is_tnc_accepted", False):
            raise serializers.ValidationError("Tourist must accept terms and conditions.")
        # ensure service exists (DRF will handle based on PK)
        service = attrs.get("service")
        package = attrs.get("package")
        if package and package.service_id != service.id:
            raise serializers.ValidationError("Selected package does not belong to the chosen service.")
        return attrs

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
    class Meta:
        model = Notification
        fields = ('id','message','is_read','created_at')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'status', 'payment_status')
