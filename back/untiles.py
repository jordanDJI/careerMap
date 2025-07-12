import base64
# from pdf2image import convert_from_path
import os
from uuid import uuid4


def pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)

    output_dir = "temp_images"
    os.makedirs(output_dir, exist_ok=True)

    image_filename = os.path.join(output_dir, f"{uuid4().hex}.jpg")
    print(f"Image location: {image_filename}")
    
    images[0].save(image_filename, 'JPEG')
    return image_filename


def image_to_base64(image_filename):
    with open(image_filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")