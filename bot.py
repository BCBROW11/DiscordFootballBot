import discord
import requests
import json
import yaml
from discord.ext import commands
from prettytable import PrettyTable
import http.client
from bs4 import BeautifulSoup

# Credentials
TOKEN = '<TOKEN>'

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
class game:
    def __init__(self, day, home, homeScore, away, awayScore, status, timeInQuarter, gameTime):
        self.day = day
        self.home = home
        self.homeScore = homeScore
        self.away = away
        self.awayScore = awayScore
        self.status = status
        self.timeInQuarter = timeInQuarter
        self.gameTime = gameTime

@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command()

async def standings(ctx):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    request = requests.get("https://www.pro-football-reference.com/", headers = headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    result = soup.find(id="all_AFC")
    items = []
    for child in result.recursiveChildGenerator():
        items.append(child)


    await ctx.send(
        len(items)
    )

@client.command()
async def scores(ctx, *args):

    request = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
    str = request.text
    str = str.replace(",,", ",\"\",")
    str = str.replace(",,", ",\"\",")
    y = json.loads(str)


    scores = []

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
                hours -= 12
            else:
                hours -= 3
            i[1] = "{:02d}:{:02d}{}".format(hours, minutes, setting)
        scores.append(game(i[0], i[6], i[7], i[4], i[5], i[2],i[3], i[1])) #might be i[1] for time left

    gmStr = "```\n"
    gameCount = len(scores)
    x = 0
    if args:
        for i in range(gameCount):
            if scores[x].home == args[0] or scores[x].away == args[0]:
                if scores[x].status == "Pregame":
                    gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}".format(scores[x].day, scores[x].gameTime)
                    gmStr = gmStr + "\n\n"
                    gmStr = gmStr + "\n```"
                    await ctx.send(
                        gmStr
                    )
                    return
                elif scores[x].status == "Halftime" or scores[x].status == "Final":
                    gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    gmStr = gmStr + "\n```"
                    await ctx.send(
                        gmStr
                    )
                    return
                else:
                    gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    gmStr = gmStr + "\n```"
                    await ctx.send(
                        gmStr
                    )
                    return
            x += 1

    x = 0
    for i in range(gameCount):
        if gameCount - x >= 3:
            #PPP
            if scores[x].status == "Pregame" and scores[x+1].status == "Pregame" and scores[x+2].status == "Pregame":
                gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                gmStr = gmStr + "\n{:3} {:9}{:3} {:9}{:3} {:9}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                gmStr = gmStr + "\n\n"
                x += 3
            #IPP
            elif scores[x].status != "Pregame" and scores[x+1].status == "Pregame" and scores[x+2].status == "Pregame":
                if scores[x].status == "Halftime" or scores[x].status == "Final": #first game at halftime
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:3} {:9}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                else:
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:3} {:9}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #IIP
            elif scores[x].status != "Pregame" and scores[x+1].status != "Pregame" and scores[x+2].status == "Pregame":
                #first two games are at halftime g3 pregame
                if (scores[x].status == "Halftime" or scores[x].status == "Final") and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:8}{:5}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 not halftime, g2 halftime, g3 pregame
                elif scores[x].status != "Halftime" and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:8}{:5}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime, g2 not halftime g3 pregame
                elif (scores[x].status == "Halftime" or scores[x].status == "Final") and scores[x+1].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}Q{:4}{:8}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #none halftime
                else:
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}Q{:4}{:8}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #PPI
            elif scores[x].status == "Pregame" and scores[x+1].status == "Pregame" and scores[x+2].status != "Pregame":
                #g3 Halftime
                if scores[x+2].status == "Halftime" or scores[x+2].status == "Final":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}{:3} {:9}{:8}{:5}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g3 not halftime
                elif scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}{:3} {:9}Q{:4}{:8}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #PII
            elif scores[x].status == "Pregame" and scores[x+1].status != "Pregame" and scores[x+2].status != "Pregame":
                #g2 halftime, g3 not halftimee
                if (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}{:8}{:5}Q{:4}{:8}".format(scores[x].day, scores[x].gameTime, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g2 not halftime, g3 halftime
                elif scores[x+1].status != "Halftime" and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}Q{:4}{:8}{:8}{:5}".format(scores[x].day, scores[x].gameTime, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g2 halftime, g3 halftime
                elif (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}{:8}{:5}{:8}{:5}".format(scores[x].day, scores[x].gameTime, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #PIP
            elif scores[x].status == "Pregame" and scores[x+1].status != "Pregame" and scores[x+2].status == "Pregame":
                #g2 halftimee
                if scores[x+1].status == "Halftime" or scores[x+1].status == "Final":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}{:8}{:5}{:3} {:9}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g2 not halftime
                elif scores[x+1].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:3} {:9}Q{:4}{:8}{:3} {:9}".format(scores[x].day, scores[x].gameTime, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #IPI
            elif scores[x].status != "Pregame" and scores[x+1].status == "Pregame" and scores[x+2].status != "Pregame":
                #g1 halftime, g3 not halftime
                if (scores[x].status == "Halftime" or scores[x].status == "Final") and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:3} {:9}Q{:4}{:8}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime, scores[x+2].day, scores[x+2].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 not halftime, g3 halftime
                elif scores[x].status != "Halftime" and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:3} {:9}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime, g3 halftime
                elif (scores[x].status == "Halftime" or scores[x].status == "Final") and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:3} {:9}{:8}{:5}".format(scores[x].day, scores[x].gameTime, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
            #III
            else:
                #all halftime
                if (scores[x].status == "Halftime" or scores[x].status == "Final") and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"): #all games on line are at halftime
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:8}{:5}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime, g2 not halftime, g3 not halftime
                elif scores[x].status == "Halftime" and scores[x+1].status != "Halftime" and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}Q{:4}{:8}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime, g2 halftime, g3 not halftime
                elif (scores[x].status == "Halftime" or scores[x].status == "Final") and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:8}{:5}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime, g2 not halftime, g3 halftime
                elif (scores[x].status == "Halftime" or scores[x].status == "Final") and scores[x+1].status != "Halftime" and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}Q{:4}{:8}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 not halftime, g2 halftime, g3 halftime
                elif scores[x].status != "Halftime" and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:8}{:5}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 not halftime, g2 not halftime, g3 halftime
                elif scores[x].status != "Halftime" and scores[x+1].status != "Halftime" and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"):
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}Q{:4}{:8}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 not halftime, g2 halftime, g3 not halftime
                elif scores[x].status != "Halftime" and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:8}{:5}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #none halftime
                else:
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}Q{:4}{:8}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3

        #only two games in a row
        elif gameCount - x == 2:
            if scores[x].status == "Pregame" and scores[x+1].status == "Pregame":
                gmStr = gmStr + '{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
                gmStr = gmStr + "\n{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
                gmStr = gmStr + "\n{:3} {:9}{:3} {:9}".format(scores[x].day, scores[x].gameTime, scores[x+1].day, scores[x+1].gameTime)
                gmStr = gmStr + "\n\n"
                x += 2
            elif scores[x].status != "Pregame" and scores[x+1].status == "Pregame":
                if (scores[x].status == "Halftime" or scores[x].status == "Final") :
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 2
                else:
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
                    gmStr = gmStr + "\nQ{:4}{:8}{:3} {:9}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime)
                    gmStr = gmStr + "\n\n"
                    x += 2
            else:
                if scores[x].status == "Pregame" and scores[x+1].status != "Pregame":
                    if (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") :
                        gmStr = gmStr + '{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
                        gmStr = gmStr + "\n{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
                        gmStr = gmStr + "\n{:3} {:9}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime)
                        gmStr = gmStr + "\n\n"
                        x += 2
                    else:
                        gmStr = gmStr + '{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore)
                        gmStr = gmStr + "\n{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore)
                        gmStr = gmStr + "\n{:3} {:9}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].day, scores[x+1].gameTime)
                        gmStr = gmStr + "\n\n"
                        x += 2
        elif gameCount - x == 1:
            if scores[x].status == "Pregame":
                gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                gmStr = gmStr + "\n{:3} {:9}".format(scores[x].day, scores[x].gameTime)
                gmStr = gmStr + "\n\n"
                x += 1
            elif scores[x].status == "Halftime" or scores[x].status == "Final":
                gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                gmStr = gmStr + "\n{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter)
                gmStr = gmStr + "\n\n"
                x += 1
            else:
                gmStr = gmStr + '{:5}{:8}'.format(scores[x].away, scores[x].awayScore)
                gmStr = gmStr + "\n{:5}{:8}".format(scores[x].home, scores[x].homeScore)
                gmStr = gmStr + "\nQ{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter)
                gmStr = gmStr + "\n\n"
                x += 2
    gmStr = gmStr + "\n```"


    await ctx.send(
        gmStr
    )

client.run(TOKEN)
