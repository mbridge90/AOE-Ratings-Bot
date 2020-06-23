import os
import random
import requests
from playerdict import playerdict

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

    if '!rating' in message.content:
        as_list = message.content.split()
        try:
            userID = as_list[1]
        except(IndexError):
            await message.channel.send(f"Please enter an ID number. I can't do anything without one yet!")
            return
        if userID not in playerdict.keys():
            await message.channel.send(
                f"Sorry, I can't find any information for that ID ({userID}). 😳 \nMaybe there's a mistake in it? ")

        else:
            try:
                TGresponse = requests.get(
                    'https://aoe2.net/api/player/ratinghistory',
                    params={'game': 'aoe2de',
                            'leaderboard_id': '4',
                            'start': '0',
                            'count': '1',
                            'steam_id': userID,
                            }
                )
                if TGresponse.status_code == 200:
                    TGdata = TGresponse.json()
                    TGinfo = TGdata[0]['rating']

            except(IndexError):
                TGinfo = 'No data available'

            try:
                onevoneresponse = requests.get(
                    'https://aoe2.net/api/player/ratinghistory',
                    params={'game': 'aoe2de',
                            'leaderboard_id': '3',
                            'start': '0',
                            'count': '1',
                            'steam_id': userID,
                            }
                )
                onevonedata = onevoneresponse.json()
                oneVoneinfo = onevonedata[0]['rating']
            except(IndexError):
                oneVoneinfo = 'No data available'

            await message.channel.send(f'Player: {playerdict[userID]}\n1v1: {oneVoneinfo}\nTG: {TGinfo}')

    if 'good bot' in message.content.lower():
        await message.channel.send('Thank you! 😇')

    if 'bad bot' in message.content.lower():
        if message.author == "JLemon":
            await message.channel.send('🍋🍋🍋🍋🍋🍋')
        else:
            await message.channel.send('😭😭😭😭😭😭')


bot.run(TOKEN)
