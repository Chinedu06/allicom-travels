# # from django.shortcuts import render

# # # payments/views.py
# # from rest_framework import generics, status, permissions
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view, permission_classes
# # from .models import Transaction
# # from .serializers import PaymentSerializer, TransactionInitSerializer, BankTransferUploadSerializer
# # from bookings.models import Booking
# # from rest_framework.permissions import IsAuthenticated


# # @api_view(['POST'])
# # @permission_classes([permissions.AllowAny])
# # def initiate_payment(request):
# #     """
# #     Request body:
# #       { "booking": <booking_id>, "provider": "flutterwave"|"interswitch"|"bank_transfer" }
# #     Returns: for gateways -> payment_url to redirect tourist; for bank -> transaction id to upload receipt.
# #     """
# #     data = request.data
# #     booking_id = data.get('booking')
# #     provider = data.get('provider')
# #     booking = Booking.objects.get(pk=booking_id)

# #     # calculate amount from booking
# #     amount = booking.total_price

# #     txn = Transaction.objects.create(booking=booking, provider=provider, amount=amount, status=Transaction.STATUS_INIT)

# #     if provider in [Transaction.PROVIDER_FLUTTERWAVE, Transaction.PROVIDER_INTERSWITCH]:
# #         # TODO: integrate real API calls. For now, return a mock payment_url and provider_reference placeholder.
# #         provider_reference = f"{provider.upper()}-MOCK-{txn.pk}"
# #         txn.provider_reference = provider_reference
# #         txn.save()
# #         payment_url = f"https://pay.mock/{provider}/{provider_reference}"  # frontend will redirect tourist here
# #         return Response({"payment_url": payment_url, "transaction_id": txn.id, "provider_reference": provider_reference})
# #     else:
# #         # bank_transfer: front-end should upload receipt to /payments/upload-receipt/
# #         txn.status = Transaction.STATUS_PENDING
# #         txn.save()
# #         return Response({"transaction_id": txn.id, "detail":"Upload bank receipt to /payments/upload-receipt/ using this transaction_id."})

# # @api_view(['POST'])
# # @permission_classes([permissions.AllowAny])
# # def mock_verify_payment(request):
# #     """
# #     This endpoint simulates webhook/verification from gateway.
# #     In production you should implement real webhook handling.
# #     Body example: { "transaction_id": 5, "status": "success", "provider_reference": "..." }
# #     """
# #     txid = request.data.get('transaction_id')
# #     status_str = request.data.get('status')  # expected 'success' or 'failed'
# #     provider_ref = request.data.get('provider_reference', '')
# #     txn = Transaction.objects.get(pk=txid)
# #     if status_str == 'success':
# #         txn.status = Transaction.STATUS_SUCCESS
# #         txn.provider_reference = provider_ref
# #         txn.save()
# #         # update booking
# #         booking = txn.booking
# #         booking.status = Booking.STATUS_PAID
# #         # auto-confirm bookings paid by gateways
# #         booking.status = Booking.STATUS_CONFIRMED
# #         booking.save()
# #         return Response({"detail":"verified and booking confirmed"})
# #     else:
# #         txn.status = Transaction.STATUS_FAILED
# #         txn.save()
# #         return Response({"detail":"marked failed"}, status=status.HTTP_400_BAD_REQUEST)

# # @api_view(['POST'])
# # @permission_classes([permissions.IsAuthenticated])
# # def upload_bank_receipt(request):
# #     """
# #     Operator / tourist (or anonymous) posts transaction_id and a file under 'receipt'.
# #     Admin will later inspect/confirm and then change Transaction.status to success and Booking to confirmed.
# #     """
# #     txid = request.data.get('transaction_id')
# #     txn = Transaction.objects.get(pk=txid)
# #     serializer = BankTransferUploadSerializer(txn, data=request.data, partial=True)
# #     if serializer.is_valid():
# #         serializer.save(provider=Transaction.PROVIDER_BANK, status=Transaction.STATUS_PENDING)
# #         return Response({"detail":"receipt uploaded, admin will verify."})
# #     return Response(serializer.errors, status=400)

# # class PaymentCreateView(generics.CreateAPIView):
# #     serializer_class = PaymentSerializer
# #     permission_classes = [IsAuthenticated]

# #     def perform_create(self, serializer):
# #         payment = serializer.save()
# #         booking = payment.bookingg

# #         if payment.provider in ['flutterwave', 'interswitch']:
# #             booking.status = 'confirmed'
# #             booking.payment_status = 'paid'
# #         elif payment.provider == 'bank_transfer':
# #             booking.payment_status = 'pending_verification'
# #         booking.save()

# from django.shortcuts import render

