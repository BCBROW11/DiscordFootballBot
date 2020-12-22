import discord
import json
import yaml
from discord.ext import commands
import http.client
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import traceback
import threading
import os

from Threads.get_def_stats import get_def_stats
from Threads.get_qb_stats import get_qb_stats
from Threads.get_rb_stats import get_rb_stats
from Threads.get_wr_stats import get_wr_stats
from Threads.get_team_def_stats import get_team_def_stats
from Threads.get_standings import get_standings
from Threads.get_scores import get_scores

from Helpers.convert_game_time import convert_game_time
from Helpers.game import game
from Helpers.quarterback import quarterback
from Helpers.runningback import runningback
from Helpers.receiver import receiver
from Helpers.defend import defend
from Helpers.team_defense import team_defense

# Create bot
client = commands.Bot(command_prefix='$')

"""
on_ready starts bot and initiates threads
"""
@client.event
async def on_ready():
    global reaction
    reaction = "❓"
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    global t1
    global t2
    global t3
    global t4
    global t5
    global t6
    global t7
    global t8
    t1 = get_standings()
    t2 = get_scores()
    t3 = get_qb_stats()
    t4 = get_rb_stats()
    t5 = get_wr_stats()
    t6 = get_def_stats()
    t7 = get_team_def_stats()
    try:
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
    except Exception:
        print("Threading error: \n" + Exception)

"""
standings allows for user to search for current standings. builds string to return depending on game states.
:args: ?standings <conference> <division>
"""
@client.command()
async def standings(ctx, *args):
    js = {}
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
    standingsSoup = t1.standingsSoup
    for s in standingsSoup.find_all('tr'):

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


    stStr = "```\n"

    if args:
        div = args[0].lower() + " " + args[1].lower()
        if div == "nfc west" or div == "nfc w":
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
        if div == "nfc east" or div == "nfc e":
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
        if div == "nfc south" or div == "nfc s":
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
        if div == "nfc north" or div == "nfc n":
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
        if div == "afc west" or div == "afc w":
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
        if div == "afc east" or div == "afc e":
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
        if div == "afc south" or div == "afc s":
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
        if div == "afc north" or div == "afc n":
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

