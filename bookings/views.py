# from rest_framework import viewsets, permissions, status, generics
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import Booking
# from .serializers import BookingCreateSerializer, BookingDetailSerializer, BookingSerializer, NotificationSerializer
# from .permissions import IsBookingOwnerOrOperatorOrAdmin
# from services.models import Service
# from .models import Notification
# from rest_framework.permissions import IsAuthenticated



# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all().order_by("-created_at")
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsBookingOwnerOrOperatorOrAdmin]

#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return BookingCreateSerializer
#         return BookingDetailSerializer

#     def perform_create(self, serializer):
#         # attach user if authenticated
#         user = self.request.user if self.request.user.is_authenticated else None
#         # default status pending
#         serializer.save(user=user, status=Booking.STATUS_PENDING)

#     def get_queryset(self):
#         user = self.request.user
#         # public listing: none (tourists shouldn't see all bookings). Only admin, operator and owners have listings.
#         if user.is_authenticated:
#             # admin: all bookings
#             if user.is_staff or user.is_superuser:
#                 return Booking.objects.all().order_by("-created_at")
#             # operator: bookings for operator's services
#             if getattr(user, "role", None) == "operator":
#                 return Booking.objects.filter(service__operator=user).order_by("-created_at")
#             # normal user: their bookings
#             return Booking.objects.filter(user=user).order_by("-created_at")
#         # anonymous: no list
#         return Booking.objects.none()

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
#     def approve(self, request, pk=None):
#         booking = self.get_object()
#         booking.status = Booking.STATUS_CONFIRMED
#         booking.admin_note = request.data.get('admin_note', '')
#         booking.save()
#         # create notifications via signals (we'll implement)
#         return Response({"detail":"Booking confirmed"}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
#     def reject(self, request, pk=None):
#         booking = self.get_object()
#         booking.status = Booking.STATUS_REJECTED
#         booking.admin_note = request.data.get('admin_note', '')
#         booking.save()
#         return Response({"detail":"Booking rejected"}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def cancel(self, request, pk=None):
#         booking = self.get_object()
#         # only admin, operator owner, or booking owner can cancel:
#         user = request.user
#         if not (user.is_staff or user.is_superuser or getattr(booking, "user_id", None) == user.id or getattr(booking.service, "operator_id", None) == user.id):
#             return Response({"detail":"Not allowed"}, status=status.HTTP_403_FORBIDDEN)
#         booking.status = Booking.STATUS_CANCELLED
#         booking.save()
#         return Response({"detail":"Booking cancelled"}, status=status.HTTP_200_OK)

# class NotificationListView(generics.ListAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
    
# class BookingCreateView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking, Notification
from .serializers import BookingCreateSerializer, BookingDetailSerializer, BookingSerializer, NotificationSerializer
from .permissions import IsBookingOwnerOrOperatorOrAdmin
from services.models import Service
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from rest_framework.views import APIView


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-created_at")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsBookingOwnerOrOperatorOrAdmin]

    def get_serializer_class(self):
        if self.action in ['create']:
            return BookingCreateSerializer
        return BookingDetailSerializer

    def perform_create(self, serializer):
        # attach user if authenticated
        user = self.request.user if self.request.user.is_authenticated else None
        # default status pending
        serializer.save(user=user, status=Booking.STATUS_PENDING)

    def get_queryset(self):
        user = self.request.user
        # public listing: none (tourists shouldn't see all bookings). Only admin, operator and owners have listings.
        if user.is_authenticated:
            # admin: all bookings
            if user.is_staff or user.is_superuser:
                return Booking.objects.all().order_by("-created_at")
            # operator: bookings for operator's services
            if getattr(user, "role", None) == "operator":
                return Booking.objects.filter(service__operator=user).order_by("-created_at")
            # normal user: their bookings
            return Booking.objects.filter(user=user).order_by("-created_at")
        # anonymous: no list
        return Booking.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = Booking.STATUS_CONFIRMED
        booking.admin_note = request.data.get('admin_note', '')
        booking.save()
        # create notifications via signals (we'll implement)
        return Response({"detail":"Booking confirmed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = Booking.STATUS_REJECTED
        booking.admin_note = request.data.get('admin_note', '')
        booking.save()
        return Response({"detail":"Booking rejected"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        # only admin, operator owner, or booking owner can cancel:
        user = request.user
        if not (user.is_staff or user.is_superuser or getattr(booking, "user_id", None) == user.id or getattr(booking.service, "operator_id", None) == user.id):
            return Response({"detail":"Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        return Response({"detail":"Booking cancelled"}, status=status.HTTP_200_OK)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingListView(APIView):
    def get(self, request):
        return JsonResponse({"message": "Booking list endpoint - coming soon"})

class BookingDetailView(APIView):
    def get(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            serializer = BookingDetailSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
