import discord
import requests
import json
import yaml
from discord.ext import commands
from prettytable import PrettyTable
import http.client
import logging
import threading
import time
from bs4 import BeautifulSoup

# Credentials
TOKEN = 'TOKEN'

# Create bot
client = commands.Bot(command_prefix='?')

def get_scores():
    while(True):
        global scoreRequest
        scoreRequest = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
        time.sleep(15)

def get_html():
    while(True):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        request = requests.get("https://www.pro-football-reference.com/years/2020/", headers = headers)
        global soup
        soup = BeautifulSoup(request.content, 'html.parser')
        global js
        js = {}
        global afce
        global afcw
        global afcn
        global afcs
        global nfce
        global nfcw
        global nfcn
        global nfcs

        afce = "AFC East"
        afcw = "AFC West"
        afcn = "AFC North"
        afcs = "AFC South"
        nfce = "NFC East"
        nfcw = "NFC West"
        nfcn = "NFC North"
        nfcs = "NFC South"
        js[afce] = []
        js[afcw] = []
        js[afcn] = []
        js[afcs] = []
        js[nfce] = []
        js[nfcw] = []
        js[nfcn] = []
        js[nfcs] = []

        for s in soup.find_all('tr'):
            tn = s.find(attrs={'data-stat': 'team'})
            w = s.find(attrs={'data-stat': 'wins'})
            l = s.find(attrs={'data-stat': 'losses'})
            t = s.find(attrs={'data-stat': 'ties'})
            #AFC Teams
            if tn != None and (tn.text == "Buffalo Bills" or tn.text == "Miami Dolphins" or tn.text == "New England Patriots" or tn.text == "New York Jets"):
                js[afce].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "Pittsburgh Steelers" or tn.text == "Cleveland Browns" or tn.text == "Baltimore Ravens" or tn.text == "Cincinnati Bengals"):
                js[afcn].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "Indianapolis Colts" or tn.text == "Tennessee Titans" or tn.text == "Houston Texans" or tn.text == "Jacksonville Jaguars"):
                js[afcs].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "Kansas City Chiefs" or tn.text == "Las Vegas Raiders" or tn.text == "Denver Broncos" or tn.text == "Los Angeles Chargers"):
                js[afcw].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})

            #NFC Teams
            if tn != None and (tn.text == "Washington Football Team" or tn.text == "Dallas Cowboys" or tn.text == "New York Giants" or tn.text == "Philadelphia Eagles"):
                js[nfce].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "Green Bay Packers" or tn.text == "Minnesota Vikings" or tn.text == "Detroit Lions" or tn.text == "Chicago Bears"):
                js[nfcn].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "Tampa Bay Buccaneers" or tn.text == "New Orleans Saints" or tn.text == "Atlanta Falcons" or tn.text == "Carolina Panthers"):
                js[nfcs].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
            if tn != None and (tn.text == "San Francisco 49ers" or tn.text == "Arizona Cardinals" or tn.text == "Seattle Seahawks" or tn.text == "Los Angeles Rams"):
                js[nfcw].append({"team":tn.text, "wins":w.text, "losses":l.text, "ties":t.text})
        time.sleep(43200)

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
    req = threading.Thread(target=get_html)
    req2 = threading.Thread(target=get_scores)
    req.start()
    req2.start()

# Command

