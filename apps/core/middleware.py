from typing import Optional

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from apps.user.models import SocialUser


def get_user(username, service) -> Optional['SocialUser']:

    user = None
    if username and service:
        user, _ = SocialUser.objects.get_or_create_user(username=username, service=service)
    return user


class ProcessSocialUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        social_username = request.META.get('HTTP_X_USERNAME')
        social_service = request.META.get('HTTP_X_SERVICE')
        request.social_username = social_username
        request.social_service = social_service
        request.social_user = SimpleLazyObject(lambda: get_user(social_username, social_service))


def get_internal_token(request) -> Optional[str]:
    return request.META.get('HTTP_X_INTERNAL_TOKEN', None)


class InternalTokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.internal_token = SimpleLazyObject(lambda: get_internal_token(request))
