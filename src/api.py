import random
import openai

class OpenAiAPI:
    def __init__(self, api_key, human_id, bot_id) -> None:
        openai.api_key = api_key
        self.human_id = human_id
        self.bot_id = bot_id

    def fetch_response(self, tokens) -> str:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=tokens,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[f" {self.human_id}:", f" {self.bot_id}:"]
        )

        return random.choice(response["choices"])["text"]