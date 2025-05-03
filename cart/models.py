from django.db import models
from django.contrib.auth.models import User
from django.template.context_processors import request

from games.models import Game


class Cart(models.Model):
    session_id = models.CharField(max_length=244, null=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_cart_total(self):
        items = self.cart_items.all()
        self.total = sum([item.get_total for item in items])

    def update_cart_total_quantity(self):
        items = self.cart_items.all()
        self.total_quantity = sum([item.quantity for item in items])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField()

    @property
    def get_total(self):
        return self.game.price * self.quantity
