import os
import random
import openai


class Constants:
    HUMAN_ID="HUMAN"
    BOT_ID="BOT"
    INITIAL_PROMPT="The following is a conversation with a very knowledgeable bot. This bot is condescending, sarcastic and knows about everything."
    INITIAL_MESSAGE=f"\n{HUMAN_ID}: Hey, who are you?\n{BOT_ID}: I'm the all knowing and the all seeing Santa.\n{HUMAN_ID}: They tell me you know everything.\n{BOT_ID}: Indeed child, I know anything and everything. Ho Ho Ho."

class Runtime:
    CHAT_HISTORY=""+Constants.INITIAL_PROMPT+Constants.INITIAL_MESSAGE

def setup():
    openai.api_key = os.getenv("OPENAI_API_KEY")

def app():
    pass

def test_api():
    setup()

    message = str(input("ENTER MSG: "))
    Runtime.CHAT_HISTORY += f"\n{Constants.HUMAN_ID}: {message}"

    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=Runtime.CHAT_HISTORY,
      temperature=0.9,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.6,
      stop=[f" {Constants.HUMAN_ID}:", f" {Constants.BOT_ID}:"]
    )

    Runtime.CHAT_HISTORY += random.choice(response["choices"])["text"]

    print(Runtime.CHAT_HISTORY)

if __name__ == "__main__":
    test_api()