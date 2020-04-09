from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.backends import ModelBackend

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


def get_authorization_header(request):
    """
    Return request's 'X-Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_X_AUTHORIZATION", b"")
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class XTokenAuthentication(TokenAuthentication):
    """
    Settings:
    ```
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            # Allow X-Authorization header to store token
            'authentication.XTokenAuthentication',
        ),
    }
    ```
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _("Invalid token header. Token string should not " "contain invalid characters.")
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
