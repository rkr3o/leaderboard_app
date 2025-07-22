from django.urls import include, path
from apps.views.user_views import JWTRefreshView, JWTView, UserCreateView
from apps.views.api_views import LeaderboardTopView, PlayerRankView, SubmitScoreView

user_urls = [
    path("token/", JWTView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", JWTRefreshView.as_view(), name="token_refresh"),
    path("create/user/", UserCreateView.as_view(), name="user_create"),
]

leaderboard_urls = [
    path("top/", LeaderboardTopView.as_view(), name="leaderboard-top"),
    path("rank/", PlayerRankView.as_view(), name="player-rank"),
    path("submit/", SubmitScoreView.as_view(), name="submit-score"),
]

urlpatterns = [
    path("user/", include((user_urls, "user"))),
    path("leaderboard/", include((leaderboard_urls, "leaderboard"))),
]
