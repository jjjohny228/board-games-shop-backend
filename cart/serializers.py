from decimal import Decimal

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cart.models import Cart, CartItem
from games.models import Game
from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart']


    def validate(self, data):
        request = self.context['request']
        item_quantity = data.get('quantity')
        cart_item_game = self.instance.game if request.method == 'PUT' else data.get('game')
        if cart_item_game and item_quantity > cart_item_game.stock:
            raise ValidationError(
                {'quantity': _(f'Quantity cannot exceed available stock ({cart_item_game.stock}).')})
        return data


class MergeCartSerializer(serializers.Serializer):
    old_session_id = serializers.CharField(required=True)
