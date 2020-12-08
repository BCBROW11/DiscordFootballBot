import discord
import requests
import json
import yaml
from discord.ext import commands
from prettytable import PrettyTable
import http.client

# Credentials
TOKEN = '<YOUR TOKEN>'

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command()
async def scores(ctx):

    request = requests.get("http://static.nfl.com/liveupdate/scorestrip/scorestrip.json")
    str = request.text
    str = str.replace(",,", ",\"\",")
    str = str.replace(",,", ",\"\",")
    y = json.loads(str)
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
            scoreEmbed.add_field(name = '{} vs {}'.format(i[4], i[6]), value='{}\n'.format(i[0]) + ("%02d:%02d" + setting) % (hours, minutes), inline = True)
        else:
            scoreEmbed.add_field(name = '{} vs {}'.format(i[4], i[6]), value='{} {}\n{} {}\n{} {}'.format(i[4], i[5], i[6], i[7], i[2], i[3]), inline = True)
    scoreEmbed.color = discord.Color.green()

    await ctx.send(
            embed = scoreEmbed
    )

client.run(TOKEN)
