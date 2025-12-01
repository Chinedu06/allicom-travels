# from rest_framework import generics, permissions, status
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from django.db import transaction
# from django.shortcuts import get_object_or_404

# from .models import Service, ServiceImage, Package
# from .serializers import (
#     ServiceListSerializer,
#     ServiceDetailSerializer,
#     ServiceCreateUpdateSerializer,
#     ServiceImageSerializer,
#     PackageSerializer,
# )
# from .permissions import IsOperatorOrReadOnly, IsOperatorOwnerOrAdmin

# # -------------------------
# # Service views (unchanged behaviour)
# # -------------------------

# class ServiceListView(generics.ListAPIView):
#     """
#     Public endpoint — tourists can view all approved services.
#     """
#     queryset = Service.objects.filter(is_approved=True, is_active=True)
#     serializer_class = ServiceListSerializer
#     permission_classes = [permissions.AllowAny]


# class ServiceDetailView(generics.RetrieveAPIView):
#     """
#     Public endpoint — view details of a specific service.
#     """
#     queryset = Service.objects.filter(is_approved=True, is_active=True)
#     serializer_class = ServiceDetailSerializer
#     permission_classes = [permissions.AllowAny]


# class OperatorServiceListView(generics.ListAPIView):
#     """
#     Operators can view only their own services.
#     """
#     serializer_class = ServiceListSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Service.objects.filter(operator=self.request.user)


# class ServiceCreateView(generics.CreateAPIView):
#     """
#     Operators create new tours.
#     """
#     serializer_class = ServiceCreateUpdateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]  # enable image uploads

#     def perform_create(self, serializer):
#         service = serializer.save(operator=self.request.user)
#         # handle uploaded images (if any)
#         for file in self.request.FILES.getlist('images'):
#             ServiceImage.objects.create(service=service, image=file)
#         return service


# class ServiceUpdateView(generics.UpdateAPIView):
#     """
#     Operators can update their own services.
#     """
#     serializer_class = ServiceCreateUpdateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def get_queryset(self):
#         return Service.objects.filter(operator=self.request.user)

#     def perform_update(self, serializer):
#         service = serializer.save()
#         if 'images' in self.request.FILES:
#             for file in self.request.FILES.getlist('images'):
#                 ServiceImage.objects.create(service=service, image=file)
#         return service


# class ServiceDeleteView(generics.DestroyAPIView):
#     """
#     Operators can delete their own services.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Service.objects.filter(operator=self.request.user)


# # -------------------------
# # Package views (new)
# # -------------------------

# class PackageListView(generics.ListAPIView):
#     """
#     Public list of packages for a service.
#     GET /api/services/<service_id>/packages/
#     """
#     serializer_class = PackageSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         service_id = self.kwargs.get('service_id')
#         # Only packages for approved & active services should be publicly visible
#         return Package.objects.filter(service_id=service_id, is_active=True, service__is_approved=True, service__is_active=True)


# class PackageDetailView(generics.RetrieveAPIView):
#     """
#     GET /api/packages/<pk>/
#     """
#     queryset = Package.objects.all()
#     serializer_class = PackageSerializer
#     permission_classes = [permissions.AllowAny]


# class PackageCreateView(generics.CreateAPIView):
#     """
#     Operators create a package under a given service.
#     POST /api/services/<service_id>/packages/
#     """
#     serializer_class = PackageSerializer
#     permission_classes = [IsOperatorOwnerOrAdmin]

#     def perform_create(self, serializer):
#         service_id = self.kwargs.get('service_id')
#         service = get_object_or_404(Service, pk=service_id)

#         # ensure request.user is owner of the service (permission class also checks)
#         if not (self.request.user.is_staff or self.request.user.is_superuser) and service.operator_id != self.request.user.id:
#             raise permissions.PermissionDenied("Not allowed to create package for this service.")

#         serializer.save(service=service)


# class PackageUpdateView(generics.UpdateAPIView):
#     """
#     PUT/PATCH /api/packages/<pk>/
#     Only operator-owner or admin can update.
#     """
#     queryset = Package.objects.all()
#     serializer_class = PackageSerializer
#     permission_classes = [IsOperatorOwnerOrAdmin]


# class PackageDeleteView(generics.DestroyAPIView):
#     """
#     DELETE /api/packages/<pk>/
#     """
#     queryset = Package.objects.all()
#     serializer_class = PackageSerializer
#     permission_classes = [IsOperatorOwnerOrAdmin]

from rest_framework import generics
from .models import Service, Package
from .serializers import ServiceSerializer, PackageSerializer


class ServiceListView(generics.ListAPIView):
    """
    Returns a list of all active services.
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer


class ServiceDetailView(generics.RetrieveAPIView):
    """
    Returns details of a single service including its packages.
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    lookup_field = "slug"


class PackageListView(generics.ListAPIView):
    """
    List all packages (usually used internally).
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageDetailView(generics.RetrieveAPIView):
    """
    Get a single package by ID.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = "id"
