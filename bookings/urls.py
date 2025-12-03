# # # # from os import path
# # # # from rest_framework.routers import DefaultRouter
# # # # from .views import BookingCreateView, BookingViewSet

# # # # router = DefaultRouter()
# # # # router.register(r'bookings', BookingViewSet, basename='bookings')

# # # # urlpatterns = router.urls

# # # # urlpatterns = [
# # # #     path('create/', BookingCreateView.as_view(), name='create-booking'),
# # # # ]

# # # from django.urls import path
# # # from rest_framework.routers import DefaultRouter
# # # from .views import BookingCreateView, BookingViewSet

# # # router = DefaultRouter()
# # # router.register(r'bookings', BookingViewSet, basename='bookings')

# # # # combine router urls with any manual endpoints
# # # urlpatterns = router.urls + [
# # #     path('create/', BookingCreateView.as_view(), name='create-booking'),
# # # ]

# # from django.urls import path
# # from rest_framework.routers import DefaultRouter
# # from .views import BookingCreateView, BookingViewSet, BookingListView, BookingDetailView

# # from django.http import JsonResponse
# # from rest_framework.views import APIView

# # router = DefaultRouter()
# # router.register(r'', BookingViewSet, basename='bookings')  # registers / (list, detail) under api/bookings/

# # urlpatterns = router.urls + [
# #     # explicit create endpoint => /api/bookings/create/
# #     path('create/', BookingCreateView.as_view(), name='booking-create'),

# #     # optional explicit list/detail shortcuts (alias for router if needed)
# #     path('list/', BookingListView.as_view(), name='booking-list'),
# #     path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
# # ]

# # class BookingDetailView(APIView):
# #     def get(self, request, pk=None):
# #         return JsonResponse({"message": f"Booking detail endpoint for booking ID {pk} - coming soon"})

# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from .views import (
#     BookingCreateView,
#     BookingViewSet,
#     BookingListView,
#     BookingDetailView,
#     NotificationListView,
# )

# router = DefaultRouter()
# router.register(r'', BookingViewSet, basename='bookings')

# urlpatterns = router.urls + [
#     path('create/', BookingCreateView.as_view(), name='booking-create'),
#     path('list/', BookingListView.as_view(), name='booking-list'),
#     path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
#     path('notifications/', NotificationListView.as_view(), name='booking-notifications'),
# ]

from django.urls import path
from .views import (
    CreateBookingView,
    MyBookingsView,
    AllBookingsView,
    UpdateBookingStatusView,
    MyNotificationsView,
    MarkNotificationReadView,
)

app_name = "bookings"


urlpatterns = [
    # -------------------------------
    # BOOKINGS
    # -------------------------------
    path("create/", CreateBookingView.as_view(), name="booking-create"),
    path("mine/", MyBookingsView.as_view(), name="booking-my-list"),
    path("all/", AllBookingsView.as_view(), name="booking-all"),  # admin only
    path("<int:booking_id>/status/", UpdateBookingStatusView.as_view(), name="booking-update-status"),

    # -------------------------------
    # NOTIFICATIONS
    # -------------------------------
    path("notifications/", MyNotificationsView.as_view(), name="notifications-list"),
    path("notifications/<int:notif_id>/read/", MarkNotificationReadView.as_view(), name="notification-read"),
]
