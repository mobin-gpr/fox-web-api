from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class CustomRefreshToken(RefreshToken):
    """Custom refresh token"""

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["email"] = user.email  # Add the email to the token payload
        return token


def token_generator(user):
    """get jwt tokens for user"""
    refresh = CustomRefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def token_decoder(token):
    """decode jwt token"""
    try:
        # Decode the token
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data["user_id"]
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {
            "error": "Activation link has expired!",
        }
    except jwt.InvalidTokenError:
        # Token is invalid
        return {
            "error": "Activation link has expired!",
        }
