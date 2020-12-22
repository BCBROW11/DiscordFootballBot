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
from team_defense import team_defense
from bs4 import BeautifulSoup
import os

# Create bot
client = commands.Bot(command_prefix='?')
#######################################################################################SCORE REQUEST THREAD

#######################################################################################INITIALIZE
@client.event
async def on_ready():
    global reaction
    reaction = "❓"
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    request = requests.get("https://www.pro-football-reference.com/years/2020/opp.htm")
    team_def_soup = BeautifulSoup(request.content, 'html.parser')
    team_def_table_div = team_def_soup.find("div", id="div_team_stats")
    table = team_def_table_div.find("tbody")
    global team_def_rows
    team_def_rows = table.find_all("tr", attrs={"class": None})
    print("defense update done")


#######################################################################################RECEVING STATS
global team_abr_map
team_abr_map = dict(az = "arizona cardinals", atl = "atlanta falcons", buf = "buffalo bills", bal = "baltimore ravens", car = "carolina panthers", cin = "cincinnati bengals", cle = "cleveland browns", chi = "chicago bears", dal = "dallas cowboys", den = "denver broncos", det = "detroit lions", gb = "green bay packers", hou = "houston texans", ind = "indianapolis colts", kc = "kansas city chiefs", lac = "los angeles chargers", lar = "los angeles rams", jax = "jacksonville jaguars", mia = "miami dolphins", min = "minnesota vikings", ne = "new england patriots", no = "new orleans saints", nyg = "new york giants", nyj = "new york jets", lv = "las vegas raiders", phi = "philadelphia eagles", sf = "san francisco 49ers", sea = "seattle seahawks", tb = "tampa bay buccaneers", ten = "tennessee titans", was = "washington football team" )
@client.command()
async def tdefense(ctx, *args):
    argLen = len(args)
    if argLen == 0:
        await ctx.message.add_reaction(emoji=reaction)
        return
    str = "```\n"
    defenses = []
    i = 1
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

@client.event
async def on_command_error(ctx, error):
    await ctx.message.add_reaction(emoji=reaction)
    return

def read_token_settings():
    #Token file located in root of workspace
    token_filename = "settings.json"
    #Get current working directory of this python file
    cwd = os.path.dirname(os.path.realpath(__file__))

    try:
        #<token_filename> is located in 1 directory above this one
        data = open(cwd + '/../' + token_filename)
    except:
        print(token_filename + " file does not exist in ../" + cwd)
        return None

    settings = json.load(data)

    token = settings.get('TOKEN')
    if token is None:
        print("Bot token not defined. Please define one in ../settings.json")
        return None

    return token

#main entry point for bot
def functionTest_main():
    token = read_token_settings()
    if token:
        client.run(token)
    else:
        print("Unable to start bot. Token does not exist!")


if __name__ == '__main__':
    functionTest_main()
