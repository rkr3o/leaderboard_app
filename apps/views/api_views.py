from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.controllers.leaderboard_top_controller import LeaderboardTopController
from apps.controllers.player_rank_controller import PlayerRankController
from apps.serializers.leader_board_top_serializer import LeaderboardTopSerializer
from apps.serializers.player_rank_serializer import PlayerRankSerializer
from apps.serializers.submit_score_serializer import SubmitScoreSerializer
from apps.controllers.submit_score_controller import SubmitScoreController


class SubmitScoreView(APIView):
    def post(self, request):
        ser = SubmitScoreSerializer(data=request.data)
        ser.is_valid()
        instance = SubmitScoreController(request.data)
        instance()

        response_data = instance.result
        return Response(response_data, status=status.HTTP_200_OK)


class LeaderboardTopView(APIView):
    def get(self, request):
        # Pass query params for validation
        ser = LeaderboardTopSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        instance = LeaderboardTopController(request.query_params)
        instance()
        response_data = instance.result
        return Response(response_data, status=status.HTTP_200_OK)


class PlayerRankView(APIView):
    def get(self, request, user_id):
        # Include path param user_id + query params if any
        data = {"user_id": user_id, **request.query_params}
        ser = PlayerRankSerializer(data=data)
        ser.is_valid(raise_exception=True)
        instance = PlayerRankController(data)
        instance()
        response_data = instance.result
        return Response(response_data, status=status.HTTP_200_OK)
