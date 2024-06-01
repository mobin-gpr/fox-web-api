from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from utils.email import EmailThread
from utils.jwt_token import token_generator

User = get_user_model()


# region - Serializer Of Registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer create a new user & send email verification code
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        password = attrs.get("password")
        # Check clean password for password and confirm_password
        if password != attrs["confirm_password"]:
            error = serializers.ValidationError({"error": "The passwords do not match"})
            raise error
        # Check password complexity
        try:
            # validate password complexity
            validate_password(password)
        # password is not strong
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return attrs

    # Create a new user
    def create(self, validated_attrs):
        request = self.context.get("request")
        email = validated_attrs.get("email")
        # raise an error if this email is already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already registered"})
        user = User.objects.create_user(
            password=validated_attrs["password"],
            email=validated_attrs["email"],
        )
        # Generate a jwt token for confirm email
        token = token_generator(user)
        # Sending confirm email token
        confirm_url = request.build_absolute_uri(
            reverse("confirm_email", kwargs={"token": token["access"]})
        )
        msg = f"for confirm email click on: {confirm_url}"
        email_obj = EmailMessage("Confirm email", msg, to=[email])
        # Sending email with threading
        EmailThread(email_obj).start()

        return {
            "id": user.id,
            "email": user.email,
        }

    class Meta:
        model = User
        fields = ("id", "email", "password", "confirm_password")


# region - Serializer Of Resend Email Verification
class ResendEmailVerificationSerializer(serializers.Serializer):
    """This serializer resend email verification code"""

    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist!"})
        if user.is_verified:
            raise serializers.ValidationError({"error": "Email already verified"})
        # Adding the user field to attrs to be captured in the resend email confirmation view to prevent re-query
        attrs["user"] = user
        return super().validate(attrs)


# endregion


# region - Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    """This serializer change user password"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")
        # If new password & confirm new password are not match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "The passwords do not match"})

        # validate password complexity
        try:
            validate_password(new_password)
        # password is not strong
        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)


# endregion

# region - Reset Password Serializer


class ResetPasswordSerializer(serializers.Serializer):
    """Reset user password"""

    email = serializers.EmailField(required=True)


# endregion


# region - Set Password Serializer
class SetPasswordSerializer(serializers.Serializer):
    """Set user password after reset password"""

    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")
        # If new password & confirm new password are not match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "The passwords do not match"})

        # validate password complexity
        try:
            validate_password(new_password)
        # password is not strong
        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)


# endregion

# region - Profile Serializer


class ProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        )


# endregion
