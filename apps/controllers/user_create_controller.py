from apps.db_manager.models import User

class UserCreateController:
    def __init__(self, data):
        self.data = data
        self.result = {}

    def __call__(self):
        phone_number = self.data.get("phone_number")
        user, created = User.objects.get_or_create(phone_number=phone_number)
        self.result = {
            "user_id": user.id,
            "created": created 
        }
