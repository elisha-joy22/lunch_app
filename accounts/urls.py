from django.urls import path
from accounts import views

urlpatterns = [
    path('user/oauth/start',views.SlackOuthStartView.as_view(), name='oauth-start'),
    path('user/oauth/redirect', views.SlackOuthRedirectView.as_view(), name='oauth-redirect'),
    path('user/profile', views.UserProfileView.as_view(), name='user-profile'),
    path('user/logout', views.LogoutView.as_view(), name="user-logout"),
    path('user/sign-in', views.SignInView.as_view(), name='user-sign-in')
]