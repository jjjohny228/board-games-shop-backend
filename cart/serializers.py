from decimal import Decimal

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cart.models import Cart, CartItem
from games.models import Game
from games.serializers import GameSerializer
from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'price', 'discount_price']


class CartItemSerializer(serializers.ModelSerializer):
    game = CartItemGameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(), source='game', write_only=True, required=True, many=False
    )
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['cart']


    def validate(self, data):
        request = self.context['request']
        item_quantity = data.get('quantity')
        print('Some if ', request.data, data)
        cart_item_game = self.instance.game if request.method in ['PUT', 'PATCH'] else data.get('game')
        if item_quantity > cart_item_game.stock:
            raise ValidationError(
                {'quantity': _(f'Quantity cannot exceed available stock ({cart_item_game.stock}).')})
        return data


class MergeCartSerializer(serializers.Serializer):
    old_session_id = serializers.CharField(required=True)
