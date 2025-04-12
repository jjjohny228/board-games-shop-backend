from django.db import models
from rest_framework.authtoken.admin import User

from games.models import Game


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_total(self):
        items = self.cart_items.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_cart_quantity_items(self):
        items = self.cart_items.all()
        total = sum([item.quantity for item in items])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)

    @property
    def get_total(self):
        return self.game.price * self.quantity
