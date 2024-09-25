import logging
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework import status
from utils.api_response import APIResponse
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from . import services

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return APIResponse.success(
                message="Login successful",
                data=serializer.validated_data,
                status_code=status.HTTP_200_OK,
            )
        except TokenError as e:
            return APIResponse.error(
                e.args[0],
                data={},
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return APIResponse.success(
                message="Token refreshed successfully",
                data=serializer.validated_data,
                status_code=status.HTTP_200_OK,
            )
        except TokenError as e:
            return APIResponse.error(
                e.args[0],
                data={},
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                username = serializer.validated_data["username"]
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]

                user, error = services.create_user(username, email, password)

                if user:
                    return APIResponse.success(
                        message="User registered successfully",
                        data={"username": user.username, "email": user.email},
                        status_code=status.HTTP_201_CREATED,
                    )
                else:
                    return APIResponse.error(
                        message=error,
                        data={},
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )

            return APIResponse.error(
                message="Registration failed",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Unexpected error during user registration: {str(e)}")
            return APIResponse.error(
                message="An unexpected error occurred during registration.",
                data={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
