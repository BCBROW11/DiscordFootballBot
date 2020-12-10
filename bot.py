import discord
import requests
import json
import yaml
from discord.ext import commands
from prettytable import PrettyTable
import http.client
from bs4 import BeautifulSoup

# Credentials
TOKEN = '<BOTTOKEN>'

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
class game:
    def __init__(self, home, homeScore, away, awayScore, status, time):
        self.home = home
        self.homeScore = homeScore
        self.away = away
        self.awayScore = awayScore
        self.status = status
        self.time = time

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command()

async def standings(ctx):

    request = requests.get("https://www.pro-football-reference.com/")
    soup = BeautifulSoup(request.content, 'html.parser')
    result = soup.find(id="all_AFC")
    items = []
    for child in result.recursiveChildGenerator():
        items.append(child)


    await ctx.send(
        len(items)
    )
async def scores(ctx):

    request = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
    str = request.text
    str = str.replace(",,", ",\"\",")
    str = str.replace(",,", ",\"\",")
    y = json.loads(str)


    scores = []

    scoreEmbed = discord.Embed(color=0x00ff00)
    for i in y['ss']:
        if(i[2] == 'final overtime'):
            i[2] = 'Final'
        if(i[2] == 'Pregame'):
            miliTime = i[1]
            hours, minutes, seconds = miliTime.split(":")
            hours, minutes, seconds = int(hours), int(minutes), int(seconds)
            setting = "AM"
            if hours > 12:
                setting = "PM"
                hours -= 15
            else:
                hours -=3
        scores.append(game(i[4], i[5], i[6], i[7], i[2], i[3])) #might be i[1] for time left

    scoreEmbed.color = discord.Color.green()
    gameCount = len(scores)
    gmStr = "```\n"
    x = 0
    for i in range(gameCount):
        if gameCount - x >= 3:
            gmStr = gmStr + '{:5} {:10} {:5} {:10} {:5} {:10}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
            gmStr = gmStr + "\n{:5} {:10} {:5} {:10} {:5} {:10}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
            gmStr = gmStr + "\n{:5} {:10} {:5} {:10} {:5} {:10}".format(scores[x].status, scores[x].time, scores[x+1].status, scores[x+1].time, scores[x+2].status, scores[x+2].time)
            gmStr = gmStr + "\n\n"
            x += 3
        elif gameCount - x == 2:
            gmStr = gmStr + '{:5} {:10} {:5} {:10}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
            gmStr = gmStr + "\n{:5} {:10} {:5} {:10}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
            gmStr = gmStr + "\n{:5} {:10} {:5} {:10}".format(scores[x].status, scores[x].time, scores[x+1].status, scores[x+1].time)
            break
        elif gameCount - x == 1:
            gmStr = gmStr + '{:5} {:10}'.format(scores[x].away, scores[x].awayScore)
            gmStr = gmStr + "\n{:5} {:10}".format(scores[x].home, scores[x].homeScore)
            gmStr = gmStr + "\n{:5} {:10}".format(scores[x].status, scores[x].time)
            break
    gmStr = gmStr + "\n```"


    await ctx.send(
        gmStr
    )

client.run(TOKEN)
