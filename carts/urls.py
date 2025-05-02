from django.urls import path, include
from rest_framework import routers
from carts import views

app_name = "carts"

urlpatterns = [
    path("", views.CartListApiView.as_view(), name='cart-list'),
    path("<int:cart_id>/", views.CartRetrieveAPIView.as_view(), name='cart-detail'),
    path("<int:cart_id>/items/", views.CartItemCreateAPIView.as_view(), name='cart-item-create'),
    path("<int:cart_id>/items/<int:cart_item_id>/", views.CartItemUpdateDeleteAPIView.as_view(), name='cart-item-detail'),
]