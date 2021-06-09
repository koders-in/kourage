# Manual file imports
import asyncio
import datetime
import json
import csv
import os
from uuid import uuid4

# Logging format
import logging
import platform
import time


import discord
import requests
from colorama import init
from discord.utils import get
from discord.ext import commands
from discord.ext.tasks import loop
from termcolor import colored

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
import config as CONFIG  # Capitals for global

class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def success(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', color))


logger = Logger("kourage-boilerplate")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.success("Kourage is running at version {0}".format(CONFIG.VERSION))

# Suggestion command
@bot.command()
# @commands.has_any_role("Koders")
async def suggestion(ctx):
    emojis = ['✅','❌'] 

    # set ADMIN_CHANNEL_ID = 849583285645475850
    # channel = bot.get_channel(CONFIG.ADMIN_CHANNEL_ID)
    channel = bot.get_channel(CONFIG.ADMIN_CHANNEL_ID)
    
    await ctx.channel.purge(limit=1)
    
    admin_embed = discord.Embed(colour=0x28da5b)
    admin_embed=discord.Embed(title="Suggestion Bot", description="To accept the suggestion: ✅"
                                                                    "To decline the suggestion: ❌", color=0x28da5b)
    admin_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    admin_embed.timestamp = datetime.datetime.utcnow()
    admin_embed.set_footer(text="Made with ❤️️  by Koders")
    admin_embed.set_author(name = f'suggested by {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    
    # Title
    title_embed = discord.Embed(colour=0x28da5b)
    title_embed = discord.Embed(
        title = 'Please tell me the title of the Suggestion',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed = title_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )
        
        if msg:
            await sent.delete()
            titlemessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)
        
        
    # description
    description_embed = discord.Embed(colour=0x28da5b)
    description_embed = discord.Embed(
        title = 'Please tell me the Description of the Suggestion',
        description = ' This request will timeout after 5 minutes'
    )
    sent2 = await ctx.send(embed = description_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )
        
        if msg:
            await sent2.delete()
            descriptionmessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent2.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300.0)
        
    # Unique ID
    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()
    
    admin_embed.add_field(name='Ticket ID: ', value = f'{unique_id}', inline=False)    
    admin_embed.add_field(name = 'Title', value  = f'{titlemessage}',inline = False)
    admin_embed.add_field(name = 'Description', value  = f'{descriptionmessage}',inline = False)

    
    # with open('suggestions.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames = ['Title', 'Description', 'ID', 'Status','Suggested By','Acknowledged By','Remarks'] )
    #     writer.writeheader()
    #     f.close()
    # make a csv called suggestions 
    
    message = await channel.send(embed = admin_embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    
    sendEmbed = discord.Embed(colour = 0x28da5b)
    # sendEmbed.add_field(name = 'New Suggestion!', value  = f'{suggestion}')
    sendEmbed.add_field(name = 'Title', value  = f'{titlemessage}')
    sendEmbed.add_field(name = 'Description', value  = f'{descriptionmessage}')
    sendEmbed.add_field(name='Ticket ID: ', value = f'{unique_id}', inline=False) 
    sendEmbed.set_author(name = f'suggested by {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.timestamp = datetime.datetime.utcnow()
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    
    def check (reaction, user):
        return not user.bot and message == reaction.message
    
    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run because of like 31,32
        # Role logic
        role_string = ''
        for role in user.roles:
            if(role.name == '@everyone'):
                continue
            else:
                role_string += role.name
                role_string += ','
        role_string = role_string[:-1]
        
        while reaction.message == message:
            if str(reaction.emoji) == "✅":
                
                # Remarks Embed
                remarks_embed = discord.Embed(colour=0x28da5b)
                remarks_embed = discord.Embed(
                    title = 'Any remarks to be added? ',
                    description = ' This request will timeout after 5 minutes'
                )
                
                remarks = await channel.send(embed = remarks_embed)
                try:
                    msg = await bot.wait_for(
                        "message",
                        timeout=300.0,
                        check=lambda message: message.author == ctx.author
                    )
                    
                    if msg:
                        await remarks.delete()
                        remarksmessage = msg.content
                        await msg.delete()
                
                except asyncio.TimeoutError:
                    await remarks.delete()
                    await channel.send('Cancelling due to timeout.', delete_after = 300.0)
                    
                # CSV File logic
                data = []

                data.append(titlemessage)
                data.append(descriptionmessage)
                data.append(unique_id)
                data.append("Approved")
                data.append(ctx.message.author)
                data.append(user)
                data.append(remarksmessage)
                
                with open('suggestions.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)

                del data
                                    
                await ctx.send(f'🙌🙌 Bravo!! Your suggestion has been Acknowledged by {user} who has these roles ({role_string}). We appreciate your efforts!')
                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False)
                
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                
                await channel.send(f'suggestion of {ctx.message.author}, with ID: {unique_id} has been approved by {user} who has these roles ({role_string}), this post will no longer be active')
                return
            if str(reaction.emoji) == "❌":
                
                # Remarks Embed
                remarks_embed = discord.Embed(colour=0x28da5b)
                remarks_embed = discord.Embed(
                    title = 'Any remarks to be added? ',
                    description = ' This request will timeout after 5 minutes'
                )
                
                remarks = await channel.send(embed = remarks_embed)
                try:
                    msg = await bot.wait_for(
                        "message",
                        timeout=300.0,
                        check=lambda message: message.author == ctx.author
                    )
                    
                    if msg:
                        await remarks.delete()
                        remarksmessage = msg.content
                        await msg.delete()
                
                except asyncio.TimeoutError:
                    await remarks.delete()
                    await channel.send('Cancelling due to timeout.', delete_after = 300.0)
                
                await ctx.send(f'🌸 Sorry! Your suggestion has not been Acknowledged by {user} who has these roles ({role_string}). We thank you for your valuable time!')
                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                
                # CSV Logic
                data = []

                data.append(titlemessage)
                data.append(descriptionmessage)
                data.append(unique_id)
                data.append("Rejected")
                data.append(ctx.message.author)
                data.append(user)
                data.append(remarksmessage)
                
                with open('suggestions.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    # write the data
                    writer.writerow(data)

                del data
                    
                await channel.send(f'suggestion of {ctx.message.author}, with ID: {unique_id} has not been approved by {user} who has these roles ({role_string}), this post will no longer be active')
                return
    except asyncio.TimeoutError:
        await ctx.send("Your suggestion was timed out. Please try again!")
        return

if __name__ == "__main__":
    try:
        bot.run('ODQ5NTY2Mzk1NjM3MTcwMTc2.YLdCXA.Jq-76rr3NpcSZcDfzGMfy13Bl2o')
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
