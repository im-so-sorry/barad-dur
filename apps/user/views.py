from distutils.util import strtobool
from typing import Optional

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.user.models import SocialUser
from apps.user.serializers import SocialUserSerializer


class SocialUserModelView(viewsets.ModelViewSet):
    queryset = SocialUser.objects.all()
    serializer_class = SocialUserSerializer

    @action(methods=["GET"], detail=False, url_path="get_user")
    def get_user(self, request: Request, *args, **kwargs):
        token: Optional[str] = request.query_params.get("token")
        social_username = request.META.get('HTTP_X_USERNAME')
        social_service = request.META.get('HTTP_X_SERVICE')

        social_user = SocialUser.objects.get_or_create_user(social_username, social_service, token)

        serializer = self.get_serializer(social_user)

        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path="switch_streaming")
    def switch_streaming(self, request: Request, *args, **kwargs):
        token: Optional[str] = request.query_params.get("token")
        social_username = request.META.get('HTTP_X_USERNAME')
        social_service = request.META.get('HTTP_X_SERVICE')

        new_state = request.data.get("state")
        if new_state is None:
            return Response("Invalid state", status=400)

        social_user = SocialUser.objects.get_or_create_user(social_username, social_service, token)

        social_user.user.is_streaming = new_state
        social_user.user.save()

        return Response("ok")
