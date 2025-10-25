# from django.urls import path
# from .views import PaymentCreateView, initiate_payment, mock_verify_payment, upload_bank_receipt

# urlpatterns = [
#     path("initiate/", initiate_payment, name="initiate-payment"),
#     path("verify/", mock_verify_payment, name="verify-payment"),      # webhook / test verify
#     path("upload-receipt/", upload_bank_receipt, name="upload-receipt"),
#     path('create/', PaymentCreateView.as_view(), name='create-payment'),

# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentCreateView,
    gateway_webhook_verify,
    initiate_payment,
    mock_verify_payment,
    upload_bank_receipt,
    TransactionViewSet,
    PaymentViewSet,
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path("initiate/", initiate_payment, name="initiate-payment"),
    path("verify/", mock_verify_payment, name="verify-payment"),
    path("upload-receipt/", upload_bank_receipt, name="upload-receipt"),
    path("create/", PaymentCreateView.as_view(), name="create-payment"),
    path("", include(router.urls)),
    # payments/urls.py (add to urlpatterns)
    path("webhook/", gateway_webhook_verify, name="gateway-webhook"),
]
