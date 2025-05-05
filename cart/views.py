from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer, MergeCartSerializer
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
            return Response(status=204)
        raise ValidationError(_('This user does not have a cart'))


class CartItemModelViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.none() # line for swagger
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CartItem.objects.filter(cart__user=user)
        print('Old session', self.request.session.session_key)
        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.save()
            session_id = self.request.session.session_key
        return CartItem.objects.filter(cart__session_id=session_id)

    def perform_create(self, serializer):
        data = self.request.data
        item_quantity = data.get('quantity')
        game_id = data.get('game_id')
        session_id = self.request.session.session_key

        game = get_object_or_404(Game, id=game_id)

        if self.request.user.is_authenticated:
            cart, is_created = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart, is_created = Cart.objects.get_or_create(session_id=session_id)

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


class MergeCartAPIView(APIView):
    serializer_class = MergeCartSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        old_session_id = request.data.get('old_session_id')
        user = request.user

        if not old_session_id:
            return Response({'detail': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        guest_cart = Cart.objects.filter(session_id=old_session_id, user=None)
        if not guest_cart.exists():
            return Response({'detail': 'Guest cart not found'}, status=status.HTTP_404_NOT_FOUND)
        guest_cart = guest_cart.first()

        user_cart, _ = Cart.objects.get_or_create(user=user)

        # Индекс CartItem по game_id для user_cart
        user_cart_items = {item.game_id: item for item in user_cart.cart_items.all()}

        for guest_item in guest_cart.cart_items.all():
            if guest_item.game.id in user_cart_items:
                user_item = user_cart_items[guest_item.game.id]
                user_and_quest_quantity = user_item.quantity + guest_item.quantity
                user_item.quantity = user_and_quest_quantity if user_and_quest_quantity <= user_item.game.stock else user_item.game.stock
                user_item.save()
            else:
                guest_item.cart = user_cart
                guest_item.save()

        guest_cart.delete()

        user_cart.update_cart_total()
        user_cart.update_cart_total_quantity()
        user_cart.save()

        return Response({'detail': 'Carts merged successfully'}, status=status.HTTP_200_OK)