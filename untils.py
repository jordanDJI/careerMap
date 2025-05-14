import base64
from pdf2image import convert_from_path
import os
from uuid import uuid4

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    image_filename = f"/tmp/{uuid4().hex}.jpg"
    images[0].save(image_filename, 'JPEG')
    return image_filename
