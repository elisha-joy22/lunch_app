from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.web import WebClient

import os
from dotenv import load_dotenv

from utils.accounts import create_user_info,update_or_create_user
from utils.jwt import generate_jwt,set_jwt_cookie
from accounts.serializers import UserSerializer
from accounts.mixins import TokenAuthRequiredMixin

# Create your views here.
load_dotenv()

ENV = os.getenv("ENV")
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID", "")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "")
SLACK_REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI_DEV", "")

if ENV.lower().startswith("prod"):
    SLACK_REDIRECT_URI = os.getenv("SLACK_REDIRECT_URI_PROD", "")

scopes = ["openid","email","profile"]

state_store = FileOAuthStateStore(expiration_seconds=300)

authorize_url_generator = AuthorizeUrlGenerator(
    client_id=SLACK_CLIENT_ID,
    user_scopes=scopes,
    redirect_uri=SLACK_REDIRECT_URI
)


# Create your views here.
class SlackOuthStartView(APIView):
    def get(self,request):
        print("StartView User",request.user)
        state = state_store.issue()
        url = authorize_url_generator.generate(state=state)
        return Response({'url':url})


class SlackOuthRedirectView(APIView):
    def get(self,request):
        print("RedirectView User",request.user)
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')

        if error:
            print(error)
            return Response({"error":f"Error{error}"})

        if not (code and state):
            return Response({"error":"Some problem with installation"})
        
        if not state_store.consume(state):
            return Response({"error":"State value expired"})
        
        try:
            auth_grand_response = WebClient().openid_connect_token(
                                                client_id=SLACK_CLIENT_ID,
                                                client_secret=SLACK_CLIENT_SECRET,
                                                redirect_uri=SLACK_REDIRECT_URI,
                                                code=code
                                            )
            access_token = auth_grand_response.get('access_token')
            user_info_response = WebClient(token=access_token).openid_connect_userInfo()
            user_info = create_user_info(
                            user_info_response=user_info_response,
                        )

        except Exception as e:
            print(e)
            return Response({"Error":"Code potti ...Entha mone ith"})

        try:     
            user_data = update_or_create_user(user=user_info)
            serialized_user_data = UserSerializer(user_data).data
            print(serialized_user_data)
            #update_or_assign_token_response = TokenSerializer(update_or_assign_auth_token(user=user_data,token=access_token)).data
            jwt = generate_jwt(serialized_user_data)
            print(jwt)
        except Exception as e:
            print("Error",e)
            return Response({"message":"success","data":"User creation failed!!"})
        response = Response({"message":"success","data":serialized_user_data}) 
        return set_jwt_cookie(response,jwt)
    


class UserProfileView(TokenAuthRequiredMixin,APIView):
    def get(self,request):
        print("User in Profile view",request.user)
        user = request.user
        print(request.user.slack_id)
        serialised_user = UserSerializer(user)
        return Response({"User-profile":serialised_user.data})