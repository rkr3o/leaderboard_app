from rest_framework import serializers
from constants.constants_and_methods import raise_error


class UserCreateSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if not data:
            raise_error((1, "No data provided", 400))

        phone_number = data.get("phone_number")
        if not phone_number:
            raise_error((1, "Phone number is missing", 400))

        return {"phone_number": phone_number}

    def to_representation(self, instance):
        return instance
