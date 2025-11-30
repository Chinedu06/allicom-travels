# # # # payments/urls.py

# # # from django.urls import path, include
# # # from rest_framework.routers import DefaultRouter

# # # from .views import (
# # #     initiate_payment,
# # #     upload_bank_receipt,
# # #     flutterwave_redirect_view,
# # #     flutterwave_webhook_view,
# # #     TransactionViewSet,
# # #     PaymentViewSet,
# # #     PaymentCreateView,
# # # )

# # # router = DefaultRouter()
# # # router.register(r"transactions", TransactionViewSet, basename="transaction")
# # # router.register(r"payments", PaymentViewSet, basename="payment")

# # # urlpatterns = [
# # #     # --- INITIATE PAYMENT ---
# # #     path("initiate/", initiate_payment, name="initiate-payment"),

# # #     # --- BANK RECEIPT UPLOAD ---
# # #     path("upload-receipt/", upload_bank_receipt, name="upload-bank-receipt"),

# # #     # --- USER REDIRECT AFTER PAYMENT ---
# # #     path("redirect/", flutterwave_redirect_view, name="flutterwave-redirect"),

# # #     # --- FLUTTERWAVE WEBHOOK (server -> server) ---
# # #     path("webhook/", flutterwave_webhook_view, name="flutterwave-webhook"),

# # #     # --- PAYMENT CREATION (existing API) ---
# # #     path("create/", PaymentCreateView.as_view(), name="create-payment"),

# # #     # --- VIEWSETS ---
# # #     path("", include(router.urls)),
# # # ]

# # # payments/urls.py
# # from django.urls import path
# # from payments import views

# # urlpatterns = [
# #     path(
# #         "flutterwave/initiate/<int:booking_id>/",
# #         views.initiate_flutterwave_payment,
# #         name="initiate-flutterwave"
# #     ),

# #     path(
# #         "flutterwave/callback/",
# #         views.flutterwave_callback,
# #         name="flutterwave-callback"
# #     ),

# #     path(
# #         "flutterwave/verify/<str:tx_ref>/",
# #         views.verify_flutterwave,
# #         name="verify-flutterwave"
# #     ),

# #     path(
# #         "flutterwave/webhook/",
# #         views.flutterwave_webhook,
# #         name="flutterwave-webhook"
# #     ),
# # ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# from .views import (
#     initiate_payment,
#     gateway_webhook_verify,
#     upload_bank_receipt,
#     TransactionViewSet,
#     PaymentViewSet,
# )

# router = DefaultRouter()
# router.register(r"transactions", TransactionViewSet, basename="transactions")
# router.register(r"payments", PaymentViewSet, basename="payments")

# urlpatterns = [
#     path("initiate/", initiate_payment, name="initiate-payment"),
#     path("webhook/", gateway_webhook_verify, name="payment-webhook"),
#     path("upload-receipt/", upload_bank_receipt, name="bank-upload"),
#     path("", include(router.urls)),
# ]

from django.urls import path
from . import views

urlpatterns = [
    # 1) Initialize Payment
    path("init/<int:booking_id>/", views.initialize_payment, name="initialize_payment"),

    # 2) Flutterwave redirect/pages
    path("success/", views.payment_success, name="payment_success"),
    path("cancelled/", views.payment_cancelled, name="payment_cancelled"),

    # 3) Flutterwave webhook
    path("webhook/", views.flutterwave_webhook, name="flutterwave_webhook"),

    # 4) Optional status checker
    path("status/<str:reference>/", views.check_payment_status, name="check_payment_status"),
]
