from constants.constants_and_methods import raise_error
import jwt
from rest_framework import status
from django.conf import settings


class AuthMixin:
    JWT_SECRET = settings.SECRET_KEY
    JWT_ALGORITHM = "HS256"

    def validate_frontend_calls(self, request):
        token = request.headers.get("Authorization")
        if not token:
            raise_error(
                (
                    1,
                    "Authorization header missing or invalid",
                    status.HTTP_401_UNAUTHORIZED,
                )
            )

        try:
            payload = jwt.decode(
                token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise_error((2, "Token expired", status.HTTP_401_UNAUTHORIZED))
        except jwt.InvalidTokenError:
            raise_error((3, "Invalid token", status.HTTP_401_UNAUTHORIZED))
