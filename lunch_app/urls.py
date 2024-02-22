from django.contrib import admin
from django.urls import path,include
from lunch_app.health_check import health_check
from accounts.views import HomeView

urlpatterns = [
    path('health_check',health_check,name="health-check"),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('polls/', include('poll.urls'))
]