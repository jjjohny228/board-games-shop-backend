from django.urls import path, include
from rest_framework import routers
from cart import views

router = routers.DefaultRouter()
router.register(r'', views.CartItemModelViewSet, basename='cart-items')
app_name = "cart"

urlpatterns = [
    path("", views.CartDestroyAPIView.as_view(), name='cart-remove'),
    path("items/", include(router.urls)),
]