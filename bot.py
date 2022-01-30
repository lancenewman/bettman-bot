# bot.py
import os
import sys
import discord
import requests
from dotenv import load_dotenv
from datetime import date
from dateutil import parser, tz


def get_game_info():
    today = date.today()
    params = (
        ('teamId', '18'),
        ('date', today.strftime('%Y-%m-%d'))
    )
    response = requests.get(
        "https://statsapi.web.nhl.com/api/v1/schedule", params=params)
    return response.json()


def game_message():
    game_info = get_game_info()

    if len(game_info['dates']) < 1:
        return "There's no game today <:feelsbadpekka:802031362767847446>"

    game = game_info['dates'][0]['games'][0]
    timestamp = parser.parse(game['gameDate'])
    from_tz = tz.gettz('UTC')
    to_tz = tz.gettz('America/Chicago')
    timestamp.replace(tzinfo=from_tz)
    central_time = timestamp.astimezone(to_tz)

    away_team = game['teams']['away']['team']['name']
    home_team = game['teams']['home']['team']['name']
    if home_team == 'Nashville Predators':
        opponent = away_team
    else:
        opponent = home_team

    return f'{away_team} @ {home_team} today, game time is {central_time.strftime("%I:%M %p")}. Fuck the {opponent} <:victoryfish:804006668379226121>'


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')

client = discord.Client()


@client.event
async def on_ready():
    print("bot:user ready == {0.user}".format(client))
    try:
        channel = client.get_channel(int(CHANNEL))
        await channel.send(game_message())
        sys.exit()
    except Exception as e:
        print(e)


client.run(TOKEN)
