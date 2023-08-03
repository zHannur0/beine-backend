import json
import openai
import requests
from PIL import Image
from io import BytesIO


class ImageService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def text_to_image(self, text):
        images = []
        json_d = json.loads(text)
        
        for i in range(5):
            response = openai.Image.create(
                prompt=json_d[f'prompt{i + 1}'],
                n=1,
                size="512x512"
            )        
            images.append(response['data'][0]['url'])

        return images
    
    def convert_url_to_image(self, image_url):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            return image
        except Exception as e:
            print(f"Error converting URL to image: {e}")
            return None