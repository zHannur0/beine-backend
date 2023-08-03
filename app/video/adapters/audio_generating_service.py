import json

import requests
import re


class AudioService:
    def __init__(self, api_key, api_userid):
        self.api_key = api_key
        self.api_userid = api_userid

    def text_to_speach(self, text):
        audio_url = "https://play.ht/api/v2/tts"
        audio_urls = []
        json_d = json.loads(text)

        for i in range(5):
            payload = {
                "text": json_d[f'title{i + 1}'] + ",... " + json_d[f'text{i + 1}'],
                "voice": "larry",
                "quality": "medium",
                "output_format": "mp3",
                "speed": 1,
                "sample_rate": 24000,
                "seed": None,
                "temperature": None
            }

            headers = {
                "accept": "text/event-stream",
                "content-type": "application/json",
                "AUTHORIZATION": f"Bearer {self.api_key}",
                "X-USER-ID": f"{self.api_userid}"
            }

            response = requests.post(audio_url, json=payload, headers=headers)

            match = re.search(r'"url":"(.*?)"', response.text)
            url_aud = match.group(1)

            audio_urls.append(url_aud)

        return audio_urls
