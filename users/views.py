# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.
# def index(request):
#     return HttpResponse("Hello, this is the Users app homepage!")

# from django.http import JsonResponse
# from rest_framework.views import APIView

# class RegisterView(APIView):
#     def post(self, request):
#         return JsonResponse({"message": "User registration endpoint - coming soon"})

# class LoginView(APIView):
#     def post(self, request):
#         return JsonResponse({"message": "User login endpoint - coming soon"})

# class OperatorRegisterView(APIView):
#     def post(self, request):
#         return JsonResponse({"message": "Operator registration endpoint - coming soon"})

# class OperatorLoginView(APIView):
#     def post(self, request):
#         return JsonResponse({"message": "Operator login endpoint - coming soon"})

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from .serializers import OperatorRegisterSerializer, OperatorLoginSerializer, SupplierProfileSerializer

from rest_framework.decorators import action

from .models import SupplierProfile
from .permissions import IsOperator, IsVerifiedOperator, IsOwnerOrAdmin


def index(request):
    return HttpResponse("Hello, this is the Users app homepage!")


class OperatorRegisterView(APIView):
    """
    POST /api/users/operators/signup/
    Register a new operator (requires phone_number).
    Account stays inactive until admin verifies.
    """
    def post(self, request):
        serializer = OperatorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Operator registered successfully. Awaiting admin approval.",
                "operator": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_verified": user.is_verified,
                    "phone_number": user.phone_number
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperatorLoginView(APIView):
    """
    POST /api/users/operators/login/
    Login with email + password. Returns JWT tokens if verified.
    """
    def post(self, request):
        serializer = OperatorLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Login successful.",
                "access": serializer.validated_data['access'],
                "refresh": serializer.validated_data['refresh'],
                "operator": serializer.validated_data['user']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SupplierProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD for SupplierProfile.
    - Non-staff users only see their own profile.
    - Admin/staff can list/retrieve all profiles via API (if we want).
    - create(): operator must be verified (is_verified==True) to create profile.
    """
    queryset = SupplierProfile.objects.all()
    serializer_class = SupplierProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOperator, IsOwnerOrAdmin]

    def get_permissions(self):
        """
        Fine-grained permissions:
        - create: require verified operator.
        - list: staff only (avoid exposing all profiles to operators).
        - other actions: owner or admin via IsOwnerOrAdmin + IsOperator.
        """
        perms = []
        if self.action == 'create':
            perms = [permissions.IsAuthenticated(), IsOperator(), IsVerifiedOperator()]
        elif self.action == 'list':
            # list should be staff-only for now
            perms = [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        else:
            # retrieve/update/destroy: owner or admin
            perms = [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        return [p for p in perms]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return SupplierProfile.objects.all()
        return SupplierProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        # always attach the requesting user as owner
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        GET /api/users/operators/profile/me/  -> returns the profile for the logged-in operator
        """
        try:
            profile = SupplierProfile.objects.get(user=request.user)
        except SupplierProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
