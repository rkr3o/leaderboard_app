import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

from libs.utils import token_utils  # your JWT helper class

class AuthMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.jwt_authorization_token = request.headers.get("authorization", None)
        self.jwt_token_util = token_utils.JWTToken()
        self.parsed_payload = None
        self.payload = None
        self.validate_authentication_token()

    def validate_authentication_token(self):
        if not self.jwt_authorization_token:
            raise AuthenticationFailed({"status": 401, "message": "Authorization token missing"})

        # Usually header is "Bearer <token>"
        parts = self.jwt_authorization_token.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise AuthenticationFailed({"status": 401, "message": "Invalid authorization header format"})

        token = parts[1]
        self.decode_authentication_token(token)

    def decode_authentication_token(self, token):
        try:
            self.parsed_payload = self.jwt_token_util.parse_jwt_token(token)
            self.validate_parsed_payload()
            self.payload = self.jwt_token_util.decode_jwt_token_payload(self.parsed_payload)
        except Exception:
            raise AuthenticationFailed({"status": 401, "message": "Invalid or expired token"})

    def validate_parsed_payload(self):
        if not self.parsed_payload:
            raise AuthenticationFailed({"status": 401, "message": "Invalid token payload"})

        exp = self.parsed_payload.get("exp")
        if exp and make_aware(datetime.datetime.fromtimestamp(exp)) <= timezone.now():
            raise AuthenticationFailed({"status": 401, "message": "Token has expired"})
