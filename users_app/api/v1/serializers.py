from django.core.mail import EmailMessage
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from utils.email import EmailThread

User = get_user_model()


# region - Serializer Of Registration
class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer create a new user
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        password = data.get('password')
        # Check clean password for password and confirm_password
        if password != data['confirm_password']:
            error = serializers.ValidationError({'details': 'Passwords must match'})
            raise error
        # Check password complexity
        try:
            validate_password(password)
        except serializers.ValidationError:
            raise serializers.ValidationError()
        return data

    # Create a new user
    def create(self, validated_data):
        email = validated_data.get('email')
        # raise an error if this email is already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'details': 'Email already registered'})
        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
        )
        # Sending confirm email token
        msg = f'for confirm email click on: '
        email_obj = EmailMessage('Confirm email', msg, to=[email])
        # Sending email with threading
        EmailThread(email_obj).start()

        return {
            'id': user.id,
            'email': user.email,
        }

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password')
