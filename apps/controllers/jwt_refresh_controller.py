import datetime
import jwt
from django.utils.timezone import now
from django.conf import settings
from apps.db_manager.models import JWTToken

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_ACCESS_EXP_SECONDS = 3600  # 1 hour
JWT_REFRESH_EXP_SECONDS = 7 * 24 * 3600  # 7 days


class JWTRefreshController:
    def __init__(self, data=None):
        self.data = data or {}
        self.refresh_token = self.data.get("refresh_token")
        self.result = {}

    def __call__(self):
        if not self.refresh_token:
            self.result = {"error": "Missing refresh_token"}
            return

        self.validate_and_refresh()

    def validate_and_refresh(self):
        try:
            payload = jwt.decode(
                self.refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            self.result = {"error": "Refresh token expired"}
            return
        except jwt.InvalidTokenError:
            self.result = {"error": "Invalid refresh token"}
            return

        token_record = JWTToken.objects.filter(
            token=self.refresh_token, is_active=True
        ).first()
        if not token_record:
            self.result = {"error": "Refresh token not found or revoked"}
            return

        user_id = payload.get("user_id")
        if not user_id:
            self.result = {"error": "Invalid token payload"}
            return

        # Issue new access token
        new_access_payload = {
            "user_id": user_id,
            "iat": now(),
            "exp": now() + datetime.timedelta(seconds=JWT_ACCESS_EXP_SECONDS),
        }
        new_access_token = jwt.encode(
            new_access_payload, JWT_SECRET, algorithm=JWT_ALGORITHM
        )

        self.result = {
            "access_token": new_access_token,
            "user_id": user_id,
        }
