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
    
    suggestEmbed2 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Phone Number',
        description = """ Write your phone number. """
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

    suggestEmbed3 = discord.Embed(
        colour = 0x28da5b,
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
        
    suggestEmbed4 = discord.Embed(
        colour = 0x28da5b,
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
        
    suggestEmbed5 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your WhatsApp Number ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed5.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    
    suggestEmbed5.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed5.timestamp = datetime.datetime.utcnow()

    message = await ctx.send(embed = suggestEmbed5)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
            await ctx.send('Thanks for letting us know your whatsapp number!')
            suggestEmbed9 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your WhatsApp Number.',
                description = " Write you phone number. "
                )
            suggestEmbed9.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed9.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed9.timestamp = datetime.datetime.utcnow()

            sent5 = await ctx.send(embed = suggestEmbed9)

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
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message5 = None
               
    except asyncio.TimeoutError:
        await ctx.send("Time out. Please try again!")
      
    suggestEmbed6 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your Facebook Id ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed6.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed6.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed6.timestamp = datetime.datetime.utcnow()
    
    message = await ctx.send(embed = suggestEmbed6)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
            await ctx.send('Thanks for letting us know your Facebook Id!')
            suggestEmbed10 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your Facebook Id.',
                description = " Write you Facebook Id. "
                )
            suggestEmbed10.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed10.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed10.timestamp = datetime.datetime.utcnow()

            sent6 = await ctx.send(embed = suggestEmbed10)

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
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message6 = None
               
    except asyncio.TimeoutError:
        await ctx.send("Time out. Please try again!")

    suggestEmbed7 = discord.Embed(
        colour = 0x28da5b,
        title = 'Could you please tell me your Instagram Id username ?',
        description = " Select your response with green tick for yes and red cross if not willing to share. "
    )
    suggestEmbed7.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed7.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed7.timestamp = datetime.datetime.utcnow()
    
    message = await ctx.send(embed = suggestEmbed7)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    def check (reaction, user):
        return not user.bot and message == reaction.message

    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run        
        if str(reaction.emoji) == "✅":
            await ctx.send('Thanks for letting us know your Instagram Id!')
            suggestEmbed11 = discord.Embed(
                colour = 0x28da5b,
                title = 'Please tell me your Instagram Id.',
                description = " Write you Instagram Id. "
                )
            suggestEmbed11.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
            suggestEmbed11.set_footer(text="Made with ❤️️  by Koders")
            suggestEmbed11.timestamp = datetime.datetime.utcnow()

            sent7 = await ctx.send(embed = suggestEmbed11)

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
        
        if str(reaction.emoji) == "❌":
           # await ctx.send('No!')
            message7 = None
               
    except asyncio.TimeoutError:
        await ctx.send("Time out. Please try again!")

    suggestEmbed8 = discord.Embed(
        colour = 0x28da5b,
        title = 'Please tell me your Redmine API Key',
        description = " Write your Redmine API Key. "
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
            message9 = message8[:-3] + '***'
            message8 = base64.b64encode(message8.encode("ascii"))
           # print(message9)
            await msg.delete()

    except asyncio.TimeoutError:
        await sent8.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        
    sendEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile',
        description = " All the information about the user profile like name, phone, mail and so on. "
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
    sendEmbed.add_field(name='Redmine API Key', value = f'{message9}', inline=False)

    cursor.execute('''INSERT INTO main
    (Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (message1, message2, message3, message4, message5, message6, message7, message8)) 

    cursor.commit()
    #cursor.close()

    await ctx.send(embed = sendEmbed)


# User Profile Info Command
@bot.command()
async def profile(ctx, *, username):

    # username = await ctx.message.mentions[0].id
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
    cur.execute('''SELECT Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine FROM main WHERE Name = ?''', (username, ))

    rows =[]
    if rows is "":
        print(rows)
        await ctx.send(embed = sendEmbed1)

    rows = cur.fetchall()
        
    print(rows)
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
async def update(ctx, Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine):

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

    conn = sqlite3.connect('main.sqlite')
    sendEmbed = discord.Embed(
        colour=0x28da5b,
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

    conn.commit()

    cur.execute('''SELECT Name, Phone, Mail, Birthday, WhatsApp, Facebook, Instagram, Redmine FROM main WHERE Name = ?''', (Name, ))

    rows = cur.fetchall()

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
