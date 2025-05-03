import tempfile
from datetime import datetime
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ddf import G
from types import SimpleNamespace

from games.models import Game, Genre, Type, Mechanic, Publisher, DifficultyLevel, PlayerCount, AgeGroup, Duration, Image
from games.serializers import GameSerializer, GenreSerializer, ImageSerializer
from games.tests.test_utils import create_image


class GenreSerializerTest(TestCase):
    def test_genre_serializer_output(self):
        genre = G(Genre, name="Strategy")
        serializer = GenreSerializer(genre)
        self.assertEqual(serializer.data["name"], "Strategy")


class ImageSerializerTest(TestCase):
    def test_image_serializer_output(self):
        game = G(Game)
        image = G(Image, game=game)
        serializer = ImageSerializer(image)
        self.assertIn("path", serializer.data)


class GameSerializerTest(TestCase):
    def setUp(self):
        self.publisher = G(Publisher, name="Test Publisher")
        self.genre = G(Genre)
        self.type = G(Type)
        self.mechanic = G(Mechanic)
        self.difficulty = G(DifficultyLevel)
        self.player_count = G(PlayerCount)
        self.age_group = G(AgeGroup)
        self.duration = G(Duration)

        self.image_file = create_image(200, 500)

    def test_create_game_serializer(self):
        data = {
            "title": "Test Game",
            "description": "Test description",
            "rules_summary": "Rules summary",
            "release_year": datetime.now().year,
            "price": "99.99",
            "discount_price": "79.99",
            "stock": 10,
            "difficulty_id": self.difficulty.pk,
            "player_count_id": self.player_count.pk,
            "age_group_id": self.age_group.pk,
            "duration_id": self.duration.pk,
            "genre_ids": [self.genre.pk],
            "type_ids": [self.type.pk],
            "mechanic_ids": [self.mechanic.pk],
            "publisher_name": self.publisher.name,
            "images": [self.image_file],
        }

        fake_request = SimpleNamespace(method="POST")
        serializer = GameSerializer(data=data, context={"request": fake_request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        game = serializer.save()

        self.assertEqual(game.title, "Test Game")
        self.assertEqual(game.genre.count(), 1)
        self.assertTrue(game.images.exists())

    def test_invalid_release_year(self):
        data = {
            "title": "Old Game",
            "release_year": 1700,  # invalid year
            "price": "50.00",
            "discount_price": "40.00",
            "stock": 5,
            "difficulty_id": self.difficulty.pk,
            "player_count_id": self.player_count.pk,
            "age_group_id": self.age_group.pk,
            "duration_id": self.duration.pk,
            "genre_ids": [self.genre.pk],
            "type_ids": [self.type.pk],
            "mechanic_ids": [self.mechanic.pk],
            "publisher_name": self.publisher.name,
        }

        serializer = GameSerializer(data=data, context={"request": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("release_year", serializer.errors)

    def test_missing_required_fields(self):
        data = {
            "title": "Incomplete Game",
            "release_year": datetime.now().year,
            "price": "30.00",
            "discount_price": "20.00",
            "stock": 0,
            "difficulty_id": self.difficulty.pk,
            "player_count_id": self.player_count.pk,
            "age_group_id": self.age_group.pk,
            "duration_id": self.duration.pk,
            "publisher_name": self.publisher.name,
        }

        serializer = GameSerializer(data=data, context={"request": type("Req", (), {"method": "POST"})()})
        self.assertFalse(serializer.is_valid())
        self.assertIn("genre_ids", serializer.errors)
        self.assertIn("mechanic_ids", serializer.errors)
        self.assertIn("type_ids", serializer.errors)
