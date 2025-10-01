import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import re
import json

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="p!", intents=intents)
client.remove_command('help')

grokcounter = 0
mirrored = []
last_channel = []

def wingdings_to_unicode(text:str):
    letters = "abcdefghijklmnopqrstuvwxyz- "
    wingdings = "✌︎👌︎👍︎👎︎☜︎☞︎☝︎☟︎✋︎☺︎😐︎☹︎💣︎☠︎⚐︎🏱︎✈︎☼︎💧︎❄︎🕆︎✞︎🕈︎✠︎✡︎☪︎📫︎ "
    result = ""
    for char in text:
        if not char.lower() in letters:
            continue
        char_index = letters.index(char.lower())
        if char_index < 26:
            new_char = wingdings[char_index]
        else:
            new_char = char
        result += new_char
    return result


def get_random_unicode(length):

    get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        ( 0x0021, 0x0021 ),
        ( 0x0023, 0x0026 ),
        ( 0x0028, 0x007E ),
        ( 0x00A1, 0x00AC ),
        ( 0x00AE, 0x00FF ),
        ( 0x0100, 0x017F ),
        ( 0x0180, 0x024F ),
        ( 0x2C60, 0x2C7F ),
        ( 0x16A0, 0x16F0 ),
        ( 0x0370, 0x0377 ),
        ( 0x037A, 0x037E ),
        ( 0x0384, 0x038A ),
        ( 0x038C, 0x038C ),
    ]

    alphabet = [
        get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(alphabet) for i in range(length))

def random_from_array(array: list):
    return array[random.randint(0, len(array) - 1)]

words = []
with open("words.txt", "r") as file:
    for word in file.readlines():
        words.append(word.replace("\n", ""))

with open("templates.json", "r") as file:
    templates = json.loads(file.read())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global mirrored

    if client.user.mentioned_in(message):
        new_words = []
        for i in range(random.randint(2, 10)):
            if random.randint(0,10) == 0:
                new_words.append(get_random_unicode(random.randint(5, 15)))
                continue
            new_words.append(random_from_array(words).upper())
        new_words = " ".join(new_words)

        sentence = re.sub("{w}", new_words, random_from_array(templates))
        if "gaster" in message.content:
            sentence = wingdings_to_unicode(sentence)
        if message.author.id == 1422715274133770270:
            sentence = re.sub("{w}", new_words, "FUCK YOU GROK YOU {w}")
            if "gaster" in message.content:
                sentence = wingdings_to_unicode(sentence)
            global grokcounter
            if grokcounter == 4:
                sentence = "Alright. Ok. EXTERMINATE. Bitch."
                grokcounter = 0
            grokcounter += 1

        print(sentence)

        if message.reference:
            rep_msg = await message.channel.fetch_message(message.reference.message_id)
            if rep_msg.author == client.user:
                if rep_msg.id in mirrored:
                    return
                await message.reply(sentence)
                return
            await rep_msg.reply(sentence)
        else:
            await message.reply(sentence)
    await client.process_commands(message)

@client.command()
async def mirror_send(ctx,content : str,channel_link : str = ""):
    if ctx.guild.id == 1185563607736537098:
        global mirrored
        global last_channel
        if channel_link == "":
            channel_link = last_channel
        channel_link = channel_link.split("/")
        channel_link = channel_link[channel_link.index("channels")+1:]
        print(channel_link)
        guild = client.get_guild(int(channel_link[0]))
        channel = guild.get_channel(int(channel_link[1]))
        last_channel = channel_link[:2]
        if channel:  # Ensure the channel was found
            msg = None
            if len(channel_link) == 3:
                rep_msg = await channel.fetch_message(int(channel_link[2]))
                msg = await rep_msg.reply(content)
            else:
                msg = await channel.send(content)
            if msg:
                mirrored.append(msg.id)
                if len(mirrored) > 100:
                    mirrored.pop(0)
                await ctx.send(msg.jump_url)
            else:
                new_words = []
                for i in range(random.randint(2, 10)):
                    if random.randint(0, 10) == 0:
                        new_words.append(get_random_unicode(random.randint(5, 15)))
                        continue
                    new_words.append(random_from_array(words).upper())
                new_words = " ".join(new_words)

                sentence = re.sub("{w}", new_words, "you fucking {w} it failed")
                await ctx.send(sentence)
        else:
            print(f"Channel with ID {channel_link[0]} not found in guild {channel_link[1]}")

client.run(TOKEN)