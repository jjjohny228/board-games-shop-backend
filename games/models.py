import re
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    """
    A validator class for checking the size of uploaded files.

    """

    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: UploadedFile) -> None:
        filesize = value.size
        if filesize > self.max_size:
            raise ValidationError(
                _(f"The maximum file size must be less than {self.max_size / (1024 * 1024)} MB")
            )


def game_image_upload_to(instance: "Image", filename: str) -> str:
    """
    Generates a unique file path for uploaded files.
    The file will be saved to MEDIA_ROOT/releases/release.title/unique_uuid_string+filename.
    """

    ext = filename.split(".")[-1]
    file_prefix = str(uuid4()).split("-")[4]
    filename = f"{file_prefix}.{ext}"
    return f"games/{instance.game.id}_{instance.game.title}/{filename}"


class Review(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    rules_summary = models.TextField(blank=True)
    release_year = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="games"
    )
    type = models.ManyToManyField("Type", related_name="games")
    player_count = models.ForeignKey(
        "PlayerCount", on_delete=models.PROTECT, related_name="games"
    )
    age_group = models.ForeignKey(
        "AgeGroup", on_delete=models.PROTECT, related_name="games"
    )
    difficulty = models.ForeignKey(
        "DifficultyLevel", on_delete=models.PROTECT, related_name="games"
    )
    genre = models.ManyToManyField("Genre", related_name="games")
    mechanic = models.ManyToManyField(
        "Mechanic", related_name="games"
    )
    duration = models.ForeignKey(
        "Duration", on_delete=models.PROTECT, related_name="games"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.discount_price is None:
            self.discount_price = self.price
        super().save(*args, **kwargs)


class Image(models.Model):
    game = models.ForeignKey(Game, related_name="images", on_delete=models.CASCADE)
    path = models.ImageField(
        upload_to=game_image_upload_to,
        validators=[
            FileExtensionValidator(settings.ALLOWED_IMAGE_FILE_EXTENSIONS),
            FileSizeValidator(settings.MAX_IMAGE_FILE_SIZE),
        ],
    )

    def __str__(self):
        return str(self.path)


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PlayerCount(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AgeGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Mechanic(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Duration(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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