"""
fbref builds link to pro-football-reference player page
:args: valid statement is ?fbref firstName LastName

"""
@client.command()
async def scores(ctx, *args):

    str = t2.scoreRequest.text
    str = str.replace(",,", ",\"\",")
    str = str.replace(",,", ",\"\",")
    y = json.loads(str)

    scores = []

    for i in y['ss']:
        if(i[2] == 'final overtime'):
            i[2] = 'Final'
        if(i[2] == 'Pregame'):
            miliTime = i[1]
            i[1] = convert_game_time(i[1])
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
                #all halftime or final
                if (scores[x].status == "Halftime" or scores[x].status == "Final") and (scores[x+1].status == "Halftime" or scores[x+1].status == "Final") and (scores[x+2].status == "Halftime" or scores[x+2].status == "Final"): #all games on line are at halftime
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}{:8}{:5}{:8}{:5}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime or final, g2 not halftime, g3 not halftime
                elif (scores[x].status == "Halftime" or scores[x].status == "Final") and scores[x+1].status != "Halftime" and scores[x+2].status != "Halftime":
                    gmStr = gmStr + '{:5}{:8}{:5}{:8}{:5}{:8}'.format(scores[x].away, scores[x].awayScore, scores[x+1].away, scores[x+1].awayScore, scores[x+2].away, scores[x+2].awayScore)
                    gmStr = gmStr + "\n{:5}{:8}{:5}{:8}{:5}{:8}".format(scores[x].home, scores[x].homeScore, scores[x+1].home, scores[x+1].homeScore, scores[x+2].home, scores[x+2].homeScore)
                    gmStr = gmStr + "\n{:8}{:5}Q{:4}{:8}Q{:4}{:8}".format(scores[x].status, scores[x].timeInQuarter, scores[x+1].status, scores[x+1].timeInQuarter, scores[x+2].status, scores[x+2].timeInQuarter)
                    gmStr = gmStr + "\n\n"
                    x += 3
                #g1 halftime or final, g2 halftime or final, g3 not halftime
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
"""
fbref builds link to pro-football-reference player page
:args: valid statement is ?fbref firstName LastName

"""
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
######################################################################################QUARTERBACK STATS
"""
qb allows for commands to get quarterback stats.
:args: valid statements are ?qb touchdowns | tds,?qb interceptions | ints,?qb yards | yds,?qb ratings | rtgs,?qb completion,?qb sacks,?qb compare firstName lastName firstName lastName, and ?qb firstName lastName

"""
@client.command()
async def qb(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    quarterbacks = []
    i = 1
    qb_rows = t3.qb_rows

    for row in qb_rows:
        stats = row.find_all(attrs={"data-stat":True})
        quarterbacks.append(quarterback(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+7].text, stats[i+8].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+13].text, stats[i+21].text, stats[i+23].text))
    if len(args) == 1:
        i = 0
        if args[0].lower() == "touchdowns" or args[0].lower() == "tds":
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: int(x.tds), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "TD")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].tds)
                i += 1
        elif args[0].lower() == "interceptions" or args[0].lower() == "ints":
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: int(x.ints), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "INT")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].ints)
                i += 1
        elif args[0].lower() == "yards" or args[0].lower() == "yds":
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "YDS")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].yards)
                i += 1
        elif args[0].lower() == "ratings" or args[0].lower() == "rtgs":
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: float(x.rtg), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "RTG")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].rtg)
                i += 1
        elif args[0].lower() == "completion":
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: float(x.cmpPctg), reverse=True)
            while i < 10:
                str = str + '{:20}{:4}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].cmpPctg)
                i += 1
        elif args[0].lower() == "sacks":
            str = str + '{:20}{:5}\n'.format("NAME", "SACKS")
            quarterbacks_sorted = sorted(quarterbacks, key = lambda x: float(x.sacks), reverse=True)
            while i < 10:
                str = str + '{:20}{:4}\n'.format(quarterbacks_sorted[i].name, quarterbacks_sorted[i].sacks)
                i += 1
        else:
            await ctx.message.add_reaction(emoji=reaction)
            return
    if len(args) == 2:
        qb_count = 0
        qb_name = args[0].lower() + " " + args[1].lower()
        while qb_count < len(quarterbacks):
            qb_name2 = quarterbacks[qb_count].name.split(" ")
            if qb_name == (qb_name2[0].lower() + " " + qb_name2[1].lower()):
                str = str + '{:20}{:4}{:4}{:5}{:3}{:4}{:6}{:3}\n'.format("NAME", "CMP", "ATT", "YDS", "TD", "INT", "RTG", "SCK")
                str = str + '{:20}{:4}{:4}{:5}{:3}{:4}{:6}{:3}\n'.format(quarterbacks[qb_count].name, quarterbacks[qb_count].cmp, quarterbacks[qb_count].att, quarterbacks[qb_count].yards, quarterbacks[qb_count].tds, quarterbacks[qb_count].ints, quarterbacks[qb_count].rtg, quarterbacks[qb_count].sacks)
                break
            qb_count += 1
    if len(args) > 2:
        str = str + '{:20}{:4}{:4}{:5}{:3}{:4}{:6}{:3}\n'.format("NAME", "CMP", "ATT", "YDS", "TD", "INT", "RTG", "SCK")
        if args[0].lower() == "compare":
            qb_comps = []
            qb_count = 0
            i = 1
            j = 2
            argLen = len(args)
            #add qbs to compare
            while i < argLen - 1:
                qb_comps.append(args[i] + " " + args[j])
                i += 2
                j += 2
            #0 less than 50
            while qb_count < len(quarterbacks):
                k = 0
                qb_name2 = quarterbacks[qb_count].name.split(" ") #qb name from qb list
                while k < len(qb_comps):
                    if qb_comps[k].lower() == (qb_name2[0].lower() + " " + qb_name2[1].lower()):
                        str = str + '{:20}{:4}{:4}{:5}{:3}{:4}{:6}{:3}\n'.format(quarterbacks[qb_count].name, quarterbacks[qb_count].cmp, quarterbacks[qb_count].att, quarterbacks[qb_count].yards, quarterbacks[qb_count].tds, quarterbacks[qb_count].ints, quarterbacks[qb_count].rtg, quarterbacks[qb_count].sacks)
                    k+=1
                qb_count += 1
    str = str + "\n```"
    if str == "```\n\n```":
        await ctx.message.add_reaction(emoji=reaction)
        return

    await ctx.send(
        str
    )
