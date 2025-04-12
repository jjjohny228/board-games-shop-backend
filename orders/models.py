import re

from django.db import models
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import ValidationError

from games.models import Game


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    status = models.CharField(max_length=20, default='pending', choices=ORDER_STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_order_total(self):
        items = self.order_items.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_order_quantity_items(self):
        items = self.order_items.all()
        total = sum([item.quantity for item in items])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    @property
    def get_total(self):
        return self.game.price * self.quantity


class Shipment(models.Model):
    def validate_zipcode(value):
        if not re.fullmatch(r'^\d{5}(-\d{4})?$', value):
            raise ValidationError("Введите корректный ZIP-код.")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipments")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10, validators=[validate_zipcode])
