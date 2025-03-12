import os
from mistralai import Mistral
from openai import OpenAI
import discord

import os
import discord
from discord.ext import commands

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are a helpful tutor who assists students with quizzes, notes, and study materials."
MISTRAL_MODEL = "mistral-large-latest"
OPENAI_MODEL = "gpt-4o"


class Agent:
    def __init__(self):
        # MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

        # self.client = Mistral(api_key=MISTRAL_API_KEY)
        self.client = OpenAI(api_key=OPENAI_TOKEN)

    async def run(self, message: str):
        # The simplest form of an agent
        # Send the message's content to Mistral's API and return Mistral's response

        # messages = [
        #     {"role": "system", "content": SYSTEM_PROMPT},
        #     {"role": "user", "content": message},
        # ]

        # response = await self.client.chat.complete_async(
        #     model=MISTRAL_MODEL,
        #     messages=messages,
        # )

        # return response.choices[0].message.content

        completion = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ]
        )

        return completion.choices[0].message.content
