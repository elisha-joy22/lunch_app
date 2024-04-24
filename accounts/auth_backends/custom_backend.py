from django.contrib.auth.backends import BaseBackend

from dotenv import load_dotenv

from accounts.models import CustomUser
from utils.jwt import decode_jwt

load_dotenv()


class TokenBackend(BaseBackend):
    def authenticate(self, request, token=None):
        print("Inside Token Backend authenticate")
        if token is not None:
            try:
                payload = decode_jwt(token)
                user = CustomUser.objects.get(email=payload.get('user'))
                print("User found",user)
                user.is_authenticated = True       #If is_authenticated is lacking - attribute error may occur.
                user.is_active = True              #If is_active is lacking - wrapped attribute error may occur.
                return user
            except CustomUser.DoesNotExist:
                print("TokenBackend-User not found!")
            except Exception as e:
                print("TokenBackend exception ",e)      
        return None
            