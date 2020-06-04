import os
import random
import requests

import discord
from dotenv import load_dotenv

from discord.ext import commands



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'rating!' in message.content:
        as_list = message.content.split()
        userID = as_list[1]
        response = requests.get(
            'https://aoe2.net/api/player/ratinghistory',
            params={'game': 'aoe2de',
                    'leaderboard_id': '4',
                    'start': '0',
                    'count': '1',
                    'steam_id': userID,
                    }
        )
        data = response.json()
        await message.channel.send(data[0]['rating'])

bot.run(TOKEN)