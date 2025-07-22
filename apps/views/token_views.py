from apps.controllers.jwt_refresh_controller import JWTRefreshController
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.serializers.jwt_serializer import JWTRefreshSerializer, JWTSerializer
from apps.controllers.jwt_controller import JWTController


class JWTView(APIView):
    def post(self, request):
        serializer = JWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        controller = JWTController(serializer.validated_data)
        controller()

        if "error" in controller.result:
            return Response(controller.result, status=status.HTTP_400_BAD_REQUEST)

        return Response(controller.result, status=status.HTTP_200_OK)

class JWTRefreshView(APIView):
    def post(self, request):
        serializer = JWTRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        controller = JWTRefreshController(serializer.validated_data)
        controller()

        if "error" in controller.result:
            return Response(controller.result, status=status.HTTP_400_BAD_REQUEST)
        return Response(controller.result, status=status.HTTP_200_OK)