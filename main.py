import discord
import platform
import logging
import time
import datetime
import asyncio
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
@bot.command()
async def user(ctx):
    suggestEmbed1 = discord.Embed(colour=0x28da5b)
    suggestEmbed1 = discord.Embed(
        title = 'Please tell me your Name',
        description = "  Write your full name . "
    )
    suggestEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed1.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed1.timestamp = datetime.datetime.utcnow()
    
    sent1 = await ctx.send(embed = suggestEmbed1)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=120.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent1.delete()
            message1 = msg.content
            await msg.delete()    

    except asyncio.TimeoutError:
        await sent1.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 120)

    cursor = sqlite3.connect('main.sqlite')
        
    suggestEmbed2 = discord.Embed(colour=0x28da5b)
    suggestEmbed2 = discord.Embed(
        title = 'Please tell me your Phone Number',
        description = """ Write you phone number. """
        )
    suggestEmbed2.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed2.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed2.timestamp = datetime.datetime.utcnow()
    
    sent2 = await ctx.send(embed = suggestEmbed2)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent2.delete()
            message2 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent2.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
    
    suggestEmbed3 = discord.Embed(colour=0x28da5b)
    suggestEmbed3 = discord.Embed(
        title = 'Please tell me your Mail Id',
        description = """ Write your email id. """
    )
    suggestEmbed3.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed3.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed3.timestamp = datetime.datetime.utcnow()

    sent3 = await ctx.send(embed = suggestEmbed3)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent3.delete()
            message3 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent3.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        
    suggestEmbed4 = discord.Embed(colour=0x28da5b)
    suggestEmbed4 = discord.Embed(
        title = 'Please tell me your Birthday',
        description = " Write your birthday date in dd/mm/yyyy in this format. "
    )
    suggestEmbed4.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed4.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed4.timestamp = datetime.datetime.utcnow()
    
    sent4 = await ctx.send(embed = suggestEmbed4)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent4.delete()
            message4 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent4.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        
    suggestEmbed5 = discord.Embed(colour=0x28da5b)
    suggestEmbed5 = discord.Embed(
        title = 'Please tell me your WhatsApp Number',
        description = " Write your WhatsApp phone number. "
    )
    suggestEmbed5.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    
    suggestEmbed5.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed5.timestamp = datetime.datetime.utcnow()
    
    sent5 = await ctx.send(embed = suggestEmbed5)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent5.delete()
            message5 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent5.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300) 

    suggestEmbed6 = discord.Embed(colour=0x28da5b)
    suggestEmbed6 = discord.Embed(
        title = 'Please tell me your Facebook Id',
        description = " Write your Facebook Id username. "
    )
    suggestEmbed6.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed6.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed6.timestamp = datetime.datetime.utcnow()
    
    sent6 = await ctx.send(embed = suggestEmbed6)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent6.delete()
            message6 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent6.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)

    suggestEmbed7 = discord.Embed(colour=0x28da5b)
    suggestEmbed7 = discord.Embed(
        title = 'Please tell me your Instagram Id username',
        description = "  Write your Instagram Id username. "
    )
    suggestEmbed7.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed7.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed7.timestamp = datetime.datetime.utcnow()
    
    sent7 = await ctx.send(embed = suggestEmbed7)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent7.delete()
            message7 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent7.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)    

    suggestEmbed8 = discord.Embed(colour=0x28da5b)
    suggestEmbed8 = discord.Embed(
        title = 'Please tell me your Redmine API Key',
        description = "  Write your Redmine API Key. "
    )
    suggestEmbed8.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed8.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed8.timestamp = datetime.datetime.utcnow()
    
    sent8 = await ctx.send(embed = suggestEmbed8)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent8.delete()
            message8 = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent8.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        
    sendEmbed = discord.Embed(colour=0x28da5b)
    sendEmbed = discord.Embed(
        title = 'User Profile',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()
    
    sendEmbed.add_field(name='Name', value = f'{message1}', inline=False)   
    sendEmbed.add_field(name='Phone Number', value = f'{message2}', inline=False) 
    sendEmbed.add_field(name='Mail Id', value = f'{message3}', inline=False)
    sendEmbed.add_field(name='Birthday', value = f'{message4}', inline=False)
    sendEmbed.add_field(name = 'WhatsApp Number', value = f'{message5}', inline=False) 
    sendEmbed.add_field(name='Facebook Id', value = f'{message6}', inline=False)
    sendEmbed.add_field(name='Instagram Id', value = f'{message7}', inline=False)
    sendEmbed.add_field(name='Redmine API Key', value = f'{message8}', inline=False)

    cursor.execute('''INSERT INTO main
    (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8)) 

    cursor.commit()

    await ctx.send(embed = sendEmbed)


# User Profile Info Command
@bot.command()
async def profile(ctx, *, username):
     
    cursor = sqlite3.connect('main.sqlite')
    
    sendEmbed = discord.Embed(colour=0x28da5b)
    sendEmbed = discord.Embed(
        title = 'User Profile',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
        )
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()

    data = []
    for row in cursor.execute('''SELECT Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine FROM main WHERE Name = ?''', (username, )):
        data.append(row)
        print(data)
        sendEmbed.add_field(name='Name', value = row[0], inline=False)   
        sendEmbed.add_field(name='Phone Number', value = row[1], inline=False) 
        sendEmbed.add_field(name='Mail Id', value = row[2], inline=False)
        sendEmbed.add_field(name='Birthday', value = row[3], inline=False)
        sendEmbed.add_field(name='WhatsApp Number', value = row[4], inline=False) 
        sendEmbed.add_field(name='Facebook Id', value = row[5], inline=False)
        sendEmbed.add_field(name='Instagram Id', value = row[6], inline=False)
        sendEmbed.add_field(name='Redmine API Key', value = row[7], inline=False)

        if not data:
            print(data)
            sendEmbed1 = discord.Embed(colour=0x28da5b)
            sendEmbed1 = discord.Embed(
                title = 'User Profile Not Found',
                description = " This user profile doesn't exists in the database. "
             )
            sendEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            sendEmbed1.set_footer(text="Made with ❤️️  by Koders")
            sendEmbed1.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = sendEmbed1)
        
    cursor.close()
    await ctx.send(embed = sendEmbed)

# Update Profile Command
@bot.command()
async def update(ctx, Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine):

    conn = None
    try:
        conn = sqlite3.connect('main.sqlite')
        sendEmbed = discord.Embed(colour=0x28da5b)
        sendEmbed = discord.Embed(
            title = 'User Profile',
            description = " All the information about the user profile like name, phone, mail and so on. "
            )
        sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
        sendEmbed.set_footer(text="Made with ❤️️  by Koders")
        sendEmbed.timestamp = datetime.datetime.utcnow()

        cur = conn.cursor()

        cur.execute('''UPDATE main 
        SET Phone = ?, Mail = ?, Birthday = ?, WhatsApp = ?, Facebook = ?, Instagram = ?, Redmine = ? WHERE Name = ?''', 
        ( Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine , Name, ))
        rows = cur.fetchall()
        for row in rows:
            sendEmbed.add_field(name='Name', value = row[0] or None, inline=False)   
            sendEmbed.add_field(name='Phone Number', value = row[1] or None, inline=False) 
            sendEmbed.add_field(name='Mail Id', value = row[2] or None, inline=False)
            sendEmbed.add_field(name='Birthday', value = row[3] or None, inline=False)
            sendEmbed.add_field(name='WhatsApp Number', value = row[4] or None, inline=False) 
            sendEmbed.add_field(name='Facebook Id', value = row[5] or None, inline=False)
            sendEmbed.add_field(name='Instagram Id', value = row[6] or None, inline=False)
            sendEmbed.add_field(name='Redmine API Key', value = row[7] or None, inline=False)

        conn.commit()
        cur.close()

    except Exception as e:
        print(e)

    await ctx.send(embed = sendEmbed)


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
    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))

if __name__ == "__main__":
    try:
        bot.run("TOKEN")
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
