import os
import base64

import requests

url = "http://127.0.0.1:8000/predict"

data = {
    "prompt": "anime girl, smiling, red eyes, green hair, white shirt",
    "negative_prompt": "bad quality, low resolution, blurry",
    "num_inference_steps": 30,
    "guidance_scale": 5.5,
    "height": 576,
    "width": 576,
    "num_images": 3,
    "seed": 42,
}

response = requests.post(url, json=data, timeout=600)
response.raise_for_status()

result = response.json()
os.makedirs("images", exist_ok=True)

image_base64 = result["data"]["images"][0]["base64"]

with open("images/generated_image.png", "wb") as image_file:
    image_file.write(base64.b64decode(image_base64))

print("Saved image to images/generated_image.png")