"""
rb allows for commands to get runningback stats.
:args: valid statements are ?rb touchdowns | tds, ?rb yards | yds, ?rb long | lng,?rb y/a,?rb compare firstName lastName firstName lastName, and ?rb firstName lastName

"""
@client.command()
async def rb(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    runningbacks = []
    i = 1
    rb_rows = t4.rb_rows
    for row in rb_rows:
        stats = row.find_all(attrs={"data-stat":True})
        runningbacks.append(runningback(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+7].text, stats[i+8].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text))
    if len(args) == 1:
        i = 0
        if args[0].lower() == "touchdowns" or args[0].lower() == "tds":
            runningbacks_sorted = sorted(runningbacks, key = lambda x: int(x.tds), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "TD")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].tds)
                i += 1
        elif args[0].lower() == "yards" or args[0].lower() == "yds":
            runningbacks_sorted = sorted(runningbacks, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "YDS")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].yards)
                i += 1
        elif args[0].lower() == "long" or args[0].lower() == "lng":
            runningbacks_sorted = sorted(runningbacks, key = lambda x: int(x.long), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "LNG")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].long)
                i += 1
        elif args[0].lower() == "y/a":
            str = str + '{:20}{:5}\n'.format("NAME", "Y/A")
            runningbacks_sorted = sorted(runningbacks, key = lambda x: float(x.ya), reverse=True)
            count = 0
            while i < len(runningbacks_sorted):
                if count == 10:
                    break
                if(runningbacks_sorted[i].pos.lower() == "rb"):
                    str = str + '{:20}{:4}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].ya)
                    count += 1
                i += 1
        elif args[0].lower() == "y/g":
            str = str + '{:20}{:5}\n'.format("NAME", "Y/G")
            runningbacks_sorted = sorted(runningbacks, key = lambda x: float(x.yg), reverse=True)
            while i < 10:
                str = str + '{:20}{:4}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].yg)
                i += 1
        elif args[0].lower() == "fumbles" or args[0].lower() == "fmb":
            str = str + '{:20}{:5}\n'.format("NAME", "FMB")
            runningbacks_sorted = sorted(runningbacks, key = lambda x: float(x.fmb), reverse=True)
            count = 0
            while i < len(runningbacks_sorted):
                if count == 10:
                    break
                if(runningbacks_sorted[i].pos.lower() == "rb"):
                    str = str + '{:20}{:4}\n'.format(runningbacks_sorted[i].name, runningbacks_sorted[i].fmb)
                    count += 1
                i += 1
        else:
            await ctx.message.add_reaction(emoji=reaction)
            return
    if len(args) == 2:
        rb_count = 0
        rb_name = args[0].lower() + " " + args[1].lower()
        while rb_count < len(runningbacks):
            rb_name2 = runningbacks[rb_count].name.split(" ")
            if rb_name == (rb_name2[0].lower() + " " + rb_name2[1].lower()):
                str = str + '{:20}{:4}{:5}{:3}{:4}{:4}{:6}{:3}\n'.format("NAME", "ATT", "YDS", "TD", "LNG", "Y/A", "Y/G", "FUM")
                str = str + '{:20}{:4}{:5}{:3}{:4}{:4}{:6}{:3}\n'.format(runningbacks[rb_count].name, runningbacks[rb_count].att, runningbacks[rb_count].yards, runningbacks[rb_count].tds, runningbacks[rb_count].long, runningbacks[rb_count].ya, runningbacks[rb_count].yg, runningbacks[rb_count].fmb)
                break
            rb_count += 1
    if len(args) > 2:
        str = str + '{:20}{:4}{:5}{:3}{:4}{:4}{:6}{:3}\n'.format("NAME", "ATT", "YDS", "TD", "LNG", "Y/A", "Y/G", "FUM")
        if args[0].lower() == "compare":
            rb_comps = []
            rb_count = 0
            i = 1
            j = 2
            argLen = len(args)
            #add qbs to compare
            while i < argLen - 1:
                rb_comps.append(args[i] + " " + args[j])
                i += 2
                j += 2
            #0 less than 50
            if len(rb_comps) == 0:
                await ctx.message.add_reaction(emoji=reaction)
                return
            while rb_count < len(runningbacks):
                k = 0
                rb_name2 = runningbacks[rb_count].name.split(" ")
                while k < len(rb_comps):
                    if rb_comps[k].lower() == (rb_name2[0].lower() + " " + rb_name2[1].lower()):
                        str = str + '{:20}{:4}{:5}{:3}{:4}{:4}{:6}{:3}\n'.format(runningbacks[rb_count].name, runningbacks[rb_count].att, runningbacks[rb_count].yards, runningbacks[rb_count].tds, runningbacks[rb_count].long, runningbacks[rb_count].ya, runningbacks[rb_count].yg, runningbacks[rb_count].fmb)
                    k+=1
                rb_count += 1
        else:
            str = "```\n"
    str = str + "\n```"
    if str == "```\n\n```":
        await ctx.message.add_reaction(emoji=reaction)
        return

    await ctx.send(
        str
    )
