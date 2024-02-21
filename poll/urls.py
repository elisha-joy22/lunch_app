from django.urls import include, path
from rest_framework.routers import DefaultRouter
from poll.views import PollModelViewSet



router = DefaultRouter()

router.register(r'',PollModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
