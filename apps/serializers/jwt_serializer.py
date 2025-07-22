from rest_framework import serializers
from constants.constants_and_methods import raise_error


class JWTSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        if not data:
            raise_error(1, "No data provided", 400)

        user_id = data.get("user_id")
        token = data.get("token")

        if not user_id and not token:
            raise_error(2, "Either user_id or token must be provided", 400)

        return {
            "user_id": user_id,
            "token": token,
        }

    def to_representation(self, instance):
        return instance


class JWTRefreshSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        refresh_token = data.get("refresh_token")
        if not refresh_token:
            raise_error(1, "refresh_token is missing", 400)
        return {"refresh_token": refresh_token}

    def to_representation(self, instance):
        return instance