# # payments/views.py
# from rest_framework import generics, status, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from .models import Transaction
# from .serializers import PaymentSerializer, TransactionInitSerializer, BankTransferUploadSerializer
# from bookings.models import Booking
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets, status, generics
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Transaction, Payment
# from .serializers import TransactionSerializer, PaymentSerializer


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def initiate_payment(request):
#     """
#     Request body:
#       { "booking": <booking_id>, "provider": "flutterwave"|"interswitch"|"bank_transfer" }
#     Returns: for gateways -> payment_url to redirect tourist; for bank -> transaction id to upload receipt.
#     """
#     data = request.data
#     booking_id = data.get('booking')
#     provider = data.get('provider')
#     booking = Booking.objects.get(pk=booking_id)

#     # calculate amount from booking
#     amount = booking.total_price

#     txn = Transaction.objects.create(booking=booking, provider=provider, amount=amount, status=Transaction.STATUS_INIT)

#     if provider in [Transaction.PROVIDER_FLUTTERWAVE, Transaction.PROVIDER_INTERSWITCH]:
#         # TODO: integrate real API calls. For now, return a mock payment_url and provider_reference placeholder.
#         provider_reference = f"{provider.upper()}-MOCK-{txn.pk}"
#         txn.provider_reference = provider_reference
#         txn.save()
#         payment_url = f"https://pay.mock/{provider}/{provider_reference}"  # frontend will redirect tourist here
#         return Response({"payment_url": payment_url, "transaction_id": txn.id, "provider_reference": provider_reference})
#     else:
#         # bank_transfer: front-end should upload receipt to /payments/upload-receipt/
#         txn.status = Transaction.STATUS_PENDING
#         txn.save()
#         return Response({"transaction_id": txn.id, "detail":"Upload bank receipt to /payments/upload-receipt/ using this transaction_id."})


# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def mock_verify_payment(request):
#     """
#     This endpoint simulates webhook/verification from gateway.
#     In production you should implement real webhook handling.
#     Body example: { "transaction_id": 5, "status": "success", "provider_reference": "..." }
#     """
#     txid = request.data.get('transaction_id')
#     status_str = request.data.get('status')  # expected 'success' or 'failed'
#     provider_ref = request.data.get('provider_reference', '')
#     txn = Transaction.objects.get(pk=txid)
#     if status_str == 'success':
#         txn.status = Transaction.STATUS_SUCCESS
#         txn.provider_reference = provider_ref
#         txn.save()
#         # update booking
#         booking = txn.booking
#         booking.status = Booking.STATUS_PAID
#         # auto-confirm bookings paid by gateways
#         booking.status = Booking.STATUS_CONFIRMED
#         booking.save()
#         return Response({"detail":"verified and booking confirmed"})
#     else:
#         txn.status = Transaction.STATUS_FAILED
#         txn.save()
#         return Response({"detail":"marked failed"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def upload_bank_receipt(request):
#     """
#     Operator / tourist (or anonymous) posts transaction_id and a file under 'receipt'.
#     Admin will later inspect/confirm and then change Transaction.status to success and Booking to confirmed.
#     """
#     txid = request.data.get('transaction_id')
#     txn = Transaction.objects.get(pk=txid)
#     serializer = BankTransferUploadSerializer(txn, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save(provider=Transaction.PROVIDER_BANK, status=Transaction.STATUS_PENDING)
#         return Response({"detail":"receipt uploaded, admin will verify."})
#     return Response(serializer.errors, status=400)


# class PaymentCreateView(generics.CreateAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         payment = serializer.save()
#         booking = payment.booking

#         if payment.provider in ['flutterwave', 'interswitch']:
#             booking.status = 'confirmed'
#             booking.payment_status = 'paid'
#         elif payment.provider == 'bank_transfer':
#             booking.payment_status = 'pending_verification'
#         booking.save()


# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     @action(detail=True, methods=['post'])
#     def verify(self, request, pk=None):
#         """
#         Simulates verifying a transaction (e.g., Flutterwave webhook or manual check).
#         """
#         transaction = self.get_object()

#         # In production, call gateway verification here.
#         transaction.mark_successful()

#         return Response({
#             'message': 'Transaction verified successfully.',
#             'transaction': TransactionSerializer(transaction).data,
#             'payment': PaymentSerializer(transaction.booking.payment).data,
#         }, status=status.HTTP_200_OK)


# class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

from rest_framework import generics, viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from .models import Transaction, Payment
from .serializers import (
    PaymentSerializer,
    TransactionSerializer,
    BankTransferUploadSerializer,
)
from bookings.models import Booking


