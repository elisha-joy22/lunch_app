from rest_framework import exceptions
from dotenv import load_dotenv

from datetime import datetime,timedelta
import os
import jwt

load_dotenv()

def generate_jwt(user):
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    jwt_algorithm = os.getenv('JWT_ALGORITHM')

    payload = {
        'user' : user['email'],
        'exp' : datetime.now() + timedelta(days=1)
    }
    print("generating jwt...")
    jwt_token = jwt.encode(payload,jwt_secret,algorithm=jwt_algorithm)
    return jwt_token


def set_jwt_cookie(response, jwt_token):
    print('setting jwt cookie ...')
    max_age_seconds = 7*24*60*60
    response.set_cookie('auth_token', jwt_token, max_age=max_age_seconds, httponly=True)
    return response


def decode_jwt(token):
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    jwt_algorithm = os.getenv('JWT_ALGORITHM')
    
    try:
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=[jwt_algorithm]
        )
        return payload
    except (ValueError, jwt.ExpiredSignatureError, jwt.DecodeError):
        raise exceptions.AuthenticationFailed('Invalid or expired token')

