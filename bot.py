import os
import requests
from playerdict import playerdict
from operator import itemgetter
import random

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
        userID = ''
        try:
            userID = as_list[1]
        except(IndexError):
            if message.author.name in playerdict.values():
                for id, name in playerdict.items():
                    if name == message.author.name:
                        userID = id
            else:
                await message.channel.send(f"Please enter an ID number. I can't do anything for you without one!")
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
        if message.author.name == "mbridge":
            await message.channel.send('❤️')
        else:
            await message.channel.send('Thank you! 😇')

    if message.author.name == "RibRidge":
        if 'bad bot' not in message.content.lower():
            random_num = random.randint(0,11)
            if random_num % 2 == 0 and random_num % 5 == 0:
                await message.channel.send("SHUT UP RICHARD")
            elif random_num % 2 == 0:
                await message.channel.send("🙄")
            elif random_num % 5 == 0:
                await message.channel.send("😠")

    if 'bad bot' in message.content.lower():
        if message.author.name == "JLemon":
            await message.channel.send('🍋🍋🍋🍋🍋🍋')
        elif message.author.name == "RibRidge":
            await message.channel.send('Go to hell.')
        else:
            await message.channel.send('😭😭😭😭😭😭')

    if '!leaderboard1v1' in message.content:
        leaderboard = {}
        for id in playerdict.keys():
            try:
                ratingresponse = requests.get(
                    'https://aoe2.net/api/player/ratinghistory',
                    params={'game': 'aoe2de',
                            'leaderboard_id': '3',
                            'start': '0',
                            'count': '1',
                            'steam_id': id,
                            }
                )
                onevonedata = ratingresponse.json()
                oneVoneinfo = onevonedata[0]['rating']
                leaderboard[playerdict[id]] = oneVoneinfo
            except(IndexError):
                leaderboard[playerdict[id]] = "No data available"

        playerswithratings = {}

        for key in leaderboard.keys():
            if type(leaderboard[key]) == int:
                playerswithratings[key] = leaderboard[key]

        pwr_sorted = sorted(playerswithratings.items(), key=itemgetter(1), reverse=True)
        for tup in pwr_sorted:
            await message.channel.send(f'{tup[0]}: {tup[1]}')

    elif '!leaderboardtg' in message.content:
        leaderboard = {}
        for id in playerdict.keys():
            try:
                ratingresponse = requests.get(
                    'https://aoe2.net/api/player/ratinghistory',
                    params={'game': 'aoe2de',
                            'leaderboard_id': '4',
                            'start': '0',
                            'count': '1',
                            'steam_id': id,
                            }
                )
                tgdata = ratingresponse.json()
                tginfo = tgdata[0]['rating']
                leaderboard[playerdict[id]] = tginfo
            except(IndexError):
                leaderboard[playerdict[id]] = "No data available"

        playerswithratings = {}

        for key in leaderboard.keys():
            if type(leaderboard[key]) == int:
                playerswithratings[key] = leaderboard[key]

        pwr_sorted = sorted(playerswithratings.items(), key=itemgetter(1), reverse=True)
        for tup in pwr_sorted:
            await message.channel.send(f'{tup[0]}: {tup[1]}')

    elif '!leaderboard' in message.content:
        await message.channel.send('Do you want "!leaderboard1v1" or "!leaderboardtg"?')

bot.run(TOKEN)
