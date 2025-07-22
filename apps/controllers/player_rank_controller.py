from apps.db_manager.models import Leaderboard
from django.shortcuts import get_object_or_404


class PlayerRankController:
    def __init__(self, data=None):
        self.data = data or {}
        self.user_id = self.data.get("user_id")
        self.result = {}

    def __call__(self):
        entry = get_object_or_404(Leaderboard, user_id=self.user_id)
        self.result = {
            "user_id": self.user_id,
            "rank": entry.rank,
            "total_score": entry.total_score,
        }
