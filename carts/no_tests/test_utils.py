import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def create_image(height: int, width: int) -> SimpleUploadedFile:
    # Creates image with different sizes for no_tests
    valid_image = Image.new('RGB', (height, width), color='white')
    buffer = io.BytesIO()
    valid_image.save(buffer, format='JPEG')
    image_data = buffer.getvalue()
    return SimpleUploadedFile('cover.jpg', image_data, content_type='image/jpg')