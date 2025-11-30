# from rest_framework import serializers
# from .models import Transaction, Payment


# class TransactionSerializer(serializers.ModelSerializer):
#     """
#     Read-only serializer for viewing transaction details via API endpoints.
#     Does not allow unsafe writes — transactions are only modified through
#     redirect, webhook, and internal verification logic.
#     """

#     class Meta:
#         model = Transaction
#         fields = [
#             "id",
#             "reference",
#             "booking",
#             "provider",
#             "amount",
#             "status",
#             "created_at",
#             "updated_at",
#             "meta",
#         ]
#         read_only_fields = fields  # no editing through serializer


# class PaymentSerializer(serializers.ModelSerializer):
#     """
#     Read-only serializer for exposing final payment details.
#     """

#     class Meta:
#         model = Payment
#         fields = [
#             "booking",
#             "reference",
#             "amount",
#             "provider",
#             "status",
#             "paid_at",
#         ]
#         read_only_fields = fields


# class VerifyTransactionInputSerializer(serializers.Serializer):
#     """
#     Optional serializer for a manual verification endpoint such as:
#     POST /api/payments/verify/manual/

#     Useful for debugging:
#         - {"tx_ref": "ALC-12345"}
#     """
#     tx_ref = serializers.CharField(required=True)

# class BankTransferUploadSerializer(serializers.ModelSerializer):
#     """
#     Serializer used when uploading bank transfer receipts.
#     Only updates the receipt image + optional fields.
#     """
#     class Meta:
#         model = Transaction
#         fields = ["receipt_image"]
#         extra_kwargs = {
#             "receipt_image": {"required": True}
#         }

#     def validate_receipt_image(self, value):
#         if not value:
#             raise serializers.ValidationError("A receipt image is required.")
#         return value

from rest_framework import serializers
from .models import Transaction, Payment
from bookings.models import Booking


# ---------------------------------------------------------
# PAYMENT INITIATION SERIALIZER
# ---------------------------------------------------------
class PaymentInitiateSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    provider = serializers.ChoiceField(
        choices=[
            ("flutterwave", "Flutterwave"),
            ("interswitch", "Interswitch"),
            ("bank_transfer", "Bank Transfer"),
        ]
    )

    def validate_booking_id(self, value):
        if not Booking.objects.filter(id=value).exists():
            raise serializers.ValidationError("Booking does not exist.")
        return value


# ---------------------------------------------------------
# TRANSACTION SERIALIZER
# ---------------------------------------------------------
class TransactionSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = Transaction
        fields = [
            "id",
            "reference",
            "booking",
            "provider",
            "amount",
            "status",
            "flutterwave_id",
            "created_at",
            "updated_at",
            "meta",
        ]
        read_only_fields = ["status", "created_at", "updated_at"]


# ---------------------------------------------------------
# PAYMENT SERIALIZER
# ---------------------------------------------------------
class PaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "booking",
            "reference",
            "amount",
            "provider",
            "status",
            "paid_at",
        ]
        read_only_fields = [
            "booking",
            "paid_at",
            "status",
        ]
