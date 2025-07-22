from rest_framework import serializers
from constants.constants_and_methods import raise_error


class PlayerRankSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        user_id = data.get("user_id")
        if not user_id:
            raise_error(1, "user_id is missing", 400)
        return {"user_id": user_id}

    def to_representation(self, instance):
        return instance