@client.command()
async def standings(ctx, *args):
    stStr = "```\n"

    if args:
        if args[0].lower() == "nfcw":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcw, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][0]["team"], js[nfcw][0]["wins"], js[nfcw][0]["losses"], js[nfcw][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][1]["team"], js[nfcw][1]["wins"], js[nfcw][1]["losses"], js[nfcw][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][2]["team"], js[nfcw][2]["wins"], js[nfcw][2]["losses"], js[nfcw][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][3]["team"], js[nfcw][3]["wins"], js[nfcw][3]["losses"], js[nfcw][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "nfce":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfce, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][0]["team"], js[nfce][0]["wins"], js[nfce][0]["losses"], js[nfce][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][1]["team"], js[nfce][1]["wins"], js[nfce][1]["losses"], js[nfce][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][2]["team"], js[nfce][2]["wins"], js[nfce][2]["losses"], js[nfce][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][3]["team"], js[nfce][3]["wins"], js[nfce][3]["losses"], js[nfce][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "nfcs":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcs, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][0]["team"], js[nfcs][0]["wins"], js[nfcs][0]["losses"], js[nfcs][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][1]["team"], js[nfcs][1]["wins"], js[nfcs][1]["losses"], js[nfcs][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][2]["team"], js[nfcs][2]["wins"], js[nfcs][2]["losses"], js[nfcs][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][3]["team"], js[nfcs][3]["wins"], js[nfcs][3]["losses"], js[nfcs][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "nfcn":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcn, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][0]["team"], js[nfcn][0]["wins"], js[nfcn][0]["losses"], js[nfcn][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][1]["team"], js[nfcn][1]["wins"], js[nfcn][1]["losses"], js[nfcn][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][2]["team"], js[nfcn][2]["wins"], js[nfcn][2]["losses"], js[nfcn][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][3]["team"], js[nfcn][3]["wins"], js[nfcn][3]["losses"], js[nfcn][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "afcw":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcw, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][0]["team"], js[afcw][0]["wins"], js[afcw][0]["losses"], js[afcw][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][1]["team"], js[afcw][1]["wins"], js[afcw][1]["losses"], js[afcw][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][2]["team"], js[afcw][2]["wins"], js[afcw][2]["losses"], js[afcw][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][3]["team"], js[afcw][3]["wins"], js[afcw][3]["losses"], js[afcw][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "afce":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afce, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][0]["team"], js[afce][0]["wins"], js[afce][0]["losses"], js[afce][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][1]["team"], js[afce][1]["wins"], js[afce][1]["losses"], js[afce][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][2]["team"], js[afce][2]["wins"], js[afce][2]["losses"], js[afce][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][3]["team"], js[afce][3]["wins"], js[afce][3]["losses"], js[afce][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "afcs":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcs, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][0]["team"], js[afcs][0]["wins"], js[afcs][0]["losses"], js[afcs][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][1]["team"], js[afcs][1]["wins"], js[afcs][1]["losses"], js[afcs][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][2]["team"], js[afcs][2]["wins"], js[afcs][2]["losses"], js[afcs][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][3]["team"], js[afcs][3]["wins"], js[afcs][3]["losses"], js[afcs][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
        elif args[0].lower() == "afcn":
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcn, "W", "L", "T")
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][0]["team"], js[afcn][0]["wins"], js[afcn][0]["losses"], js[afcn][0]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][1]["team"], js[afcn][1]["wins"], js[afcn][1]["losses"], js[afcn][1]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][2]["team"], js[afcn][2]["wins"], js[afcn][2]["losses"], js[afcn][2]["ties"])
            stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][3]["team"], js[afcn][3]["wins"], js[afcn][3]["losses"], js[afcn][3]["ties"])
            stStr = stStr + "\n```"
            await ctx.send(
                stStr
            )
            return
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcn, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][0]["team"], js[afcn][0]["wins"], js[afcn][0]["losses"], js[afcn][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][1]["team"], js[afcn][1]["wins"], js[afcn][1]["losses"], js[afcn][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcn][2]["team"], js[afcn][2]["wins"], js[afcn][2]["losses"], js[afcn][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[afcn][3]["team"], js[afcn][3]["wins"], js[afcn][3]["losses"], js[afcn][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afce, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][0]["team"], js[afce][0]["wins"], js[afce][0]["losses"], js[afce][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][1]["team"], js[afce][1]["wins"], js[afce][1]["losses"], js[afce][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afce][2]["team"], js[afce][2]["wins"], js[afce][2]["losses"], js[afce][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[afce][3]["team"], js[afce][3]["wins"], js[afce][3]["losses"], js[afce][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcs, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][0]["team"], js[afcs][0]["wins"], js[afcs][0]["losses"], js[afcs][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][1]["team"], js[afcs][1]["wins"], js[afcs][1]["losses"], js[afcs][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcs][2]["team"], js[afcs][2]["wins"], js[afcs][2]["losses"], js[afcs][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[afcs][3]["team"], js[afcs][3]["wins"], js[afcs][3]["losses"], js[afcs][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(afcw, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][0]["team"], js[afcw][0]["wins"], js[afcw][0]["losses"], js[afcw][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][1]["team"], js[afcw][1]["wins"], js[afcw][1]["losses"], js[afcw][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[afcw][2]["team"], js[afcw][2]["wins"], js[afcw][2]["losses"], js[afcw][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[afcw][3]["team"], js[afcw][3]["wins"], js[afcw][3]["losses"], js[afcw][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcn, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][0]["team"], js[nfcn][0]["wins"], js[nfcn][0]["losses"], js[nfcn][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][1]["team"], js[nfcn][1]["wins"], js[nfcn][1]["losses"], js[nfcn][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcn][2]["team"], js[nfcn][2]["wins"], js[nfcn][2]["losses"], js[nfcn][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[nfcn][3]["team"], js[nfcn][3]["wins"], js[nfcn][3]["losses"], js[nfcn][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfce, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][0]["team"], js[nfce][0]["wins"], js[nfce][0]["losses"], js[nfce][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][1]["team"], js[nfce][1]["wins"], js[nfce][1]["losses"], js[nfce][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfce][2]["team"], js[nfce][2]["wins"], js[nfce][2]["losses"], js[nfce][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[nfce][3]["team"], js[nfce][3]["wins"], js[nfce][3]["losses"], js[nfce][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcs, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][0]["team"], js[nfcs][0]["wins"], js[nfcs][0]["losses"], js[nfcs][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][1]["team"], js[nfcs][1]["wins"], js[nfcs][1]["losses"], js[nfcs][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcs][2]["team"], js[nfcs][2]["wins"], js[nfcs][2]["losses"], js[nfcs][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n\n'.format(js[nfcs][3]["team"], js[nfcs][3]["wins"], js[nfcs][3]["losses"], js[nfcs][3]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(nfcw, "W", "L", "T")
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][0]["team"], js[nfcw][0]["wins"], js[nfcw][0]["losses"], js[nfcw][0]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][1]["team"], js[nfcw][1]["wins"], js[nfcw][1]["losses"], js[nfcw][1]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][2]["team"], js[nfcw][2]["wins"], js[nfcw][2]["losses"], js[nfcw][2]["ties"])
    stStr = stStr + '{:25}{:4}{:4}{:4}\n'.format(js[nfcw][3]["team"], js[nfcw][3]["wins"], js[nfcw][3]["losses"], js[nfcw][3]["ties"])
    stStr = stStr + "\n```"
    await ctx.send(
        stStr
    )


@client.command()
async def scores(ctx, *args):
    str = scoreRequest.text
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
            if scores[x].home.lower() == args[0].lower() or scores[x].away.lower() == args[0].lower():
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
                    gmStr = gmStr + "\n{:8}{:5}{:8}{:5}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
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

@client.command()
async def NFLBotHelp(ctx):
    str = "```\n Commands: ?standings | ?standings <conference:division> (afce, nfce, etc) | ?scores | ?scores <team> (SEA, JAX, LAC, etc) | ?fbref <firstName> <lastName>\n```"
    await ctx.send(
        str
    )

@client.command()
async def fbref(ctx, *args):
    if len(args) == 0:
        await ctx.send(
            "```\n" + "Enter a player" + "\n```"
        )
        return
    i = 0
    urlStr = "https://www.pro-football-reference.com/search/search.fcgi?search="

    if args[0].lower() == "asian" and args[1].lower() == "jesus":
        urlStr = "https://www.pro-football-reference.com/players/D/DaltAn00.htm"
        await ctx.send(
            urlStr
        )
        return

    while i < len(args):
        if(i == 0):
            urlStr = urlStr + args[0]
        else:
            urlStr = urlStr + "+" + args[i]
        i += 1
    await ctx.send(
        urlStr
    )

client.run(TOKEN)
