import openai
import requests
import json


class TextService:

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_text(self, prompt_text):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""Write explanation text about this request '{prompt_text}' to me in 5 points, your answer should be only about this theme.
        Your answer should look like this in JSON form:
        {{
          "title1": "Title",
          "text1": "Explanation of this title's topic",
          "title2": "Title",
          "text2": "Explanation of this title's topic",
          "title3": "Title",
          "text3": "Explanation of this title's topic",
          "title4": "Title",
          "text4": "Explanation of this title's topic",
          "title5": "Title",
          "text5": "Explanation of this title's topic"
        }}""",
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        text = response["choices"][0]["text"]
        return text
    
    def generate_image_text(self, prompt_text):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""{prompt_text} ->
            For the queries at the top, write good prompts for each text to generate pictures on DALL-E AI.

            Example of other query:
            - Generate a high-quality photo of a model with a futuristic hairstyle, neon makeup, and geometric nail art, inspired by Cyberpunk aesthetics.

            Please add a corresponding negative clue to each prompt to ensure the pictures are visually pleasing and free from errors. Your response should look like JSON:

            {{
             "prompt1": "Prompt for the image of text1 ",
             "prompt2": "Prompt for the second image text2 ",
             "prompt3": "Prompt for the third image text3",
             "prompt4": "Prompt for the fourth image text4",
             "prompt5": "Prompt for the fifth image text5"
            }}""",
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )

        text = response["choices"][0]["text"]
        return text
    
    def translate(self, text):
        text_arr = {}
        json_d = json.loads(text)

        for i in range(5):
            url = "https://backend-project-5m5f.onrender.com/api/translater"
            data = {
                "query": json_d[f'title{i + 1}'],
                "fr": "en",
                "to": "kk",
            }

            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                text_arr[f"title{i+1}"] = result["msg"]
            else:
                return "NO"
            
        for i in range(5):
            url = "https://backend-project-5m5f.onrender.com/api/translater"
            data = {
                "query": json_d[f'text{i + 1}'],
                "fr": "en",
                "to": "kk",
            }

            response = requests.post(url, json=data)

            if response.status_code == 200:
                result = response.json()
                text_arr[f"text{i+1}"] = result["msg"]
            else:
                return "NO"
            
        return text_arr

    def translate_prompt(self, text):
        url = "https://backend-project-5m5f.onrender.com/api/translater"
        data = {
            "query": text,
            "fr": "kk",
            "to": "en",
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["msg"]
        else:
            return "NO"