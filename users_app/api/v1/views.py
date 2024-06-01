from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from utils.jwt_token import token_decoder
from django.urls import reverse
from django.core.mail import EmailMessage
from utils.email import EmailThread
from utils.jwt_token import token_generator
from django.contrib.auth.password_validation import validate_password
from .serializers import RegisterSerializer, ResendEmailVerificationSerializer, ChangePasswordSerializer, \
    ResetPasswordSerializer, SetPasswordSerializer, ProfileSerializer
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
            # Generate a jwt token for resend confirm email
            token = token_generator(user)
            # Resending confirm email token
            confirm_url = self.request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token['access']}))
            msg = f'for confirm email click on: {confirm_url}'
            email_obj = EmailMessage('Confirm email', msg, to=[user.email])
            # Sending email with threading
            EmailThread(email_obj).start()
            return Response({'message: The activation email has been sent again successfully'},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# endregion


# region - Change Password API View

class ChangePasswordAPIView(APIView):
    """Change user password"""
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Get current user
            user: User = User.objects.get(id=self.request.user.id)
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            # Old password is correct
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Your password has been changed successfully!'}, status=status.HTTP_200_OK)
            # Old password is not correct
            else:
                return Response({'error': 'Your old password is not correct'})
        # Serializer is not valid
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# endregion

# region - Reset Password API View

class ResetPasswordAPIView(APIView):
    """Reset user password"""
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user: User = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
            # Generate a jwt token for reset password
            token = token_generator(user)
            # Sending reset password email token
            set_password_url = self.request.build_absolute_uri(
                reverse('set_password', kwargs={'token': token['access']}))
            msg = f'for reset password click on: {set_password_url}'
            email_obj = EmailMessage('Set password', msg, to=[user.email])
            # Sending email with threading
            EmailThread(email_obj).start()
            return Response({'message: Reset password email has been sent!'},
                            status=status.HTTP_200_OK)

        return Response('')


# endregion

# region - Set Password API View
class SetPasswordAPIView(APIView):
    """Set user password"""
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SetPasswordSerializer

    def post(self, request, token):
        serializer = SetPasswordSerializer(data=request.data)
        # Decode the token to get the user id
        user_id = token_decoder(token)

        try:
            user = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        # Token is not valid or expired
        except TypeError:
            return Response(user_id)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Your password has been changed successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion

# region - Profile API View

class ProfileAPIView(RetrieveAPIView):
    """User profile view"""
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProfileSerializer

    # definition of get_object due to not using lookup_field
    def get_object(self):
        return self.request.user
    def get_queryset(self):
        return get_object_or_404(User, id=self.get_object().id)

# endregion