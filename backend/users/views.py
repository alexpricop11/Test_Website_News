from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .managers import AuthManager


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token = AuthManager.generate_token(user)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            token = AuthManager.generate_token(user)
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
