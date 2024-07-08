import numpy as np
import cv2
from PIL import Image
import io

def save_image(image_bytes, image_path):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode in ["CMYK", "P"]:
            image = image.convert("RGB")
        image.save(image_path, format="PNG")
        print(f"Saved image {image_path}")
    except Exception as e:
        print(f"Error saving image: {str(e)}")
