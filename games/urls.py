from django.urls import path, include
from rest_framework import routers
from .views import GameModelViewSet

app_name = "games"
router = routers.DefaultRouter()
router.register(r'games', GameModelViewSet, basename='game')

urlpatterns = [
    path("", include(router.urls)),
]