"""
wr allows for commands to get wide receiver and tight end stats.
:args: valid statements are ?wr touchdowns | tds, ?wr yards | yds, ?wr receptions | recs,?wr long | lng,?wr y/g,?wr fumbles | fmb, ?wr compare firstName lastName firstName lastName, and ?rb firstName lastName

"""
@client.command()
async def wr(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    receivers = []
    i = 1
    wr_rows = t5.wr_rows
    for row in wr_rows:
        stats = row.find_all(attrs={"data-stat":True})
        receivers.append(receiver(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+7].text, stats[i+8].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text, stats[i+14].text, stats[i+16].text, stats[i+17].text))
    if len(args) == 1:
        i = 0
        if args[0].lower() == "touchdowns" or args[0].lower() == "tds":
            receivers_sorted = sorted(receivers, key = lambda x: int(x.tds), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "TD")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(receivers_sorted[i].name, receivers_sorted[i].tds)
                i += 1
        elif args[0].lower() == "yards" or args[0].lower() == "yds":
            receivers_sorted = sorted(receivers, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "YDS")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(receivers_sorted[i].name, receivers_sorted[i].yards)
                i += 1
        elif args[0].lower() == "receptions" or args[0].lower() == "recs":
            receivers_sorted = sorted(receivers, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "REC")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(receivers_sorted[i].name, receivers_sorted[i].rec)
                i += 1
        elif args[0].lower() == "long" or args[0].lower() == "lng":
            receivers_sorted = sorted(receivers, key = lambda x: int(x.long), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "LNG")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(receivers_sorted[i].name, receivers_sorted[i].long)
                i += 1
        elif args[0].lower() == "y/g":
            str = str + '{:20}{:5}\n'.format("NAME", "Y/G")
            receivers_sorted = sorted(receivers, key = lambda x: float(x.yg), reverse=True)
            while i < 10:
                str = str + '{:20}{:4}\n'.format(receivers_sorted[i].name, receivers_sorted[i].yg)
                i += 1
        elif args[0].lower() == "fumbles" or args[0].lower() == "fmb":
            str = str + '{:20}{:5}\n'.format("NAME", "FMB")
            receivers_sorted = sorted(receivers, key = lambda x: float(x.fmb), reverse=True)
            count = 0
            while i < len(receivers_sorted):
                if count == 10:
                    break
                if(receivers_sorted[i].pos.lower() == "wr"):
                    str = str + '{:20}{:4}\n'.format(receivers_sorted[i].name, receivers_sorted[i].fmb)
                    count += 1
                i += 1
        else:
            await ctx.message.add_reaction(emoji=reaction)
            return
    if len(args) == 2:
        wr_count = 0
        wr_name = args[0].lower() + " " + args[1].lower()
        while wr_count < len(receivers):
            wr_name2 = receivers[wr_count].name.split(" ")
            if wr_name == (wr_name2[0].lower() + " " + wr_name2[1].lower()):
                str = str + '{:20}{:4}{:4}{:5}{:3}{:6}{:3}\n'.format("NAME", "TGT", "REC", "YDS", "TD", "Y/G", "FUM")
                str = str + '{:20}{:4}{:4}{:5}{:3}{:6}{:3}\n'.format(receivers[wr_count].name, receivers[wr_count].tgt, receivers[wr_count].rec, receivers[wr_count].yards, receivers[wr_count].tds, receivers[wr_count].yg, receivers[wr_count].fmb)
                break
            wr_count += 1
    if len(args) > 2:
        str = str + '{:20}{:4}{:4}{:5}{:3}{:6}{:3}\n'.format("NAME", "TGT", "REC", "YDS", "TD", "Y/G", "FUM")
        if args[0].lower() == "compare":
            wr_comps = []
            wr_count = 0
            i = 1
            j = 2
            argLen = len(args)
            #add qbs to compare
            while i < argLen - 1:
                wr_comps.append(args[i] + " " + args[j])
                i += 2
                j += 2
            #0 less than 50
            if len(wr_comps) == 0:
                await ctx.message.add_reaction(emoji=reaction)
                return
            while wr_count < len(receivers):
                k = 0
                wr_name2 = receivers[wr_count].name.split(" ")
                while k < len(wr_comps):
                    if wr_comps[k].lower() == (wr_name2[0].lower() + " " + wr_name2[1].lower()):
                        str = str + '{:20}{:4}{:4}{:5}{:3}{:6}{:3}\n'.format(receivers[wr_count].name, receivers[wr_count].tgt, receivers[wr_count].rec, receivers[wr_count].yards, receivers[wr_count].tds, receivers[wr_count].yg, receivers[wr_count].fmb)
                    k+=1
                wr_count += 1
        else:
            str = "```\n"
    str = str + "\n```"
    if str == "```\n\n```":
        await ctx.message.add_reaction(emoji=reaction)
        return

    await ctx.send(
        str
    )
