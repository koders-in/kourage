import discord
import platform
import logging
import time
import datetime
import asyncio
import base64
from uuid import uuid4
import sqlite3
from sqlite3.dbapi2 import Cursor
from colorama import init
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
import config as CONFIG  # Capitals for global

class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def warning(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', color))


logger = Logger("kourage-boilerplate")

# FOR TESTING
# bot = commands.Bot(command_prefix="!")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

# Create User Profile Command
async def user(ctx):
    suggestEmbed1 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Name',
        description = " Write your full name ."
    )
    suggestEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed1.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed1.timestamp = datetime.datetime.utcnow()
    
    sent1 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed1)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=120.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent1.delete()
            message1 = msg.content
            await msg.delete()    

    except asyncio.TimeoutError:
        await sent1.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

    cursor = sqlite3.connect('main.sqlite')
    
    suggestEmbed2 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Phone Number',
        description = """ Write your phone number. """
        )
    suggestEmbed2.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed2.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed2.timestamp = datetime.datetime.utcnow()
    
    sent2 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed2)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent2.delete()
            message2 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent2.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)

    suggestEmbed3 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Mail Id',
        description = """ Write your email id. """
    )
    suggestEmbed3.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed3.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed3.timestamp = datetime.datetime.utcnow()

    sent3 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed3)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent3.delete()
            message3 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent3.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
    suggestEmbed4 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Birthday',
        description = " Write your birthday date in dd/mm/yyyy in this format. "
    )
    suggestEmbed4.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed4.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed4.timestamp = datetime.datetime.utcnow()
    
    sent4 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed4)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent4.delete()
            message4 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent4.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
    suggestEmbed5 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your WhatsApp Number ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed5.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    
    suggestEmbed5.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed5.timestamp = datetime.datetime.utcnow()

    message = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed5)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
           # await ctx.send('Thanks for letting us know your whatsapp number!')
            suggestEmbed9 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your WhatsApp Number.',
                description = " Write you phone number. "
                )
            suggestEmbed9.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed9.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed9.timestamp = datetime.datetime.utcnow()

            sent5 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed9)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.member
                )

                if msg:
                    await sent5.delete()
                    message5 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent5.delete()
                await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message5 = None
               
    except asyncio.TimeoutError:
        await bot.get_channel(ctx.channel_id).send("Time out. Please try again!")
      
    suggestEmbed6 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your Facebook Id ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed6.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed6.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed6.timestamp = datetime.datetime.utcnow()
    
    message = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed6)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
           # await ctx.send('Thanks for letting us know your Facebook Id!')
            suggestEmbed10 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your Facebook Id.',
                description = " Write you Facebook Id. "
                )
            suggestEmbed10.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed10.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed10.timestamp = datetime.datetime.utcnow()

            sent6 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed10)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.member
                )

                if msg:
                    await sent6.delete()
                    message6 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent6.delete()
                await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message6 = None
               
    except asyncio.TimeoutError:
        await bot.get_channel(ctx.channel_id).send("Time out. Please try again!")

    suggestEmbed7 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your Instagram Id username ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed7.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed7.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed7.timestamp = datetime.datetime.utcnow()
    
    message = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed7)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
           # await ctx.send('Thanks for letting us know your Instagram Id!')
            suggestEmbed11 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your Instagram Id.',
                description = " Write you Instagram Id. "
                )
            suggestEmbed11.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed11.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed11.timestamp = datetime.datetime.utcnow()

            sent7 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed11)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.member
                )

                if msg:
                    await sent7.delete()
                    message7 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent7.delete()
                await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message7 = None
               
    except asyncio.TimeoutError:
        await bot.get_channel(ctx.channel_id).send("Time out. Please try again!")

    suggestEmbed8 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Redmine API Key',
        description = " Write your Redmine API Key. "
    )
    suggestEmbed8.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed8.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed8.timestamp = datetime.datetime.utcnow()
    
    sent8 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed8)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent8.delete()
            message8 = msg.content
            message9 = message8[:-3] + '***'
            message8 = base64.b64encode(message8.encode("ascii"))
           # print(message9)
            await msg.delete()

    except asyncio.TimeoutError:
        await sent8.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 300)
        
    msg9 = ctx.member.id

    suggestEmbed12 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your role at Koders',
        description = " Write your role name at Koders like Developer, Design, Content and Marketing."
    )
    suggestEmbed12.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed12.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed12.timestamp = datetime.datetime.utcnow()
    
    sent12 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed12)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=120.0,
            check=lambda message: message.author == ctx.member
        )

        if msg:
            await sent12.delete()
            message10 = msg.content
            await msg.delete()    

    except asyncio.TimeoutError:
        await sent12.delete()
        await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)


    sendEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile',
        description = " All the information about the user profile like name, phone, mail and so on. "
    )
    sendEmbed.set_thumbnail(url=user.avatar_url)
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()


    sendEmbed.add_field(name='Name', value = f'{message1}', inline=False)   
    sendEmbed.add_field(name='Phone Number', value = f'{message2}', inline=False) 
    sendEmbed.add_field(name='Mail Id', value = f'{message3}', inline=False)
    sendEmbed.add_field(name='Birthday', value = f'{message4}', inline=False)
    sendEmbed.add_field(name='WhatsApp Number', value = f'{message5}', inline=False) 
    sendEmbed.add_field(name='Facebook Id', value = f'{message6}', inline=False)
    sendEmbed.add_field(name='Instagram Id', value = f'{message7}', inline=False)
    sendEmbed.add_field(name='Redmine API Key', value = f'{message9}', inline=False)
    sendEmbed.add_field(name='Roles', value = f'{message10}', inline=False)


    # Developer role 
    suggestEmbed13 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite Language ?',
        description = " Write name of your favourite language like which use most eg: python, c++, etc."
    )
    suggestEmbed13.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed13.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed13.timestamp = datetime.datetime.utcnow()


    suggestEmbed14 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite Text-editor/Ide ?',
        description = " Write name of your favourite code-editor like which use most eg: vscode, atom, vim, etc."
    )
    suggestEmbed14.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed14.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed14.timestamp = datetime.datetime.utcnow()


    suggestEmbed15 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your skills ?',
        description = " Write your skills."
    )
    suggestEmbed15.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed15.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed15.timestamp = datetime.datetime.utcnow()


    suggestEmbed16 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your previous projects ?',
        description = " Write your about previous projects."
    )
    suggestEmbed16.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed16.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed16.timestamp = datetime.datetime.utcnow()


    if message10 == "Developer":
        sent13 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed13)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent13.delete()
                message11 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent13.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent14 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed14)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent14.delete()
                message12 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent14.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent15 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed15)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent15.delete()
                message13 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent15.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent16 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed16)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent16.delete()
                message14 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent16.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)


        sendEmbed.add_field(name='Favourite Language', value = f'{message11}', inline=False)
        sendEmbed.add_field(name='Favourite Text-editor/Ide', value = f'{message12}', inline=False)
        sendEmbed.add_field(name='Skills', value = f'{message13}', inline=False)
        sendEmbed.add_field(name='Previous projects', value = f'{message14}', inline=False)

        cursor.execute('''INSERT INTO main
        (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine, Discord_Id, Roles, Language, Ide, Skills, Projects) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8, msg9, message10, message11, message12, message13, message14)) 

        cursor.commit()
        #cursor.close()

    # Marketing role
    suggestEmbed17 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Bio(Thoughts) ?',
        description = " Write your bio or thoughts ."
    )
    suggestEmbed17.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed17.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed17.timestamp = datetime.datetime.utcnow()


    suggestEmbed18 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your skills ?',
        description = " Write your skills."
    )
    suggestEmbed18.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed18.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed18.timestamp = datetime.datetime.utcnow()


    suggestEmbed19 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your previous projects ?',
        description = " Write your about previous projects."
    )
    suggestEmbed19.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed19.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed19.timestamp = datetime.datetime.utcnow()


    suggestEmbed20 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite tools ?',
        description = " Write your about you favourite tools."
    )
    suggestEmbed20.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed20.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed20.timestamp = datetime.datetime.utcnow()


    suggestEmbed21 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite brand name ?',
        description = " Write name of your favourite brand."
    )
    suggestEmbed21.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed21.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed21.timestamp = datetime.datetime.utcnow()


    suggestEmbed22 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Hobbies ?',
        description = " Write about your Hobbies."
    )
    suggestEmbed22.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed22.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed22.timestamp = datetime.datetime.utcnow()


    if message10 == "Marketing":
        sent17 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed17)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent17.delete()
                message15 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent17.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent18 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed18)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent18.delete()
                message16 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent18.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent19 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed19)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent19.delete()
                message17 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent19.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent20 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed20)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent20.delete()
                message18 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent20.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent21 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed21)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent21.delete()
                message19 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent21.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent22 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed22)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent22.delete()
                message20 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent22.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)


        sendEmbed.add_field(name='Bio (Thoughts)', value = f'{message15}', inline=False)
        sendEmbed.add_field(name='Skills', value = f'{message16}', inline=False)
        sendEmbed.add_field(name='Previous Projects', value = f'{message17}', inline=False)
        sendEmbed.add_field(name='Favourite Tools', value = f'{message18}', inline=False)
        sendEmbed.add_field(name='Favourite Brand', value = f'{message19}', inline=False)
        sendEmbed.add_field(name='Hobbies', value = f'{message20}', inline=False)


        cursor.execute('''INSERT INTO main
        (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine, Discord_Id, Roles, Bio, Skills, Projects, Tools, Brand, Hobbies) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8, msg9, message10, message15, message16, message17, message18, message19, message20)) 

        cursor.commit()


    # Design role 
    suggestEmbed23 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite tools ?',
        description = " Write name of your favourite tools."
    )
    suggestEmbed23.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed23.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed23.timestamp = datetime.datetime.utcnow()


    suggestEmbed24 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Portfolio link ?',
        description = "Enter your portfolio link here."
    )
    suggestEmbed24.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed24.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed24.timestamp = datetime.datetime.utcnow()


    suggestEmbed25 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your skills ?',
        description = " Write your skills."
    )
    suggestEmbed25.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed25.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed25.timestamp = datetime.datetime.utcnow()


    suggestEmbed26 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your previous projects ?',
        description = " Write your about previous projects."
    )
    suggestEmbed26.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed26.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed26.timestamp = datetime.datetime.utcnow()


    if message10 == "Design":
        sent23 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed23)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent23.delete()
                message21 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent23.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent24 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed24)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent24.delete()
                message22 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent24.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent25 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed25)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent25.delete()
                message23 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent25.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent26 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed26)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent26.delete()
                message24 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent26.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)


        sendEmbed.add_field(name='Favourite Tools', value = f'{message21}', inline=False)
        sendEmbed.add_field(name='Portfolio', value = f'{message22}', inline=False)
        sendEmbed.add_field(name='Skills', value = f'{message23}', inline=False)
        sendEmbed.add_field(name='Previous projects', value = f'{message24}', inline=False)

    
        cursor.execute('''INSERT INTO main
        (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine, Discord_Id, Roles, Tools, Portfolio, Skills, Projects) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8, msg9, message10, message21, message22, message23, message24)) 

        cursor.commit()
        #cursor.close()


    # Content role
    suggestEmbed27 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Bio(Thoughts) ?',
        description = " Write your bio or thoughts ."
    )
    suggestEmbed27.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed27.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed27.timestamp = datetime.datetime.utcnow()


    suggestEmbed28 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your skills ?',
        description = " Write your skills."
    )
    suggestEmbed28.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed28.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed28.timestamp = datetime.datetime.utcnow()


    suggestEmbed29 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your previous projects ?',
        description = " Write your about previous projects."
    )
    suggestEmbed29.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed29.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed29.timestamp = datetime.datetime.utcnow()


    suggestEmbed30 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite tools ?',
        description = " Write your about you favourite tools."
    )
    suggestEmbed30.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed30.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed30.timestamp = datetime.datetime.utcnow()


    suggestEmbed31 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite blogs ?',
        description = " Write your favourite blogs name."
    )
    suggestEmbed31.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed31.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed31.timestamp = datetime.datetime.utcnow()


    suggestEmbed32 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Favourite books ?',
        description = " Write about or name of your favourite books."
    )
    suggestEmbed32.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed32.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed32.timestamp = datetime.datetime.utcnow()


    if message10 == "Content":
        sent27 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed27)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent27.delete()
                message25 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent27.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent28 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed18)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent28.delete()
                message26 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent28.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent29 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed29)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent29.delete()
                message27 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent29.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent30 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed30)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent30.delete()
                message28 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent30.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent31 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed31)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent31.delete()
                message29 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent31.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)

        sent32 = await bot.get_channel(ctx.channel_id).send(embed = suggestEmbed32)
        try:
            msg = await bot.wait_for(
                "message",
                timeout=120.0,
                check=lambda message: message.author == ctx.member
            )

            if msg:
                await sent32.delete()
                message30 = msg.content
                await msg.delete()    

        except asyncio.TimeoutError:
            await sent32.delete()
            await bot.get_channel(ctx.channel_id).send('Cancelling due to timeout.', delete_after = 120)


        sendEmbed.add_field(name='Bio (Thoughts)', value = f'{message25}', inline=False)
        sendEmbed.add_field(name='Skills', value = f'{message26}', inline=False)
        sendEmbed.add_field(name='Previous Projects', value = f'{message27}', inline=False)
        sendEmbed.add_field(name='Favourite Tools', value = f'{message28}', inline=False)
        sendEmbed.add_field(name='Favourite Blogs', value = f'{message29}', inline=False)
        sendEmbed.add_field(name='Favourite Books', value = f'{message30}', inline=False)
 

        cursor.execute('''INSERT INTO main
        (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine, Discord_Id, Roles, Bio, Skills, Projects, Tools, Blogs, Books) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8, msg9, message10, message25, message26, message27, message28, message29, message30)) 

        cursor.commit()


    await bot.get_channel(ctx.channel_id).send(embed = sendEmbed)

    # Admin Channel Id
    channel = bot.get_channel("")

    message = await channel.send(embed = sendEmbed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    from uuid import uuid4

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()


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
                await bot.get_channel(ctx.channel_id).send('Created User profile has been approved!')
                #sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await bot.get_channel(ctx.channel_id).send("Your profile was: ")
                message1 = await bot.get_channel(ctx.channel_id).send(embed = sendEmbed)
                
                await channel.send('Created User profile has been approved!')
                return
            if str(reaction.emoji) == "❌":
                await bot.get_channel(ctx.channel_id).send('Created User profile has not been approved!. We thank you for your valuable time!')
                #sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await bot.get_channel(ctx.channel_id).send("Your profile was: ")
                message1 = await bot.get_channel(ctx.channel_id).send(embed = sendEmbed)
                    
                await channel.send('Created User profile has not been approved!')
                return
    except asyncio.TimeoutError:
        await bot.get_channel(ctx.channel_id).send("Timeout for creating user profile. Please try again!")
        return


# User Profile Info Command
@bot.command() 
async def profile(ctx, *, username: discord.Member):

    await ctx.message.mentions[0].id
    # print(username)

    conn = sqlite3.connect('main.sqlite')

    sendEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile',
        description = " All the information about the user profile like name, phone, mail and so on. "
        )
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()

    sendEmbed1 = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile Not Found',
        description = " This user profile doesn't exists in the database. "
        )
    sendEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed1.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed1.timestamp = datetime.datetime.utcnow()

    cur = conn.cursor()
    cur.execute('''SELECT Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine FROM main WHERE Discord_Id = ?''', (username.id, ))

    rows = cur.fetchall()

    if rows is "":

        await ctx.send(embed = sendEmbed1)

    else:

        for row in rows:
            # Decoding the Api Key 
            message = base64.b64decode(row[7]).decode()
            new = message[:-3] + '***'

            sendEmbed.add_field(name='Name', value = row[0], inline=False)   
            sendEmbed.add_field(name='Phone Number', value = row[1], inline=False) 
            sendEmbed.add_field(name='Mail Id', value = row[2], inline=False)
            sendEmbed.add_field(name='Birthday', value = row[3], inline=False)
            sendEmbed.add_field(name='WhatsApp Number', value = row[4], inline=False) 
            sendEmbed.add_field(name='Facebook Id', value = row[5], inline=False)
            sendEmbed.add_field(name='Instagram Id', value = row[6], inline=False)
            sendEmbed.add_field(name='Redmine API Key', value = new, inline=False)

            await ctx.send(embed = sendEmbed)
    
    cur.close()
    

