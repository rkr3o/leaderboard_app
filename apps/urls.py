from django.urls import path

from apps.views.api_views import LeaderboardTopView, PlayerRankView, SubmitScoreView
from apps.views.user_registration_views import UserGameRegisterView, UserRegisterView


urlpatterns = [
    path("api/leaderboard/top", LeaderboardTopView.as_view(), name="leaderboard-top"),
    path(
        "api/leaderboard/rank/<int:user_id>",
        PlayerRankView.as_view(),
        name="player-rank",
    ),
    path("api/leaderboard/submit", SubmitScoreView.as_view(), name="submit-score"),
]
