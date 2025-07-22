import datetime
import jwt
from django.utils.timezone import now
from django.conf import settings
from apps.db_manager.models import JWTToken

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1 hour


class JWTController:
    def __init__(self, data=None):
        self.data = data or {}
        self.user_id = self.data.get("user_id")
        self.token = self.data.get("token")
        self.result = {}

    def __call__(self):
        if self.user_id:
            self.create_token()
        elif self.token:
            self.validate_token()
        else:
            self.result = {"error": "Missing user_id or token"}

    def create_token(self):
        payload = {
            "user_id": self.user_id,
            "name": "Test",
            "iat": now(),
            "exp": now() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Save or update token in DB
        JWTToken.objects.update_or_create(
            user_id=self.user_id,
            defaults={
                "token": token,
                "created_at": now(),
                "expired_at": now() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
                "is_active": True,
            },
        )

        self.result = {"token": token}

    def validate_token(self):
        try:
            payload = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            self.result = {"error": "Token expired"}
            return
        except jwt.InvalidTokenError:
            self.result = {"error": "Invalid token"}
            return

        token_record = JWTToken.objects.filter(token=self.token, is_active=True).first()
        if not token_record:
            self.result = {"error": "Token not found or revoked"}
            return

        self.result = {"message": "Token is valid", "user_id": payload.get("user_id")}
