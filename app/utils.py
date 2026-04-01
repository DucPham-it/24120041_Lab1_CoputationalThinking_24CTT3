import base64
from io import BytesIO

from PIL import Image


def validate_prompt(prompt: str) -> None:
    if not prompt or not prompt.strip():
        raise ValueError("Prompt is empty")

    if len(prompt) > 1000:
        raise ValueError("Prompt too long (max 1000 chars)")


def validate_image_options(height: int, width: int) -> None:
    if height % 64 != 0 or width % 64 != 0:
        raise ValueError("Height and width must be multiples of 64")

    if height * width > 1280 * 1280:
        raise ValueError("Image size is too large for this API")


def image_to_base64(image: Image.Image, image_format: str = "PNG") -> str:
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
