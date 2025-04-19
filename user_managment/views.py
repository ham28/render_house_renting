import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, permissions

from .serializers import UserSerializer, LoginSerializer

logger = logging.getLogger("django")

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            # Vérifiez si l'utilisateur a un reseller
            user_data = UserSerializer(user).data if user.reseller else "none"
            logger.info(f"User data: {user_data}")  # Ajout d'un log pour voir les données utilisateur

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data,
            }
            logger.info(f"Login successful. Response data: {response_data}")
            return Response(response_data)
        logger.warning(f'Invalid login attempt for username: {username}')
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyCredentialsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'status': 'valid'})
        logger.warning(f'Invalid verification attempt for username: {username}')
        return Response({'status': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Customizations for the token view can be added here
    pass


@api_view(['POST'])
def validate_token(request):
    # Logic for validating the token
    return Response({"message": "Token is valid."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin_status(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'groups': list(user.groups.values_list('name', flat=True)),
        'phone_number': user.profile.telephone if hasattr(user, 'profile') else None,
        'fonction': user.profile.fonction if hasattr(user, 'profile') else None,
    })

