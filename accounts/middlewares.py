from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

from dotenv import load_dotenv

from accounts.auth_backends.custom_backend import TokenBackend

load_dotenv()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get("auth_token")
        user = TokenBackend().authenticate(request,token=token)
        request.user = SimpleLazyObject(
                            lambda: user if user else get_user(request)
        )   