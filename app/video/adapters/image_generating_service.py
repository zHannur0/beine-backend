import json
import requests


class ImageService:
    def __init__(self, api_key):
        self.api_key = api_key

    def text_to_image(self, text):
        images = []
        json_d = json.loads(text)
        url = 'https://api.getimg.ai/v1/stable-diffusion/text-to-image'
        access_token = self.api_key
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        for i in range(5):
            data = {
                'model': 'stable-diffusion-v1-5',
                'prompt': json_d[f'prompt{i + 1}'],
                'negative_prompt': "Disfigured, cartoon, blurry, bad anatomy, bad proportions, cloned face, cropped, deformed, dehydrated, disfigured, duplicate, error, extra arms, extra fingers, extra legs, extra limbs, fused fingers, gross proportions, jpeg artifacts, long neck, low quality, lowres, malformed limbs, missing arms, missing legs, morbid, mutated hands, mutation, mutilated, out of frame, poorly drawn face, poorly drawn hands, signature, text, too many fingers, ugly, username, watermark, worst quality, distorted colors",
                'width': 500,
                'height': 500,
                'steps': 25,
                'guidance': 7.5,
                'seed': 42,
                'scheduler': 'dpmsolver++',
                'output_format': 'jpeg'
            }

            response = requests.post(url, headers=headers, json=data)

            images.append(response.json()['image'])

        return images