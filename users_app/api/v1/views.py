from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from django.shortcuts import get_object_or_404
from utils.jwt_token import token_decoder

User = get_user_model()

# region - Resgister API View
class RegisterAPIView(CreateAPIView):
    """Register a new user"""
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = RegisterSerializer

# endregion

# region - Confirm Email API View
class ConfirmEmailAPIView(RegisterAPIView):
    """Confirm users email"""
    def get(self, request, token):
        # Decode the token to get the user id
        user_id = token_decoder(token)
        # Attempt to retrieve the user and activate the account
        try:
            user = get_object_or_404(User, pk=user_id)
            if user.is_verified:
                return Response({'message': 'You are already verified'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response(user_id)

# endregion