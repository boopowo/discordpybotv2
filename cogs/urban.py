import discord
import datetime
import pytz
from discord.ext import commands
from datetime import datetime
import requests
import bs4
from bs4 import BeautifulSoup

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def current_time():
    utc_time = datetime.now(tz=pytz.UTC)
    tz_chicago = utc_time.astimezone(pytz.timezone('America/Chicago'))
    return tz_chicago.strftime("%Y-%m-%d %H:%M:%S (America/Chicago)")

class urban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('urban Ready {}'.format(current_time()))

    @commands.command()
    async def urban(self, ctx, *, term):
        try:
            term.replace(' ', '+')
            request = requests.get('https://www.urbandictionary.com/define.php?term={}'.format(term), headers = header)
            soup = BeautifulSoup(request.content, 'html.parser')
            title = soup.title.string
            meaning = soup.find('div', {'class': 'meaning'}).get_text()
            example = soup.find('div', {'class': 'example'}).get_text()
            result = '{}\n\nDefinition:\n\n{}\n\nExample:\n\n{}'.format(title, meaning, example)
            await ctx.send(result)
        except Exception as e:
            await ctx.send('{} cannot be found'.format(term))
        
            

def setup(client):
    client.add_cog(urban(client))