"""
defense allows for commands to get individual defensive players stats.
:args: valid statements are ?defense interceptions | ints, ?defense sacks, ?defense passes defended, ?defense forced fumbles, ?defense fumbles recovered, ?defense combined tackles, ?defense solo tackles, ?defense assisted tackles, ?defense compare firstName lastName firstName lastName, and ?defense firstName lastName

"""
@client.command()
async def defense(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    defends = []
    i = 1
    df_rows = t6.df_rows
    for row in df_rows:
        stats = row.find_all(attrs={"data-stat":True})
        if stats[i+6].text == "":
            stats[i+6].insert(0, "0")
        if stats[i+10].text == "":
            stats[i+10].insert(0, "0")
        if stats[i+11].text == "":
            stats[i+11].insert(0, "0")
        if stats[i+13].text == "":
            stats[i+13].insert(0, "0")
        if stats[i+16].text == "":
            stats[i+16].insert(0, "0")
        if stats[i+17].text == "":
            stats[i+17].insert(0, "0")
        if stats[i+18].text == "":
            stats[i+18].insert(0, "0")
        if stats[i+19].text == "":
            stats[i+19].insert(0, "0")
        if stats[i+20].text == "":
            stats[i+20].insert(0, "0")
        if stats[i+21].text == "":
            stats[i+21].insert(0, "0")
        defends.append(defend(stats[i].text, stats[i+1].text, stats[i+2].text, stats[i+3].text, stats[i+6].text, stats[i+10].text, stats[i+11].text, stats[i+13].text, stats[i+16].text, stats[i+17].text, stats[i+18].text, stats[i+19].text, stats[i+20].text, stats[i+21].text))
    if argLen == 1:
        i = 0
        if args[0].lower() == "interceptions" or args[0].lower() == "ints":
            defenders_sorted = sorted(defends, key = lambda x: int(x.ints), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "INTS")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(defenders_sorted[i].name, defenders_sorted[i].ints)
                i += 1
        elif args[0].lower() == "sacks":
            defenders_sorted = sorted(defends, key = lambda x: float(x.sacks), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "SACKS")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenders_sorted[i].name, defenders_sorted[i].sacks)
                i += 1

        else:
            await ctx.message.add_reaction(emoji=reaction)
            return
    if len(args) == 2:
        i = 0
        if args[0].lower() == "passes" and args[1].lower() == "defended":
            defenders_sorted = sorted(defends, key = lambda x: int(x.pd), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "PD")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(defenders_sorted[i].name, defenders_sorted[i].pd)
                i += 1
        elif args[0].lower() == "forced" and args[1].lower() == "fumbles":
            defenders_sorted = sorted(defends, key = lambda x: int(x.ff), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "FF")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(defenders_sorted[i].name, defenders_sorted[i].ff)
                i += 1
        elif args[0].lower() == "fumbles" and args[1].lower() == "recovered":
            defenders_sorted = sorted(defends, key = lambda x: int(x.fr), reverse=True)
            str = str + '{:20}{:3}\n'.format("NAME", "FR")
            while i < 10:
                str = str + '{:20}{:3}\n'.format(defenders_sorted[i].name, defenders_sorted[i].fr)
                i += 1
        elif args[0].lower() == "combined" and args[1].lower() == "tackles":
            defenders_sorted = sorted(defends, key = lambda x: int(x.comb), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "COMB")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenders_sorted[i].name, defenders_sorted[i].comb)
                i += 1
        elif args[0].lower() == "solo" and args[1].lower() == "tackles":
            defenders_sorted = sorted(defends, key = lambda x: int(x.solo), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "SOLO")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenders_sorted[i].name, defenders_sorted[i].solo)
                i += 1
        elif args[0].lower() == "assisted" and args[1].lower() == "tackles":
            defenders_sorted = sorted(defends, key = lambda x: int(x.ast), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "AST")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenders_sorted[i].name, defenders_sorted[i].ast)
                i += 1
        else:
            df_count = 0
            df_name = args[0].lower() + " " + args[1].lower()
            while df_count < len(defends):
                df_name2 = defends[df_count].name.split(" ")
                if df_name == (df_name2[0].lower() + " " + df_name2[1].lower()):
                    str = str + '{:20}{:4}{:4}{:4}{:5}{:5}{:4}{:4}\n'.format("NAME", "INT", "FF", "SCK", "COMB", "SOLO", "AST", "QBH")
                    str = str + '{:20}{:4}{:4}{:4}{:5}{:5}{:4}{:4}\n'.format(defends[df_count].name, defends[df_count].ints, defends[df_count].ff, defends[df_count].sacks, defends[df_count].comb, defends[df_count].solo, defends[df_count].ast, defends[df_count].qb_hits)
                    break
                df_count += 1

    if len(args) > 2:
        i = 0
        str = str + '{:20}{:4}{:4}{:4}{:5}{:5}{:4}{:4}\n'.format("NAME", "INT", "FF", "SCK", "COMB", "SOLO", "AST", "QBH")
        if args[0].lower() == "compare":
            df_comps = []
            df_count = 0
            i = 1
            j = 2
            argLen = len(args)
            while i < argLen - 1:
                df_comps.append(args[i] + " " + args[j])
                i += 2
                j += 2
            if len(df_comps) == 0:
                await ctx.message.add_reaction(emoji=reaction)
                return
            while df_count < len(defends):
                k = 0
                df_name2 = defends[df_count].name.split(" ")
                while k < len(df_comps):
                    if df_comps[k].lower() == (df_name2[0].lower() + " " + df_name2[1].lower()):
                        str = str + '{:20}{:4}{:4}{:4}{:5}{:5}{:4}{:4}\n'.format(defends[df_count].name, defends[df_count].ints, defends[df_count].ff, defends[df_count].sacks, defends[df_count].comb, defends[df_count].solo, defends[df_count].ast, defends[df_count].qb_hits)
                    k+=1
                df_count += 1
        else:
            str = "```\n"
    str = str + "\n```"
    if str == "```\n\n```":
        await ctx.message.add_reaction(emoji=reaction)
        return

    await ctx.send(
        str
    )
