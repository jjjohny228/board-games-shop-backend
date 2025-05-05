from django.test import TestCase
from ddf import G
from cart.models import Cart, CartItem
from games.models import Game
from cart.serializers import CartSerializer, CartItemSerializer, MergeCartSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class CartSerializerTest(TestCase):
    def test_cart_serializer_output(self):
        user = G(User)
        cart = G(Cart, user=user)
        serializer = CartSerializer(cart)
        self.assertEqual(serializer.data['user'], user.id)

class CartItemSerializerTest(TestCase):
    def setUp(self):
        self.user = G(User)
        self.game = G(Game, stock=5, price=100)
        self.cart = G(Cart, user=self.user)

    def test_cartitem_serializer_output(self):
        cart_item = G(CartItem, cart=self.cart, game=self.game, quantity=2)
        serializer = CartItemSerializer(cart_item)
        self.assertEqual(serializer.data['quantity'], 2)
        self.assertEqual(serializer.data['game'], self.game.id)

    def test_cartitem_quantity_not_exceed_stock(self):
        data = {
            'cart': self.cart.id,
            'game': self.game,
            'quantity': 10  # больше, чем stock
        }
        serializer = CartItemSerializer(data=data, context={'request': None})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class MergeCartSerializerTest(TestCase):
    def test_serializer_valid_data(self):
        data = {'old_session_id': 'abc123'}
        serializer = MergeCartSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['old_session_id'], 'abc123')

    def test_serializer_missing_session_id(self):
        data = {}
        serializer = MergeCartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('old_session_id', serializer.errors)