from django.db import transaction

from apps.db_manager.models import GameSession, Leaderboard

class SubmitScoreController:
    def __init__(self, data=None):
        self.data = data or {}
        self.user_id = self.data.get("user_id")
        self.score = self.data.get("score")
        self.game_mode = self.data.get("game_mode", "solo")
        # Fetch or create leaderboard object for the user
        self.leaderboard_obj, _ = Leaderboard.objects.get_or_create(user_id=self.user_id)
        self.result = {}

    def __call__(self, *args, **kwargs):
        # Defensive check: Ensure user exists before processing
        from django.core.exceptions import ObjectDoesNotExist
        try:
            with transaction.atomic():
                # Create new gamesession entry
                GameSession.objects.create(
                    user_id=self.user_id,
                    score=self.score,
                    game_mode=self.game_mode
                )
                # Update total score in leaderboard
                self.leaderboard_obj.total_score += self.score
                self.leaderboard_obj.save()

            self.result = {"message": "Score submitted successfully"}
        except ObjectDoesNotExist:
            self.result = {"error": "User not found"}
        except Exception as e:
            self.result = {"error": str(e)}
