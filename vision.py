from google.cloud import vision
from google.cloud.vision import types
import io

def detect_document(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    print(document.text)
    return document.text
