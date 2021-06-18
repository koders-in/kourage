import asyncio
import datetime
import json
import csv
import os
from uuid import uuid4
import logging
import platform
import time
import os

import discord
import requests
from colorama import init
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.tasks import loop
from termcolor import colored

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

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

logger = Logger("kourage-suggestion")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.success("Kourage is running at version {0}".format("0.1.0"))

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == int(os.environ.get("REACTION_MESSAGE_ID")):
        # await suggestion(payload)
        #print(payload.member)
        #print(payload.channel_id)
        #print(payload.guild_id)
        #print(payload.member.avatar_url)
        await suggestion(payload)

# Suggestion function
async def suggestion(ctx):
    emojis = ['✅','❌'] 
    admin_embed = discord.Embed(colour=0x28da5b)
    admin_embed=discord.Embed(title="Suggestion Bot", description="To accept the suggestion: ✅"
                                                                    "To decline the suggestion: ❌", color=0x28da5b)
    admin_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    admin_embed.timestamp = datetime.datetime.utcnow()
    admin_embed.set_footer(text="Made with ❤️️  by Koders")
    admin_embed.set_author(name = f'suggested by {ctx.member}', icon_url = f'{ctx.member.avatar_url}')
    
    # Title
    title_embed = discord.Embed(colour=0x28da5b)
    title_embed = discord.Embed(
        title = 'Please tell me the title of the Suggestion',
        description = ' This request will timeout after a minute'
    )
    sent = await bot.get_channel(ctx.channel_id).send(embed = title_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.member
        )
        
        if msg:
            await sent.delete()
            titlemessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 60.0)
        
    # description
    description_embed = discord.Embed(colour=0x28da5b)
    description_embed = discord.Embed(
        title = 'Please tell me the Description of the Suggestion',
        description = ' This request will timeout after 5 minutes'
    )
    sent2 = await bot.get_channel(ctx.channel_id).send(embed = description_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.member
        )
        
        if msg:
            await sent2.delete()
            descriptionmessage = msg.content
            await msg.delete()
    
    except asyncio.TimeoutError:
        await sent2.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300.0)
        
    # Unique ID
    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()
    
    admin_embed.add_field(name='Ticket ID: ', value = f'{unique_id}', inline=False)    
    admin_embed.add_field(name = 'Title', value  = f'{titlemessage}',inline = False)
    admin_embed.add_field(name = 'Description', value  = f'{descriptionmessage}',inline = False)

    channel = bot.get_channel(int(os.environ.get("ADMIN_CHANNEL_ID")))
    message = await channel.send(embed = admin_embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    
    sendEmbed = discord.Embed(colour = 0x28da5b)
    sendEmbed.add_field(name = 'Title', value  = f'{titlemessage}')
    sendEmbed.add_field(name = 'Description', value  = f'{descriptionmessage}')
    sendEmbed.add_field(name='Ticket ID: ', value = f'{unique_id}', inline=False) 
    sendEmbed.set_author(name = f'suggested by {ctx.member}', icon_url = f'{ctx.member.avatar_url}')
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.timestamp = datetime.datetime.utcnow()
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    
    def check (reaction, user):
        return not user.bot and message == reaction.message
    
    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) 

        # Role logic for displaying the maximum authority over roles
        roles = []
        for role in user.roles:
            if(role.name == '@everyone'):
                continue
            else:
                roles.append(role)
        
        while reaction.message == message:
            if str(reaction.emoji) == "✅":
                await message.delete()
                
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
                        check=lambda message: message.author == user
                    )
                    
                    if msg:
                        await remarks.delete()
                        remarksmessage = msg.content
                        await msg.delete()
                
                except asyncio.TimeoutError:
                    await remarks.delete()
                    await channel.send('Cancelling due to timeout.', delete_after = 300.0)
                    
                data = []
                data.append(titlemessage)
                data.append(descriptionmessage)
                data.append(unique_id)
                data.append("Approved")
                data.append(ctx.member)
                data.append(user)
                data.append(remarksmessage)
                
                with open('suggestions.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                del data
                                    
                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False)
                approved_channel = bot.get_channel(int(os.environ.get("SUGGESTION_APPROVED_CHANNEL_ID")))
                await approved_channel.send(embed = sendEmbed)
                
                return

            elif str(reaction.emoji) == "❌":
                await message.delete()
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
                        check=lambda message: message.author == user
                    )
                    if msg:
                        await remarks.delete()
                        remarksmessage = msg.content
                        await msg.delete()
                except asyncio.TimeoutError:
                    await remarks.delete()
                    await channel.send('Cancelling due to timeout.', delete_after = 300.0)
                
                sendEmbed.add_field(name='Disapproved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False) 
                disapproved_channel = bot.get_channel(int(os.environ.get("SUGGESTION_DISAPPROVED_CHANNEL_ID")))
                await disapproved_channel.send(embed = sendEmbed)
                
                data = []
                data.append(titlemessage)
                data.append(descriptionmessage)
                data.append(unique_id)
                data.append("Rejected")
                data.append(ctx.member)
                data.append(user)
                data.append(remarksmessage)
                
                with open('suggestions.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                del data
                    
                return
    except asyncio.TimeoutError:
        await bot.get_channel(ctx.channel_id).send("Your suggestion was timed out. Please try again!")
        return

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
    except CommandNotFound:
        pass # For handling command not found errors
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)