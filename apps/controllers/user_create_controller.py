from apps.db_manager.models import User, UserDetails
from django.db.models import Max


class UserCreateController:
    def __init__(self, data=None):
        self.data = data or {}
        self.phone_number = data.get("phone_number")
        self.result = {}

    def __call__(self):
        self.check_for_existing_user()
    
    def check_for_existing_user(self):
        existing_user = UserDetails.objects.filter(phone_number=self.phone_number).first()
        if existing_user and existing_user.user_id:
            raise ValueError("User with this phone number already exists")
    
    def process_to_create_user(self):
        phone_number = self.data.get("phone_number")
        last_user_id = UserDetails.objects.aggregate(Max("user_id"))["user_id__max"]
        new_user_id = (last_user_id or 1) + 1 

        user, created = UserDetails.objects.get_or_create(
            phone_number=phone_number,
            defaults={"user_id": new_user_id}
        )

        self.result = {"user_id": user.user_id, "created": created}