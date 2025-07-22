from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.common.authmixin import AuthMixin
from apps.controllers.jwt_refresh_controller import JWTRefreshController
from apps.controllers.user_create_controller import UserCreateController
from apps.serializers.user_create_serializer import UserCreateSerializer

from apps.serializers.jwt_serializer import JWTRefreshSerializer, JWTSerializer
from apps.controllers.jwt_controller import JWTController


class JWTView(APIView, AuthMixin):
    def post(self, request):
        serializer = JWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        controller = JWTController(serializer.validated_data)
        controller()

        if "error" in controller.result:
            return Response(controller.result, status=status.HTTP_400_BAD_REQUEST)

        return Response(controller.result, status=status.HTTP_200_OK)


class JWTRefreshView(APIView, AuthMixin):
    def post(self, request):
        serializer = JWTRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        controller = JWTRefreshController(serializer.validated_data)
        controller()

        if "error" in controller.result:
            return Response(controller.result, status=status.HTTP_400_BAD_REQUEST)
        return Response(controller.result, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        controller = UserCreateController(serializer.validated_data)
        controller()

        return Response(controller.result, status=status.HTTP_201_CREATED)
