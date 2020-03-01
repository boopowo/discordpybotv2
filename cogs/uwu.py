import discord
import datetime
import pytz
import re

from discord.ext import commands
from datetime import datetime

def current_time():
    utc_time = datetime.now(tz=pytz.UTC)
    tz_chicago = utc_time.astimezone(pytz.timezone('America/Chicago'))
    return tz_chicago.strftime("%Y-%m-%d %H:%M:%S (America/Chicago)")

class uwu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('uwu Ready {}'.format(current_time()))

    @commands.command()
    async def uwu(self, ctx):
        message = await ctx.channel.history(limit = 2).flatten()
        content = message[1].content
        content = re.sub('l|r|v', 'w', content)
        content = re.sub('L|R|V', 'W', content)
        await ctx.send(content + " uwu")
    
    @commands.command()
    async def uwutranslate(self, ctx, * , string):
        string = re.sub('l|r|v', 'w', string)
        string = re.sub('L|R|V', 'W', string)
        await ctx.send(string + " uwu")

def setup(client):
    client.add_cog(uwu(client))