from django.urls import include, path
from apps.views.token_views import JWTRefreshView, JWTView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.views.api_views import LeaderboardTopView, PlayerRankView, SubmitScoreView

token_urls = [
    path("token/", JWTView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", JWTRefreshView.as_view(), name="token_refresh"),
]

leaderboard_urls = [
    path("top/", LeaderboardTopView.as_view(), name="leaderboard-top"),
    path("rank/<int:user_id>/", PlayerRankView.as_view(), name="player-rank"),
    path("submit/", SubmitScoreView.as_view(), name="submit-score"),
]

urlpatterns = [
    path("user/", include((token_urls, "user"))),
    path("leaderboard/", include((leaderboard_urls, "leaderboard"))),
]
