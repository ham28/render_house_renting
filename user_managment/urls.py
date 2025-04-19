from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, VerifyCredentialsView, SmsUserLogin, LoginSMSUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

router = DefaultRouter()

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]