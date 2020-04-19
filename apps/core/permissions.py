from django.conf import settings
from rest_framework.permissions import BasePermission


class InternalTokenPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            if request.internal_token_id is None or settings.INTERNAL_TOKEN is None:
                return False
        except:
            return False

        return request.internal_token_id in settings.INTERNAL_TOKENS