#######################################################################################Team defense
global team_abr_map
team_abr_map = dict(ari = "arizona cardinals", atl = "atlanta falcons", buf = "buffalo bills", bal = "baltimore ravens", car = "carolina panthers", cin = "cincinnati bengals", cle = "cleveland browns", chi = "chicago bears", dal = "dallas cowboys", den = "denver broncos", det = "detroit lions", gb = "green bay packers", hou = "houston texans", ind = "indianapolis colts", kc = "kansas city chiefs", lac = "los angeles chargers", lar = "los angeles rams", jax = "jacksonville jaguars", mia = "miami dolphins", min = "minnesota vikings", ne = "new england patriots", no = "new orleans saints", nyg = "new york giants", nyj = "new york jets", lv = "las vegas raiders", phi = "philadelphia eagles", sf = "san francisco 49ers", sea = "seattle seahawks", tb = "tampa bay buccaneers", ten = "tennessee titans", was = "washington football team" )
@client.command()
async def tdefense(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    defenses = []
    i = 1
    team_def_rows = t7.team_def_rows
    for row in team_def_rows:
        stats = row.find_all(attrs={"data-stat":True})
        defenses.append(team_defense(stats[i].text, stats[i+2].text, stats[i+3].text, stats[i+5].text, stats[i+6].text, stats[i+7].text, stats[i+9].text, stats[i+10].text, stats[i+11].text, stats[i+12].text, stats[i+13].text, stats[i+14].text, stats[i+16].text, stats[i+17].text, stats[i+18].text, stats[i+19].text, stats[i+21].text, stats[i+22].text))
    if len(args) == 1:
        i = 0
        if args[0].lower() == "y/p":
            defenses_sorted = sorted(defenses, key = lambda x: float(x.ypp), reverse=False)
            str = str + '{:25}{:3}\n'.format("TEAM", "Y/P")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].ypp)
                i += 1
        elif args[0].lower() == "yards" or args[0].lower() == "yds":
            defenses_sorted = sorted(defenses, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "YDS")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenses_sorted[i].name, defenses_sorted[i].yards)
                i += 1
        elif args[0].lower() == "receptions" or args[0].lower() == "recs":
            defenses_sorted = sorted(defenses, key = lambda x: int(x.yards), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "REC")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenses_sorted[i].name, defenses_sorted[i].rec)
                i += 1
        elif args[0].lower() == "long" or args[0].lower() == "lng":
            defenses_sorted = sorted(defenses, key = lambda x: int(x.long), reverse=True)
            str = str + '{:20}{:4}\n'.format("NAME", "LNG")
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenses_sorted[i].name, defenses_sorted[i].long)
                i += 1
        elif args[0].lower() == "y/g":
            str = str + '{:20}{:5}\n'.format("NAME", "Y/G")
            defenses_sorted = sorted(defenses, key = lambda x: float(x.yg), reverse=True)
            while i < 10:
                str = str + '{:20}{:4}\n'.format(defenses_sorted[i].name, defenses_sorted[i].yg)
                i += 1
        elif args[0].lower() == "fumbles" or args[0].lower() == "fmb":
            str = str + '{:20}{:5}\n'.format("NAME", "FMB")
            defenses_sorted = sorted(defenses, key = lambda x: float(x.fmb), reverse=True)
            count = 0
            while i < len(defenses_sorted):
                if count == 10:
                    break
                if(defenses_sorted[i].pos.lower() == "team_def"):
                    str = str + '{:20}{:4}\n'.format(defenses_sorted[i].name, defenses_sorted[i].fmb)
                    count += 1
                i += 1
        else:
            team_def_count = 0
            team_def_name = team_abr_map[args[i].lower()]
            while team_def_count < len(defenses):
                if team_def_name == defenses[team_def_count].team.lower():
                    str = str + '{:20}{:4}{:5}{:4}{:4}{:7}\n'.format("NAME", "PA", "YDS", "INT", "FUM", "PEN/YDS")
                    str = str + '{:20}{:4}{:5}{:4}{:4}{:7}\n'.format(defenses[team_def_count].team[:19], defenses[team_def_count].points_allowed, defenses[team_def_count].yards_allowed, defenses[team_def_count].ints, defenses[team_def_count].fumbles, defenses[team_def_count].penalty_yards)
                    break
                team_def_count += 1

    if len(args) == 2:

        i = 0
        if args[0].lower() == "y/p" and args[1].lower() == "top":
            defenses_sorted = sorted(defenses, key = lambda x: float(x.ypp), reverse=False)
            str = str + '{:25}{:3}\n'.format("TEAM", "Y/P")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].ypp)
                i += 1
        elif args[0].lower() == "y/p" and args[1].lower() == "bottom":
            defenses_sorted = sorted(defenses, key = lambda x: float(x.ypp), reverse=True)
            str = str + '{:25}{:3}\n'.format("TEAM", "Y/P")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].ypp)
                i += 1
        elif args[0].lower() == "turnovers" and args[1].lower() == "top":
            defenses_sorted = sorted(defenses, key = lambda x: float(x.turnovers), reverse=True)
            str = str + '{:25}{:3}\n'.format("TEAM", "TO")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].turnovers)
                i += 1
        elif args[0].lower() == "turnovers" and args[1].lower() == "bottom":
            defenses_sorted = sorted(defenses, key = lambda x: float(x.turnovers), reverse=False)
            str = str + '{:25}{:3}\n'.format("TEAM", "TO")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].turnovers)
                i += 1

    if len(args) > 2:
        if args[0].lower() == "points" and args[1].lower() == "allowed" and args[2].lower() == "top":
            defenses_sorted = sorted(defenses, key = lambda x: int(x.points_allowed), reverse=False)
            str = str + '{:25}{:3}\n'.format("TEAM", "PA")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].points_allowed)
                i += 1
        elif args[0].lower() == "points" and args[1].lower() == "allowed" and args[2].lower() == "bottom":
            defenses_sorted = sorted(defenses, key = lambda x: int(x.points_allowed), reverse=True)
            str = str + '{:25}{:3}\n'.format("TEAM", "PA")
            while i < 10:
                str = str + '{:25}{:3}\n'.format(defenses_sorted[i].team, defenses_sorted[i].points_allowed)
                i += 1

        elif args[0].lower() == "compare":
            str = str + '{:20}{:4}{:5}{:4}{:4}{:7}\n'.format("NAME", "PA", "YDS", "INT", "FUM", "PEN/YDS")
            team_def_comps = []
            team_def_count = 0
            i = 1
            argLen = len(args)
            while i < argLen:
                team_def_comps.append(team_abr_map[args[i].lower()])
                i += 1
            if len(team_def_comps) == 0:
                await ctx.message.add_reaction(emoji=reaction)
                return
            while team_def_count < len(defenses):
                k = 0
                team_def_name2 = defenses[team_def_count].team.lower()
                while k < len(team_def_comps):
                    if team_def_comps[k].lower() == (team_def_name2):
                        str = str + '{:20}{:4}{:5}{:4}{:4}{:7}\n'.format(defenses[team_def_count].team[:19], defenses[team_def_count].points_allowed, defenses[team_def_count].yards_allowed, defenses[team_def_count].ints, defenses[team_def_count].fumbles, defenses[team_def_count].penalty_yards)
                    k+=1
                team_def_count += 1
        else:
            str = "```\n"
    str = str + "\n```"
    if str == "```\n\n```":
        await ctx.message.add_reaction(emoji=reaction)
        return

    await ctx.send(
        str
    )


#######################################################################################INJURIES

#######################################################################################INVALID COMMAND
@client.event
async def on_command_error(ctx, error):
    await ctx.message.add_reaction(emoji=reaction)
    return

def read_token_settings():
    #Settings file
    token_filename = "settings.json"
    cwd = os.path.dirname(os.path.realpath(__file__))
    
    try:
        data = open(cwd + '/' + token_filename)
    except:
        print(token_filename + " file does not exist in " + cwd)
        return None
    
    settings = json.load(data)

    token = settings.get('TOKEN')
    if token is None:
        print("Bot token not defined. Please define one in settings.json")
        return None

    return token

#main entry point for bot
def footballBot_main():
    token = read_token_settings()
    if token:
        client.run(token)
    else:
        print("Unable to start bot. Token does not exist!")


if __name__ == '__main__':
    footballBot_main()
