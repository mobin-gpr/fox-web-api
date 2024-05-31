from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ResendEmailVerificationSerializer
from django.shortcuts import get_object_or_404
from utils.jwt_token import token_decoder
from django.urls import reverse
from django.core.mail import EmailMessage
from utils.email import EmailThread
from utils.jwt_token import token_generator

# Get the user from active model
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
class EmailVerificationAPIView(APIView):
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


# region - Resend Email Verification API View
class ResendEmailVerificationAPIView(APIView):
    """Resend a verification email to user"""
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ResendEmailVerificationSerializer
    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            # Get user from serilizer validate method
            user = serializer.validated_data['user']
            # Generate a jwt token for confirm email
            token = token_generator(user)
            # Sending confirm email token
            confirm_url = self.request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token['access']}))
            msg = f'for confirm email click on: {confirm_url}'
            email_obj = EmailMessage('Confirm email', msg, to=[user.email])
            # Sending email with threading
            EmailThread(email_obj).start()
            return Response({'message: The activation email has been sent again successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion