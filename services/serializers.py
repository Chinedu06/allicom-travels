# from rest_framework import serializers
# from .models import Service, ServiceImage, Package

# class ServiceImageSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = ServiceImage
#         fields = ("id", "image", "uploaded_at")
#         read_only_fields = ("id", "uploaded_at")


# class PackageSerializer(serializers.ModelSerializer):
#     """
#     Serializer for packages. Used for create/update by operators and for public read.
#     """
#     service = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Package
#         fields = (
#             "id", "service", "name", "description", "price",
#             "duration_days", "max_people", "is_active",
#             "created_at", "updated_at"
#         )
#         read_only_fields = ("id", "created_at", "updated_at")


# class ServiceListSerializer(serializers.ModelSerializer):
#     """Lightweight serializer for list endpoints (for tourists/public)."""
#     operator = serializers.StringRelatedField(read_only=True)
#     images = ServiceImageSerializer(many=True, read_only=True)
#     # Optionally display packages in list view (lightweight)
#     packages = PackageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Service
#         fields = (
#             "id", "title", "category", "city", "country", "price",
#             "min_age", "available_days", "is_approved", "images", "operator", "packages",
#         )
#         read_only_fields = ("is_approved", "operator", "images", "packages")


# class ServiceDetailSerializer(serializers.ModelSerializer):
#     operator = serializers.StringRelatedField(read_only=True)
#     images = ServiceImageSerializer(many=True, read_only=True)
#     packages = PackageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Service
#         # Explicitly list fields rather than __all__ to be clear what frontend expects
#         fields = (
#             "id", "operator", "category", "title", "description", "city", "country",
#             "duration_hours", "price", "min_age", "available_days",
#             "is_active", "is_approved", "created_at", "updated_at",
#             "images", "packages",
#         )
#         read_only_fields = ("operator", "is_approved", "created_at", "updated_at", "images", "packages")


# class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
#     """
#     Used for create and update by authenticated operators.
#     Accepts 'images' via files when using multipart/form-data. Images are handled in perform_create/perform_update.
#     """
#     images = ServiceImageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Service
#         # don't allow client to set is_approved or operator
#         exclude = ("is_approved", "created_at", "updated_at")

#     def validate_available_days(self, value):
#         """
#         Ensure available_days list items are valid weekday values (if provided).
#         """
#         if not isinstance(value, (list, tuple)):
#             raise serializers.ValidationError("available_days must be a list.")
#         valid = {d[0] for d in Service.WEEKDAYS}
#         for v in value:
#             if v not in valid:
#                 raise serializers.ValidationError(f"Invalid weekday: {v}")
#         return list(value)

from rest_framework import serializers
from .models import Service, Package


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "id",
            "title",
            "description",
            "price",
            "duration",
            "features",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image",
            "is_active",
            "packages",
        ]
