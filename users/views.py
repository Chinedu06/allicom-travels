from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, this is the Users app homepage!")

from django.http import JsonResponse
from rest_framework.views import APIView

class RegisterView(APIView):
    def post(self, request):
        return JsonResponse({"message": "User registration endpoint - coming soon"})

class LoginView(APIView):
    def post(self, request):
        return JsonResponse({"message": "User login endpoint - coming soon"})

class OperatorRegisterView(APIView):
    def post(self, request):
        return JsonResponse({"message": "Operator registration endpoint - coming soon"})

class OperatorLoginView(APIView):
    def post(self, request):
        return JsonResponse({"message": "Operator login endpoint - coming soon"})
