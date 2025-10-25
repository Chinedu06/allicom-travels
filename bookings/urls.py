# from os import path
# from rest_framework.routers import DefaultRouter
# from .views import BookingCreateView, BookingViewSet

# router = DefaultRouter()
# router.register(r'bookings', BookingViewSet, basename='bookings')

# urlpatterns = router.urls

# urlpatterns = [
#     path('create/', BookingCreateView.as_view(), name='create-booking'),
# ]

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookingCreateView, BookingViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')

# combine router urls with any manual endpoints
urlpatterns = router.urls + [
    path('create/', BookingCreateView.as_view(), name='create-booking'),
]
