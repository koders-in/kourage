import asyncio
import datetime
import json
import csv
import os
from uuid import uuid4
from sqlite3.dbapi2 import Cursor
import sqlite3
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
import embeds

machine = platform.node()
init()

logger = embeds.Logger("kourage-suggestions")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():  # Triggers when bot is ready
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions(
        Title TEXT,
        Description TEXT,
        UniqueId TEXT,
        Status TEXT,
        DiscordId TEXT,
        User TEXT,
        Remark TEXT
        )
    ''')

    db.commit()
    print("bot is ready!")

    logger.success("Kourage is running at version {0}".format("0.1.0"))

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == int(os.environ.get("REACTION_MESSAGE_ID")):
        await suggestion(payload)

# Suggestion function
async def suggestion(ctx):
    cursor = sqlite3.connect('main.sqlite')
    emojis = ['✅','❌'] 
    
    admin_embed = embeds.simple_embed(ctx,title="Suggestion Bot", description="To accept the suggestion: ✅"
    "To decline the suggestion: ❌")
    admin_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    admin_embed.set_author(name = f'suggested by {ctx.member}', icon_url = f'{ctx.member.avatar_url}')
    discordId = str(ctx.member.id)
    user = str(ctx.member.name)

    # Title
    title_embed = embeds.simple_embed(ctx,
        title = 'Please tell me the title of the Suggestion',
        description = ' This request will timeout after a minute'
    )
    sent = await bot.get_channel(ctx.channel_id).send(embed = title_embed)
    titlemessage = embeds.ctx_input(ctx, bot, sent)
    if not titlemessage:
        logger.error("Title message timeout")
        return
    logger.info("Title message"+titlemessage)
        
    # description
    description_embed = embeds.simple_embed(ctx,
        title = 'Please tell me the Description of the Suggestion',
        description = ' This request will timeout after 5 minutes'
    )
    sent2 = await bot.get_channel(ctx.channel_id).send(embed = description_embed)
    descriptionmessage = embeds.ctx_input(ctx, bot, sent2, timeout = 300.0)
    if not descriptionmessage:
        logger.error("Description message timeout")
        return
    logger.info("Description message"+descriptionmessage)
        
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
    
    sendEmbed = embeds.simple_embed(ctx, "", "")
    sendEmbed.add_field(name = 'Title', value  = f'{titlemessage}')
    sendEmbed.add_field(name = 'Description', value  = f'{descriptionmessage}')
    sendEmbed.add_field(name='Ticket ID: ', value = f'{unique_id}', inline=False) 
    sendEmbed.set_author(name = f'suggested by {ctx.member}', icon_url = f'{ctx.member.avatar_url}')
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    
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
                remarks_embed = embeds.simple_embed(ctx,
                    title = 'Any remarks to be added? ',
                    description = ' This request will timeout after 5 minutes'
                )
                
                remarks = await channel.send(embed = remarks_embed)
                remarksmessage = embeds.ctx_input(ctx, bot, remarks, timeout = 300.0)
                if not remarksmessage:
                    logger.error("Remarks message timeout")
                    return
                logger.info("Remarks message"+remarksmessage)

                sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False)
                approved_channel = bot.get_channel(int(os.environ.get("SUGGESTION_APPROVED_CHANNEL_ID")))
                await approved_channel.send(embed = sendEmbed)
                status = "Approved"

                cursor.execute('''INSERT INTO suggestions
                (Title, Description, UniqueId, Status, DiscordId, User, Remark) VALUES (?, ?, ?, ?, ?, ?, ?)''', (titlemessage, descriptionmessage, unique_id, status, str(discordId), str(user), remarksmessage))
                cursor.commit()
                cursor.close()
                
                return

            elif str(reaction.emoji) == "❌":
                await message.delete()
                remarks_embed = embeds.simple_embed(ctx,
                    title = 'Any remarks to be added? ',
                    description = ' This request will timeout after 5 minutes'
                )
                remarks = await channel.send(embed = remarks_embed)
                remarksmessage = embeds.ctx_input(ctx, bot, remarks, timeout = 300.0)
                if not remarksmessage:
                    logger.error("Remarks message timeout")
                    return
                logger.info("Remarks message"+remarksmessage)

                sendEmbed.add_field(name='Disapproved by:  ', value = f'{user}', inline=False)
                sendEmbed.add_field(name='Remarks: ',value = f'{remarksmessage}',inline=False) 
                disapproved_channel = bot.get_channel(int(os.environ.get("SUGGESTION_DISAPPROVED_CHANNEL_ID")))
                await disapproved_channel.send(embed = sendEmbed)
                status = "Disapproved"

                cursor.execute('''INSERT INTO suggestions
                (Title, Description, UniqueId, Status, DiscordId, User, Remark) VALUES (?, ?, ?, ?, ?, ?, ?)''', (titlemessage, descriptionmessage, unique_id, status, str(discordId), str(user), remarksmessage))
                cursor.commit()
                cursor.close()
            
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