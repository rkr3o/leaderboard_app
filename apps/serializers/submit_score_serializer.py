from rest_framework import serializers
from constants.constants_and_methods import raise_error  # your custom error helper

class SubmitScoreSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        if not data:
            raise_error(1, "No data provided", 400)

        user_id = data.get("user_id")
        if not user_id:
            raise_error(2, "user_id is missing", 400)

        score = data.get("score")
        if score is None:
            raise_error(3, "score is missing", 400)

        game_mode = data.get("game_mode", "solo")
        if not isinstance(game_mode, str):
            raise_error(4, "game_mode must be a string", 400)

        # Return the validated dictionary
        return {
            "user_id": user_id,
            "score": score,
            "game_mode": game_mode,
        }

    def to_representation(self, instance):
        return {}
