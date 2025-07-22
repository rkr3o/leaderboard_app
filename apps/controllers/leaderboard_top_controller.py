
from apps.db_manager.models import Leaderboard


class LeaderboardTopController:
    def __init__(self, data=None):
        self.result = []
    
    def __call__(self):
        # Fetch top 10 leaderboard entries ordered by total_score desc
        qs = Leaderboard.objects.select_related('user').order_by('-total_score')[:10]
        result = []
        for entry in qs:
            result.append({
                "user_id": entry.user.id,
                "username": entry.user.username,
                "total_score": entry.total_score,
                "rank": entry.rank,
            })
        self.result = result


