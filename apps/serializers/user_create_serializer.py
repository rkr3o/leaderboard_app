from rest_framework import serializers
from apps.db_manager.models import User
from rest_framework.exceptions import ValidationError

class UserCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number already exists.")
        return value

    def to_representation(self, instance):
        return {
            "user_id": instance.id,
            "phone_number": instance.phone_number,
        }