# -------------------------------
#  Functional API Views
# -------------------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def initiate_payment(request):
    """
    Creates a new transaction record and returns payment initiation details.
    """
    data = request.data
    booking_id = data.get("booking")
    provider = data.get("provider")

    booking = Booking.objects.get(pk=booking_id)
    amount = booking.total_price

    txn = Transaction.objects.create(
        booking=booking, provider=provider, amount=amount, status=Transaction.STATUS_INIT
    )

    if provider in [
        Transaction.PROVIDER_FLUTTERWAVE,
        Transaction.PROVIDER_INTERSWITCH,
    ]:
        provider_reference = f"{provider.upper()}-MOCK-{txn.pk}"
        txn.provider_reference = provider_reference
        txn.save()
        payment_url = f"https://pay.mock/{provider}/{provider_reference}"
        return Response(
            {
                "payment_url": payment_url,
                "transaction_id": txn.id,
                "provider_reference": provider_reference,
            }
        )
    else:
        txn.status = Transaction.STATUS_PENDING
        txn.save()
        return Response(
            {
                "transaction_id": txn.id,
                "detail": "Upload bank receipt to /payments/upload-receipt/ using this transaction_id.",
            }
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def mock_verify_payment(request):
    """
    Simulates a payment verification or webhook callback.
    """
    txid = request.data.get("transaction_id")
    status_str = request.data.get("status")
    provider_ref = request.data.get("provider_reference", "")

    txn = Transaction.objects.get(pk=txid)

    if status_str == "success":
        txn.status = Transaction.STATUS_SUCCESS
        txn.provider_reference = provider_ref
        txn.save()

        booking = txn.booking
        booking.status = Booking.STATUS_CONFIRMED
        booking.save()

        return Response({"detail": "verified and booking confirmed"})
    else:
        txn.status = Transaction.STATUS_FAILED
        txn.save()
        return Response({"detail": "marked failed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def upload_bank_receipt(request):
    """
    Uploads a bank transfer receipt for manual verification.
    """
    txid = request.data.get("transaction_id")
    txn = Transaction.objects.get(pk=txid)
    serializer = BankTransferUploadSerializer(txn, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(provider=Transaction.PROVIDER_BANK, status=Transaction.STATUS_PENDING)
        return Response({"detail": "receipt uploaded, admin will verify."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
#  Class-based API Views
# -------------------------------
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        booking = payment.booking

        if payment.provider in ["flutterwave", "interswitch"]:
            booking.status = Booking.STATUS_CONFIRMED
            booking.payment_status = "paid"
        elif payment.provider == "bank_transfer":
            booking.payment_status = "pending_verification"
        booking.save()


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        transaction = self.get_object()
        transaction.mark_successful()

        return Response(
            {
                "message": "Transaction verified successfully.",
                "transaction": TransactionSerializer(transaction).data,
                "payment": PaymentSerializer(transaction.booking.payment).data,
            },
            status=status.HTTP_200_OK,
        )


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# payments/views.py (webhook verify section)
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def gateway_webhook_verify(request):
    """
    Generic webhook endpoint for gateways (mock).
    Expects body with:
      { "provider": "flutterwave"|"interswitch", "provider_reference": "<ref>", "status": "success"|"failed", "transaction_reference": "<our_tx_ref or provider_ref>" }

    Idempotency: if a Transaction exists with provider_reference, reuse it. If multiple webhook calls come,
    state transitions are safe (only move to success once).
    """
    data = request.data
    provider = data.get('provider')
    provider_reference = data.get('provider_reference')
    status_str = data.get('status')

    if not provider_reference:
        return Response({"detail": "provider_reference required"}, status=status.HTTP_400_BAD_REQUEST)

    # Try to find transaction by provider_reference first
    try:
        txn = Transaction.objects.filter(provider=provider, provider_reference=provider_reference).first()
    except Exception as e:
        logger.exception("Error querying transaction by provider_reference")
        txn = None

    if not txn:
        # fallback: maybe provider posted our local transaction reference
        our_ref = data.get('transaction_reference')
        if our_ref:
            txn = Transaction.objects.filter(reference=our_ref).first()

    if not txn:
        logger.warning("Webhook for unknown transaction provider_reference=%s provider=%s", provider_reference, provider)
        return Response({"detail": "transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    # idempotent status update
    if status_str == 'success':
        if txn.status != Transaction.STATUS_SUCCESS:
            txn.status = Transaction.STATUS_SUCCESS
            txn.provider_reference = provider_reference
            txn.save()
            # mark_successful handles syncing and notification
            try:
                txn.mark_successful()
            except Exception:
                logger.exception("Error in txn.mark_successful")
        else:
            logger.info("Webhook received for already-successful txn %s", txn.reference)

        return Response({"detail":"verified and booking confirmed"}, status=status.HTTP_200_OK)
    else:
        # failed
        txn.status = Transaction.STATUS_FAILED
        txn.save()
        return Response({"detail":"marked failed"}, status=status.HTTP_200_OK)
