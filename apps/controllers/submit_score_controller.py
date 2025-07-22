from django.utils import timezone
from django.db import transaction

from apps.db_manager.models import GameSession, Leaderboard
from django.core.exceptions import ObjectDoesNotExist


class SubmitScoreController:
    def __init__(self, data=None):
        self.data = data or {}
        self.user_id = self.data.get("user_id")
        self.score = self.data.get("score")
        self.game_mode = self.data.get("game_mode", "solo")
        self.leaderboard_obj, _ = Leaderboard.objects.get_or_create(
            user_id=self.user_id
        )
        self.result = {}

    def __call__(self, *args, **kwargs):
        try:
            with transaction.atomic():
                GameSession.objects.create(
                    user_id=self.user_id, score=self.score, game_mode=self.game_mode
                )
                self.leaderboard_obj.total_score += self.score
                self.leaderboard_obj.save()

            self.result = {"message": "Score submitted successfully"}
        except ObjectDoesNotExist:
            self.result = {"error": "User not found"}
        except Exception as e:
            self.result = {"error": str(e)}
