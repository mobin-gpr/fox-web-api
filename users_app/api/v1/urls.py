from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),  # Register a new user
    path('confirm_email/<str:token>/', EmailVerificationAPIView.as_view(), name='confirm_email'),  # Confirm email by token
    path('resend_confirm_email/', ResendEmailVerificationAPIView.as_view(), name='resend_confirm_email'),  # Resend confirm email
    path('change_password/', ChangePasswordAPIView.as_view(), name='change_password'),  # Change user password
]
