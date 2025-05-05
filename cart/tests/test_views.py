from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from ddf import G
from games.models import Game
from cart.models import Cart, CartItem
from django.contrib.auth.models import User

class CartItemAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = G(User)
        cls.game = G(Game, stock=5, price=100)
        cls.cart = G(Cart, user=cls.user)

        cls.authenticated_client = APIClient()

        user_refresh = RefreshToken.for_user(cls.user)
        cls.user_access = str(user_refresh.access_token)

    def setUp(self):
        # This runs before each test method
        self.authenticated_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
        # Unauthenticated client will be self.client

    def test_create_cart_item(self):
        url = reverse('cart:cart-items-list')
        data = {'game_id': self.game.id, 'quantity': 2}
        response = self.authenticated_client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)

    def test_update_cart_item_quantity(self):
        cart_item = G(CartItem, cart=self.cart, game=self.game, quantity=1)
        url = reverse('cart:cart-items-detail', args=[cart_item.id])
        data = {'quantity': 3}
        response = self.authenticated_client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_delete_cart_item(self):
        cart_item = G(CartItem, cart=self.cart, game=self.game)
        url = reverse('cart:cart-items-detail', args=[cart_item.id])
        response = self.authenticated_client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_create_cart_item_exceed_stock(self):
        url = reverse('cart:cart-items-list')
        data = {'game_id': self.game.id, 'quantity': 11}
        response = self.authenticated_client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('quantity', response.data)


class MergeCartAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = G(User)
        cls.game = G(Game, stock=5, price=100)
        cls.old_session_id = 'guest-session-123'
        cls.guest_cart = G(Cart, session_id=cls.old_session_id, user=None)
        cls.user_cart = G(Cart, user=cls.user)
        cls.guest_item = G(CartItem, cart=cls.guest_cart, game=cls.game, quantity=3)
        cls.user_item = G(CartItem, cart=cls.user_cart, game=cls.game, quantity=2)

        cls.authenticated_client = APIClient()


        cls.user_refresh = RefreshToken.for_user(cls.user)
        cls.user_access = str(cls.user_refresh.access_token)

    def setUp(self):
        # This runs before each test method
        self.authenticated_client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
        # Unauthenticated client will be self.client


    def test_merge_carts_success(self):
        url = reverse('cart:cart-merge')
        response = self.authenticated_client.post(url, {'old_session_id': self.old_session_id})
        self.assertEqual(response.status_code, 200)
        # После merge должно быть только один CartItem в user_cart
        self.user_cart.refresh_from_db()
        merged_item = CartItem.objects.get(cart=self.user_cart, game=self.game)
        self.assertEqual(merged_item.quantity, 5)
        self.assertFalse(Cart.objects.filter(session_id=self.old_session_id, user=None).exists())

    def test_merge_cart_guest_cart_not_found(self):
        url = reverse('cart:cart-merge')
        response = self.authenticated_client.post(url, {'old_session_id': 'nonexistent-session'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)

    def test_merge_cart_missing_session_id(self):
        url = reverse('cart:cart-merge')
        response = self.authenticated_client.post(url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.data)

    def test_merge_cart_quantity_exceeds_stock(self):
        new_game = G(Game, stock=10)
        G(CartItem, cart=self.guest_cart, game=new_game, quantity=4)
        G(CartItem, cart=self.user_cart, game=new_game, quantity=10)

        url = reverse('cart:cart-merge')
        response = self.authenticated_client.post(url, {'old_session_id': self.old_session_id})

        self.assertEqual(response.status_code, 200)
        merged_item = CartItem.objects.get(cart=self.user_cart, game=self.game)
        self.assertEqual(merged_item.quantity, self.game.stock)
        # Гостевая корзина удалена
        self.assertFalse(Cart.objects.filter(session_id=self.old_session_id, user=None).exists())