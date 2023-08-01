import json
import openai


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