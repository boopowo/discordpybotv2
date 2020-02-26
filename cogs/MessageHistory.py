import discord
import datetime
import pytz
import time
from discord.ext import commands
from datetime import datetime


def current_time():
    utc_time = datetime.now(tz=pytz.UTC)
    tz_chicago = utc_time.astimezone(pytz.timezone('America/Chicago'))
    return tz_chicago.strftime("%Y-%m-%d %H:%M:%S (America/Chicago)")

class MessageHistory(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('MessageHistory Ready {}'.format(current_time()))
    
    @commands.command()
    async def words_top(self, ctx, words, message_amount, guild_name, channel_name):
        start_time = time.time()
        valid_server = False
        valid_channel = False
        await ctx.send('Attempting to retrieve top {} words through past {} messages in server: "{}" channel: #{}\nThis might take a while...'.format(
            words, message_amount,guild_name,channel_name
            ))
        try:
            channel_list = []
        
            for guild in self.client.guilds:
                if str(guild.name) == str(guild_name):
                    found_guild = guild
                    valid_server = True

            for channel in found_guild.channels:
                if str(channel.name) == str(channel_name):
                    found_channel = channel
                    valid_channel = True
            
            word_list = {}
            messages = await found_channel.history(limit = int(message_amount)).flatten()
            message_content = []
            for message in messages:
                message_content.append(message.content.lower())
            for i in range(len(message_content)):
                splt = message_content[i].split()
                for j in range(len(splt)):
                    s = ""
                    for k in range(len(splt[j])):
                        letter = splt[j][k]
                        if letter.isalnum():
                            s += letter
                    if len(s) == 0:
                        pass
                    elif s in word_list:
                        word_list[s] += 1
                    else:
                        word_list[s] = 1
            sorted_wordlist = dict(sorted(word_list.items(), key = lambda x:x[1], reverse = True))
            output = "{:<10} {:<30} {:<10}\n".format(
                "Rank", "Word", "Frequency"
            )
            rank = 1
            for word in sorted_wordlist:
                output += "{:<10} {:<30} {:<10}\n".format(
                    str(rank), str(word), str(sorted_wordlist[word]))
                rank += 1
                if int(rank) > int(words):
                    break
            end_time = time.time()
            execution_time = end_time - start_time
            await ctx.send("```{:<10} {:<10}\n{:<10} {:<30} {:<15} {:<10}\n{}```".format(
                "Time: " + str(current_time()), "Execution time: " + str(execution_time), "Top: " + str(words), "Messages: " + str(message_amount), 
                "Server: " + str(guild_name), "Channel: #" + str(channel_name), output
            ))
        except UnboundLocalError:
            if valid_server == False:
                await ctx.send("Server not found")
            elif valid_channel == False:
                await ctx.send("Channel not found")
        except Exception as e:
            if len(output) > 1500:
                await ctx.send('Result may be too long for discord. Will fix in the future.')
            print(e)
            
    @commands.command()
    async def users_top(self, ctx, users, message_amount, guild_name, channel_name):
        start_time = time.time()
        valid_server = False
        valid_channel = False
        await ctx.send('Attempting to retrieve top {} users through last {} messages in server: "{}" channel: #{}\nThis might take a while...'.format(
            users, message_amount,guild_name,channel_name
        ))
        try:
            channel_list = []
        
            for guild in self.client.guilds:
                if str(guild.name) == str(guild_name):
                    found_guild = guild
                    valid_server = True

            for channel in found_guild.channels:
                if str(channel.name) == str(channel_name):
                    found_channel = channel
                    valid_channel = True
            
            user_list = {}
            messages = await found_channel.history(limit = int(message_amount)).flatten()
            message_author = []
            for message in messages:
                message_author.append(message.author)
            for i in range(len(message_author)):
                if message_author[i] in user_list:
                    user_list[message_author[i]] += 1
                else:
                    user_list[message_author[i]] = 1
            sorted_userlist = dict(sorted(user_list.items(), key = lambda x:x[1], reverse = True))
            output = "{:<10} {:<30} {:<10}\n".format(
                "Rank", "User", "Frequency"
            )
            rank = 1
            for user in sorted_userlist:
                output += '{:<10} {:<30} {:<10}\n'.format(
                    str(rank), str(user), str(sorted_userlist[user]))
                rank += 1
                if int(rank) > int(users):
                    break
            end_time = time.time()
            execution_time = end_time - start_time
            await ctx.send("```{:<10} {:<10}\n{:<10} {:<30} {:<15} {:<10}\n{}```".format(
                "Time: " + str(current_time()), "Execution time: " + str(execution_time), "Top: " + str(users), "Messages: " + str(message_amount), 
                "Server: " + str(guild_name), "Channel: #" + str(channel_name), output
            ))
        except UnboundLocalError:
            if valid_server == False:
                await ctx.send("Server not found")
            elif valid_channel == False:
                await ctx.send("Channel not found")
        except Exception as e:
            if len(output) > 1500:
                await ctx.send('Result may be too long for discord. Will fix in the future.')
            print(e)
def setup(client):
    client.add_cog(MessageHistory(client))
        
