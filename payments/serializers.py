# from rest_framework import serializers
# from .models import Payment, Transaction

# class TransactionInitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ("id", "booking", "provider", "amount")

# class BankTransferUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ("id", "booking", "provider", "amount", "receipt")
#         read_only_fields = ("provider",)

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'
#         read_only_fields = ('status',)

from rest_framework import serializers
from .models import Payment, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class BankTransferUploadSerializer(serializers.ModelSerializer):
    """
    Handles file uploads for manual bank transfer receipts.
    """
    class Meta:
        model = Transaction
        fields = ['id', 'receipt', 'status']
        read_only_fields = ['status']