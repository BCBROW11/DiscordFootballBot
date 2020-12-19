import discord
import requests
import json
import yaml
from discord.ext import commands
import http.client
import logging
import threading
import time
from quarterback import quarterback
from runningback import runningback
from receiver import receiver
from defend import defend
from bs4 import BeautifulSoup

# Credentials
TOKEN = 'token'

# Create bot
client = commands.Bot(command_prefix='?')
#######################################################################################SCORE REQUEST THREAD
def get_scores():
    while(True):
        global scoreRequest
        scoreRequest = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
        time.sleep(43200)
#######################################################################################STANDINGS REQUEST THREAD
def get_standings():
    while(True):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        request = requests.get("https://www.pro-football-reference.com/years/2020/", headers = headers)
        global standingsSoup
        standingsSoup = BeautifulSoup(request.content, 'html.parser')
        print("standings update done")
        time.sleep(43200)
#######################################################################################STATS REQUEST THREAD
def get_stats():
    while(True):
        request = requests.get("https://www.pro-football-reference.com/years/2020/passing.htm")
        qb_soup = BeautifulSoup(request.content, 'html.parser')
        qb_table_div = qb_soup.find("div", id="div_passing")
        table = qb_table_div.find("tbody")
        global qb_rows
        qb_rows = table.find_all("tr", attrs={"class": None})
        print("quarterbacks update done")
        request = requests.get("https://www.pro-football-reference.com/years/2020/rushing.htm")
        rb_soup = BeautifulSoup(request.content, 'html.parser')
        rb_table_div = rb_soup.find("div", id="div_rushing")
        table = rb_table_div.find("tbody")
        global rb_rows
        rb_rows = table.find_all("tr", attrs={"class": None})
        print("runningbacks update done")
        request = requests.get("https://www.pro-football-reference.com/years/2020/receiving.htm")
        wr_soup = BeautifulSoup(request.content, 'html.parser')
        wr_table_div = wr_soup.find("div", id="div_receiving")
        table = wr_table_div.find("tbody")
        global wr_rows
        wr_rows = table.find_all("tr", attrs={"class": None})
        print("receivers update done")
        time.sleep(43200)

def get_def_stats():
    while(True):
        request = requests.get("https://www.pro-football-reference.com/years/2020/defense.htm")
        df_soup = BeautifulSoup(request.content, 'html.parser')
        df_table_div = df_soup.find("div", id="div_defense")
        table = df_table_div.find("tbody")
        global df_rows
        df_rows = table.find_all("tr", attrs={"class": None})
        print("defense update done")
        time.sleep(43200)

#######################################################################################INITIALIZE
@client.event
async def on_ready():
    global reaction
    reaction = "❓"
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    req = threading.Thread(target=get_standings)
    req2 = threading.Thread(target=get_scores)
    req3 = threading.Thread(target=get_stats)
    req4 = threading.Thread(target=get_def_stats)
    req.start()
    req2.start()
    req3.start()
    req4.start()

#######################################################################################STANDINGS
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
##########################################################################SCORES
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
#######################################################################################HELP COMMAND
@client.command()
async def NFLBotHelp(ctx):
    str = "```\n Commands: ?standings | ?standings <conference:division> (afce, nfce, etc) | ?scores | ?scores <team> (SEA, JAX, LAC, etc) | ?fbref <firstName> <lastName>\n```"
    await ctx.send(
        str
    )
#######################################################################################FBREF LINKER
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
#######################################################################################QUARTERBACK STATS

@client.command()
async def qb(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    quarterbacks = []
    i = 1
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
#######################################################################################RUNNINGBACK STATS

@client.command()
async def rb(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    runningbacks = []
    i = 1
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
#######################################################################################RECEVING STATS

@client.command()
async def wr(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    receivers = []
    i = 1
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
#######################################################################################DEFENSIVE STATS
@client.command()
async def defense(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    defends = []
    i = 1
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
#######################################################################################SPECIAL TEAMS STATS

#######################################################################################INJURIES

#######################################################################################INVALID COMMAND
@client.event
async def on_command_error(ctx, error):
    await ctx.message.add_reaction(emoji=reaction)
    return

client.run(TOKEN)
