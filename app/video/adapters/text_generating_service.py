import openai


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
            for each text in this query, write text for the query to create a picture that fits the context. Your response should look like JSON:
	            {{
                "prompt1": "Prompt for 1 image",
                "prompt2": "Prompt for 2 image."
                "prompt3": "Prompt for 3 image",
                "prompt4": "Prompt for 4 image",
                "prompt5": "Prompt for 5 image."
                }}""",
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )

        text = response["choices"][0]["text"]
        return text
