import os
import discord
from dotenv import load_dotenv
import random
import re

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def random_from_array(array: list):
    return array[random.randint(0, len(array) - 1)]

words = []
with open("words.txt", "r") as file:
    for word in file.readlines():
        words.append(word.replace("\n", ""))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        new_words = []
        for i in range(random.randint(2, 10)):
            new_words.append(random_from_array(words).upper())
        new_words = " ".join(new_words)

        sentence = re.sub("{w}", new_words, "SHUT YO {w} AHH")

        print(sentence)

        if message.reference:
            rep_msg = await message.channel.fetch_message(message.reference.message_id)
            await rep_msg.reply(sentence)
        else:
            await message.reply(sentence)

client.run(TOKEN)