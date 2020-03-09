import discord
import datetime
import pytz
from discord.ext import commands
from datetime import datetime

def current_time():
    utc_time = datetime.now(tz=pytz.UTC)
    tz_chicago = utc_time.astimezone(pytz.timezone('America/Chicago'))
    return tz_chicago.strftime("%Y-%m-%d %H:%M:%S (America/Chicago)")

class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ErrorHandling Ready {}'.format(current_time()))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            #print('Command not found {}'.format(current_time()))
            await ctx.send('Command not found')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send('Extension already loaded')
        else:
            print('{} {}'.format(error, current_time()))

def setup(client):
    client.add_cog(ErrorHandling(client))