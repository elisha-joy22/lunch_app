from django.urls import include, path
from rest_framework.routers import DefaultRouter
from poll.views import PollModelViewSet



router = DefaultRouter()

router.register(r'',PollModelViewSet,basename='poll')

urlpatterns = [
    path('', include(router.urls)),
    path('active_polls/', PollModelViewSet.as_view({'get':'active_polls'}),name='active-polls')
]
