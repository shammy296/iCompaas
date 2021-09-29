from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.settings import knox_settings
from rest_framework.exceptions import AuthenticationFailed


'''
Authentication is handled using this util.
'''


class KnoxTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            result = super(KnoxTokenAuthentication, self).authenticate(request)
            if result:
                user, auth_token = result
                current_expiry = auth_token.expiry
                new_expiry = timezone.now() + knox_settings.TOKEN_TTL
                auth_token.expires = new_expiry
                if (new_expiry - current_expiry).total_seconds() > 1:
                    pass
            return result
        except AuthenticationFailed:
            raise AuthenticationFailed({'msg': 'Invalid session.'})
