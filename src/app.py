import os
import discord
from discord.ext import commands

from api import OpenAiAPI

class Constants:
    # Global
    HUMAN_ID="HUMAN"
    BOT_ID="BOT"
    INITIAL_PROMPT="The following is a conversation with a very knowledgeable bot. This bot is condescending, sarcastic and knows about everything."
    INITIAL_MESSAGE=f"\n{HUMAN_ID}: Hey, who are you?\n{BOT_ID}: I'm the all knowing and the all seeing Santa.\n{HUMAN_ID}: They tell me you know everything.\n{BOT_ID}: Indeed child, I know anything and everything. Ho Ho Ho."
    # Server Specific
    CHANNEL_ID=1014647460393664512 # TODO

class Runtime:
    CHAT_HISTORY=""+Constants.INITIAL_PROMPT+Constants.INITIAL_MESSAGE

def main():
    # Initial setup
    api = OpenAiAPI(
        api_key=os.environ.get('OPENAI_API_KEY'),
        human_id=Constants.HUMAN_ID,
        bot_id=Constants.BOT_ID
    )

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$$', description="", intents=intents)


    # Define commands/events
    @bot.event
    async def on_ready():
        print(f'[INFO] Logged in as {bot.user}')

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

        if message.channel.id != Constants.CHANNEL_ID: return
        if not str(message.content).startswith('.'): return
        
        # Add message to chat history
        Runtime.CHAT_HISTORY += f"\n{Constants.HUMAN_ID}: {str(message.content)[1:]}" # exclude .
        response = api.fetch_response(Runtime.CHAT_HISTORY)
        Runtime.CHAT_HISTORY += response
        
        # Send response to channel
        await message.channel.send(response.split(Constants.BOT_ID)[-1][1:].strip())

    @bot.command()
    async def clear(ctx):
        Runtime.CHAT_HISTORY = ""+Constants.INITIAL_PROMPT+Constants.INITIAL_MESSAGE
        print("[INFO] Chat History Cleared")

    # Run bot
    bot.run(os.environ.get('DISCORD_BOT_TOKEN'))



if __name__ == "__main__":
    main()

