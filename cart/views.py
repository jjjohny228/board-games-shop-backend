from jsonschema.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from games.models import Game


class CartDestroyAPIView(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            carts = Cart.objects.filter(user=user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.save()
                session_id = request.session.session_key
            carts = Cart.objects.filter(session_id=session_id)
        if carts.exists():
            carts.delete()
            return Response({'detail': _('Cart was successfully deleted')}, status=204)
        raise ValidationError(_('This user does not have a cart'))


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        request = self.request
        data = request.data
        item_quantity = data.get('quantity')
        game_id = data.get('game')  # Обычно приходит как id
        session_id = self.request.session.session_key

        # Получаем игру
        game = get_object_or_404(Game, id=game_id)

        # Определяем корзину
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart, _ = Cart.objects.get_or_create(session_id=session_id)

        # Создаём CartItem
        cart_item = CartItem.objects.create(cart=cart, game=game, quantity=item_quantity)

        # Обновляем корзину
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()

        # Возвращаем сериализованный объект
        serializer.instance = cart_item

class CartItemUpdateDeleteAPIView(UpdateAPIView, DestroyAPIView):
    serializer_class = CartItemSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        item_quantity = request.data.get('quantity')

        if item_quantity == '0':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        cart = instance.cart
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()

    def perform_destroy(self, instance):
        cart = instance.cart
        instance.delete()
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()


class CartItemModelViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user)
        session_id = self.request.session.session_key
        return CartItem.objects.filter(cart__session_id=session_id)

    def perform_create(self, serializer):
        request = self.request
        data = request.data
        item_quantity = data.get('quantity')
        game_id = data.get('game')
        session_id = self.request.session.session_key

        game = get_object_or_404(Game, id=game_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart, _ = Cart.objects.get_or_create(session_id=session_id)

        cart_item = CartItem.objects.create(cart=cart, game=game, quantity=item_quantity)
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()
        serializer.instance = cart_item

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        item_quantity = request.data.get('quantity')

        if str(item_quantity) == '0':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        cart = instance.cart
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()

    def perform_destroy(self, instance):
        cart = instance.cart
        instance.delete()
        cart.update_cart_total()
        cart.update_cart_total_quantity()
        cart.save()


