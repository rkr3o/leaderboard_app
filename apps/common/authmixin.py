import jwt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class AuthMixin:
    JWT_SECRET = settings.SECRET_KEY
    JWT_ALGORITHM = "HS256"

    def validate_frontend_calls(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"error": "Authorization header missing or invalid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM]
            )
            # Optionally return payload if you want to use it later
            return payload
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
