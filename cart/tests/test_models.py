from decimal import Decimal
from django.test import TestCase
from ddf import G
from cart.models import Cart, CartItem
from games.models import Game
from django.contrib.auth.models import User

class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = G(User)
        cls.game = G(Game, price=Decimal('100.00'))
        cls.cart = G(Cart, user=cls.user)
        cls.cart_item = G(CartItem, cart=cls.cart, game=cls.game, quantity=2)

    def test_update_cart_total(self):
        self.cart.update_cart_total()
        self.assertEqual(self.cart.total, self.cart_item.get_total)

    def test_update_cart_total_quantity(self):
        self.cart.update_cart_total_quantity()
        self.assertEqual(self.cart.total_quantity, self.cart_item.quantity)

    def test_cartitem_get_total(self):
        self.assertEqual(self.cart_item.get_total, self.game.price * self.cart_item.quantity)

    def test_cart_str(self):
        self.assertIsInstance(str(self.cart), str)

    def test_cartitem_str(self):
        self.assertIsInstance(str(self.cart_item), str)
