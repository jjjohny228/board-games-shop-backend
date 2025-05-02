from decimal import Decimal

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from carts.models import Cart, CartItem
from games.models import Game
from rest_framework.serializers import ModelSerializer

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        item_quantity = Decimal(validated_data['quantity'])
        cart_item_game = Game.objects.get(id=validated_data['id'])
        if self.context['request'].user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.context['request'].user)
        else:
            cart = Cart.objects.get_or_create(session_id=validated_data['session_id'])

        cart_item = CartItem.objects.create(cart=cart, game=cart_item_game, quantity=item_quantity)
        return cart_item

    def update(self, instance, validated_data):
        item_quantity = validated_data['quantity']
        if item_quantity == '0':
            instance.delete()
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        return instance


    def validate(self, data):
        game_id = data.get('game')
        item_quantity = data.get('quantity')
        cart_item_game = Game.objects.get(id=game_id)
        if item_quantity > cart_item_game.stock:
            raise ValidationError({'quantity': _(f"Quantity cannot exceed available stock ({cart_item_game.stock}).")})

        return data

