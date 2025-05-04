from rest_framework.test import APITestCase
from django.urls import reverse
from ddf import G
from games.models import Game
from cart.models import Cart, CartItem
from django.contrib.auth.models import User

class CartItemAPITest(APITestCase):
    def setUp(self):
        self.user = G(User)
        self.game = G(Game, stock=5, price=100)
        self.client.force_authenticate(user=self.user)
        self.cart = G(Cart, user=self.user)

    def test_create_cart_item(self):
        url = reverse('cart:cart-items-list')
        data = {'game': self.game.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)

    def test_update_cart_item_quantity(self):
        cart_item = G(CartItem, cart=self.cart, game=self.game, quantity=1)
        url = reverse('cart:cart-items-detail', args=[cart_item.id])
        data = {'quantity': 3}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_delete_cart_item(self):
        cart_item = G(CartItem, cart=self.cart, game=self.game)
        url = reverse('cart:cart-items-detail', args=[cart_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_create_cart_item_exceed_stock(self):
        url = reverse('cart:cart-items-list')
        data = {'game': self.game.id, 'quantity': 11}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('quantity', response.data)
