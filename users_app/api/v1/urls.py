from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),  # Register a new user
    path('confirm_email/<str:token>/', ConfirmEmailAPIView.as_view(), name='confirm_email'),  # Confirm email
]
