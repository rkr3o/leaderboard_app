import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.db.models import Sum
from django.db import transaction
from apps.db_manager.models import GameSession, Leaderboard


def bulk_create_leaderboard():
    # Aggregate total scores per user
    user_scores = (
        GameSession.objects.values("user")
        .annotate(total_score=Sum("score"))
        .order_by("-total_score")
    )

    leaderboard_entries = []
    rank = 1
    prev_score = None
    same_rank_count = 0

    for entry in user_scores:
        user_id = entry["user"]
        total_score = entry["total_score"]

        if total_score == prev_score:
            same_rank_count += 1
        else:
            rank += same_rank_count
            same_rank_count = 1
        prev_score = total_score

        leaderboard_entries.append(
            Leaderboard(user_id=user_id, total_score=total_score, rank=rank)
        )

    with transaction.atomic():
        Leaderboard.objects.all().delete()  # clear old entries
        Leaderboard.objects.bulk_create(leaderboard_entries)

    print(f"Leaderboard updated with {len(leaderboard_entries)} entries.")


if __name__ == "__main__":
    bulk_create_leaderboard()
