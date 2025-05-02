import os
import shutil
import tempfile
from decimal import Decimal
from unittest.mock import patch
from uuid import UUID

from ddf import G
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from django.test import TestCase
from django.test import override_settings

from games.models import game_image_upload_to, Game, Image, FileSizeValidator, Review
from games.tests.test_utils import create_image

# Create a temporary file directory for testing
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FileUploadToTest(TestCase):
    """
    Test case for the release_upload_to() used by Release model
    to dynamically generate a filepath for each Release object.

    """

    @classmethod
    def setUpTestData(cls):
        # Create a Release object for testing
        cls.user = G(User)
        cls.cover = 'cover.jpg'
        cls.game = G(Game)
        cls.image = G(Image, game=cls.game)
        cls.generated_path = game_image_upload_to(cls.image, cls.cover)
        cls.expected_path = f'games/{cls.image.game.id}_{cls.image.game.title}/'

    def test_it_generates_correct_file_path_to_file(self):
        self.assertTrue(self.generated_path.startswith(self.expected_path))

    def test_it_contains_game_id_in_path(self):
        self.assertIn(str(self.game.id), self.generated_path)

    @patch('games.models.uuid4')
    def test_in_release_upload_to(self, mock_uuid4):
        mock_uuid4.return_value = UUID('747e99f7-35d9-d4dc-436a-0f8b4be52f1b')
        expected_prefix = '0f8b4be52f1b.jpg'
        expected_output = f'games/{self.game.id}_{self.game.title}/{expected_prefix}'
        generated_path = game_image_upload_to(self.image, self.cover)
        self.assertEqual(generated_path, expected_output)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Очистка медиафайлов, удаление временных директорий и т.п.
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


class FileSizeValidatorTest(TestCase):
    """
    Test FileSizeValidator for validating the uploaded file sizes
    of cover and sample fields of the of releases.

    """

    def test_valid_image_file_size(self):
        size_validator = FileSizeValidator(5 * 1024 * 1024)  # 5 MB
        valid_cover = create_image(800, 800)
        self.assertIsNone(size_validator(valid_cover))  # Should not raise ValidationError

    def test_it_returns_validation_error_for_large_sample_size(self):
        sample_validator = FileSizeValidator(10 * 1024 * 1024)  # 10 MB
        large_cover = SimpleUploadedFile('cover.jpg', b'image content' * (16 * 1024 * 1024), content_type='image/jpg')
        with self.assertRaisesMessage(ValidationError, 'The maximum file size must be less than 10.0 MB'):
            sample_validator(large_cover)


class ReviewTest(TestCase):
    def test_rating_validation(self):
        user = G(User)
        game = G(Game)
        review = Review.objects.create(user=user, game=game, rating=Decimal("6.0"))
        with self.assertRaises(ValidationError) as ctx:
            review.full_clean()
            print(ctx.exception.messages)
            # self.assertIn()


class GameTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.game = G(Game, title="Chess", price=Decimal("29.99"), discount_price=None)

    def test_str_representation(self):
        self.assertEqual(str(self.game), "Chess")

    def test_discount_price_defaults_to_price(self):
        self.game.save()
        self.assertEqual(self.game.discount_price, self.game.price)

    def test_get_average_rating_no_reviews(self):
        self.assertEqual(self.game.get_average_rating, 0.0)

    def test_get_average_rating_with_reviews(self):
        user = G(User)
        G(Review, game=self.game, user=user, rating=Decimal("3.0"))
        G(Review, game=self.game, user=user, rating=Decimal("5.0"))
        self.assertEqual(self.game.get_average_rating, 4.0)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        image_path = SimpleUploadedFile("valid.png", b"data", content_type="image/png")
        cls.valid_image = G(Image, path=image_path)

    def test_it_saves_cover_correct_file_extention(self):
        expected_extension = 'png'
        actual_extension = self.valid_image.path.path.split('.')[-1]
        self.assertEqual(expected_extension, actual_extension)

    def test_valid_image_extension_passes(self):
        self.assertIsNone(self.valid_image.full_clean())

    def test_invalid_image_extension_raises(self):
        invalid_image = SimpleUploadedFile("file.txt", b"data", content_type="text/plain")
        image = G(Image, path=invalid_image)
        with self.assertRaises(ValidationError):
            image.full_clean()

    def test_it_returns_error_for_not_allowed_image_file_formats(self):
        invalid_image = SimpleUploadedFile('file.txt', b'large image content', content_type='text/plain')
        validator = FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_FILE_EXTENSIONS)
        with self.assertRaises(ValidationError):
            validator(invalid_image)

    def test_it_returns_error_for_not_allowed_image_file_sizes(self):
        invalid_image = SimpleUploadedFile('large_image.jpeg', b'large image content' * 30 * 1024 * 1024, content_type='image/jpeg')
        validator = FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_FILE_EXTENSIONS)
        with self.assertRaises(ValidationError):
            validator(invalid_image)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Очистка медиафайлов, удаление временных директорий и т.п.
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)



