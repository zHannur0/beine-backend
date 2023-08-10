import json

import requests
import re


class AudioService:
    def __init__(self, api_key):
        self.api_key = api_key

    def text_to_speach(self, text, lang):
        audio_urls = []
        url = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": f"{self.api_key}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
        }

        if lang == "kk-KZ":
            voice = "kk-KZ-DauletNeural"
        else:
            voice = "en-US-ChristopherNeural"

        for i in range(5):
            data = f'''<speak version='1.0' xml:lang='{lang}'><voice xml:lang='{lang}' xml:gender='Male' name='{voice}'>{text[f"title{i+1}"] + ",..." + text[f"text{i+1}"] }</voice></speak>'''
            
            data_utf8 = data.encode('utf-8')
            response = requests.post(url, headers=headers, data=data_utf8)

            audio_urls.append(response.content)

        return audio_urls