# Update Profile Command
@bot.command()
async def update(ctx, username: discord.Member):

    await ctx.message.mentions[0].id

    conn = sqlite3.connect('main.sqlite')

    cur = conn.cursor()

    embed = discord.Embed(
            colour = 0x28da5b,
            title = 'User Profile',
            description = " All the information about the user profile like name, phone, mail and so on. "
            )
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.set_footer(text="Made with ❤️️  by Koders")
    embed.timestamp = datetime.datetime.utcnow()
    
    embed.add_field(name="Which user profile feature you want to update ?", value=f'''
     :one: {'Name'}

     :two: {'Phone Number'}

     :three: {'Mail Id'}

     :four: {'Birthday'} 

     :five: {'WhatsApp Number'}

     :six: {'Facebook Id'}

     :seven: {'Instagram Id'} 

     :eight: {'Redmine API Key'}''', inline = False)

    message = await ctx.send(embed=embed)

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")
    await message.add_reaction("6️⃣")
    await message.add_reaction("7️⃣")
    await message.add_reaction("8️⃣")

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "1️⃣":
            await ctx.send('Thanks for updating your Name!')
            suggestEmbed01 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Name.',
                description = " Write your updated name. "
                )
            suggestEmbed01.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed01.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed01.timestamp = datetime.datetime.utcnow()

            sent01 = await ctx.send(embed = suggestEmbed01)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent01.delete()
                    message01 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent01.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Name = ? WHERE Discord_Id = ?''', 
            (message01, username.id))

            conn.commit()

        if str(reaction.emoji) == "2️⃣":
            await ctx.send('Thanks for updating your Phone Number!')
            suggestEmbed02 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated phone number.',
                description = " Write your updated phone number. "
                )
            suggestEmbed02.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed02.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed02.timestamp = datetime.datetime.utcnow()

            sent02 = await ctx.send(embed = suggestEmbed02)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent02.delete()
                    message02 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent02.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Phone = ? WHERE Discord_Id = ?''', 
            (message02, username.id ))

            conn.commit()

        if str(reaction.emoji) == "3️⃣":
            await ctx.send('Thanks for updating your Mail Id!')
            suggestEmbed03 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Mail Id.',
                description = " Write your updated Mail Id. "
                )
            suggestEmbed03.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed03.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed03.timestamp = datetime.datetime.utcnow()

            sent03 = await ctx.send(embed = suggestEmbed03)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent03.delete()
                    message03 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent03.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Mail = ? WHERE Discord_Id = ?''', 
            (message03, username.id ))

            conn.commit()

        if str(reaction.emoji) == "4️⃣":
            await ctx.send('Thanks for updating your Birthday date!')
            suggestEmbed04 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated birthday date.',
                description = " Write your updated birthday date. "
                )
            suggestEmbed04.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed04.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed04.timestamp = datetime.datetime.utcnow()

            sent04 = await ctx.send(embed = suggestEmbed04)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent04.delete()
                    message04 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent04.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Birthday = ? WHERE Discord_Id = ?''', 
            (message04, username.id ))

            conn.commit()

        if str(reaction.emoji) == "5️⃣":
            await ctx.send('Thanks for updating your Name!')
            suggestEmbed05 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Name.',
                description = " Write your updated name. "
                )
            suggestEmbed05.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed05.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed05.timestamp = datetime.datetime.utcnow()

            sent05 = await ctx.send(embed = suggestEmbed05)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent05.delete()
                    message05 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent05.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET WhatsApp = ? WHERE Discord_Id = ?''', 
            (message05, username.id ))

            conn.commit()

        if str(reaction.emoji) == "6️⃣":
            await ctx.send('Thanks for updating your Name!')
            suggestEmbed06 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Name.',
                description = " Write your updated name. "
                )
            suggestEmbed06.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed06.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed06.timestamp = datetime.datetime.utcnow()

            sent06 = await ctx.send(embed = suggestEmbed06)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent06.delete()
                    message06 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent06.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Facebook = ? WHERE Discord_Id = ?''', 
            (message06, username.id ))

            conn.commit()

        if str(reaction.emoji) == "7️⃣":
            await ctx.send('Thanks for updating your Name!')
            suggestEmbed07 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Name.',
                description = " Write your updated name. "
                )
            suggestEmbed07.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed07.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed07.timestamp = datetime.datetime.utcnow()

            sent07 = await ctx.send(embed = suggestEmbed07)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent07.delete()
                    message07 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent07.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Instagram = ? WHERE Discord_Id = ?''', 
            (message07, username.id ))

            conn.commit()

        if str(reaction.emoji) == "8️⃣":
            await ctx.send('Thanks for updating your Name!')
            suggestEmbed08 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your updated Name.',
                description = " Write your updated name. "
                )
            suggestEmbed08.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed08.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed08.timestamp = datetime.datetime.utcnow()

            sent08 = await ctx.send(embed = suggestEmbed08)

            try:
                msg = await bot.wait_for(
                    "message",
                    timeout=300.0,
                    check=lambda message: message.author == ctx.author
                )

                if msg:
                    await sent08.delete()
                    message08 = msg.content
                    await msg.delete()

            except asyncio.TimeoutError:
                await sent08.delete()
                await ctx.send('Cancelling due to timeout.', delete_after = 300)
            
            cur.execute('''UPDATE main 
            SET Redmine = ? WHERE Discord_Id = ?''', 
            (message08, username.id ))

            conn.commit()
            
    except asyncio.TimeoutError:
        await ctx.send("Time out. Please try again!")

    cur.close()


@bot.event
async def on_ready():  # Triggers when bot is ready
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
        Name TEXT,
        Phone INTEGER,
        Mail TEXT,
        Birthday TEXT,
        WhatsApp INTEGER,
        Facebook TEXT,
        Instagram TEXT,
        Redmine TEXT
        )
    ''')
    cursor.execute("ALTER TABLE main ADD Discord_Id TEXT")
    cursor.execute("ALTER TABLE main ADD Roles TEXT")
    cursor.execute("ALTER TABLE main ADD Tools TEXT")
    cursor.execute("ALTER TABLE main ADD Skills TEXT")
    cursor.execute("ALTER TABLE main ADD Projects TEXT")
    cursor.execute("ALTER TABLE main ADD Portfolio TEXT")
    cursor.execute("ALTER TABLE main ADD Brand TEXT")
    cursor.execute("ALTER TABLE main ADD Bio TEXT")
    cursor.execute("ALTER TABLE main ADD Hobbies TEXT")
    cursor.execute("ALTER TABLE main ADD Blogs TEXT")
    cursor.execute("ALTER TABLE main ADD Books TEXT")
    cursor.execute("ALTER TABLE main ADD Language TEXT")
    cursor.execute("ALTER TABLE main ADD Ide TEXT")

    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))

@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    message_id = payload.message_id
    
    # Create Profile Channel Id
    channel = bot.get_channel("CREATE_CHANNEL_ID")
    sendEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile',
        description = " All the information about the user profile like name, phone, mail and so on. "
    )
    
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()

    if str(payload.emoji) == '👍':
        
        message = await channel.send(embed = sendEmbed)
       # await message.add_reaction('😋')
       # await message.add_reaction('😉')
       # await message.add_reaction('💪')
       # await message.add_reaction('🔥')

    if str(payload.emoji) in ('😋', '😉', '💪', '🔥'):

        await user(payload)

if __name__ == "__main__":
    try:
        bot.run("TOKEN")

    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
