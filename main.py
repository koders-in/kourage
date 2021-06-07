# Manual file imports
import asyncio
import datetime
import json

# Logging format
import logging
import platform
import time

from discord.utils import get
import discord
import requests
from colorama import init
from discord.ext import commands
from discord.ext.tasks import loop
from termcolor import colored

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

import config as CONFIG  # Capitals for global
import embeds as EMBEDS  # Capitals for global
import gsheet as GSHEET  # Capital for global


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
        print(colored(f'{message}', "blue"))


logger = Logger("kourage")

# FOR TESTING
# bot = commands.Bot(command_prefix="!")

intents = discord.Intents.default()
intents.members = True

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))

@bot.event
async def on_member_join(member):  # Triggers when members joins the server
    #await member.send('Thank you for joining Koders') # Have an embed there
    role = get(member.guild.roles, id=726643908624515195)
    await member.add_roles(role)
    

# TODO
# Add Duckhunt system responsive
# Look for setting career at koders with something better at server setup
# Google doc requirement on Koders App
# Sprint showcase

# Attendance System
def check(reaction, user):
    return str(reaction.emoji) == '⬆️' and user.bot is not True


async def take_reaction(ctx, timeout=1200.0):
    start = time.time()
    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.delete()
    else:
        reaction, user = result
        channel = await user.create_dm()
        date_time = datetime.datetime.now()
        embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
        await channel.send(embed=embed)
        end = time.time()
        timeout = timeout - (end - start)
        logger.warning(user)

        # Write into Gsheet Username Time Date
        GSHEET.insert(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), user)
        logger.warning(user)
        await take_reaction(ctx, timeout=timeout)


async def take_attendance_morning(ctx):
    embed = EMBEDS.attendance("11:00", "11:20")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    await take_reaction(msg)


async def take_attendance_lunch(ctx):
    embed = EMBEDS.attendance("3:00", "3:20")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    await take_reaction(msg)


@loop(minutes=1)
async def attendance_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(839125549304643684)  # attendance channel id
    working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    date_time = datetime.datetime.now()
    for working_day in working_days:
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "11:00":
            logger.info("Ran morning attendance.")
            await take_attendance_morning(channel)
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "15:00":
            logger.info("Ran post lunch attendance.")
            await take_attendance_lunch(channel)
    logger.info("Waiting for tasks...")


# Ping command
@bot.command()
@commands.has_any_role("@everyone")
async def ping(msg):
    await msg.send('Pong! 🏓\n ' +
                   'Name: Kourage \n ' +
                   'Description: AIO bot of Koders \n ' +
                   'Version: {0} \n '.format(CONFIG.VERSION) +
                   'Username: {0} \n '.format(msg.author.name) +
                   'Latency: {0} sec '.format(round(bot.latency, 1)))


# Define command
@bot.command()
@commands.has_any_role("Koders")
async def define(msg, *args):
    response = None
    word = args[0]  # API REQUEST
    url = 'https://owlbot.info/api/v4/dictionary/' + str(word)
    headers = {"Authorization": CONFIG.OWL_TOKEN}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        logger.error("Something went wrong during requesting API. Reason: " + str(e))  # Request exception

    data = json.loads(response.text)  # JSON PARSE WITH EMBED
    try:
        for i in range(0, len(data['definitions'])):
            embed = discord.Embed(title="Word: " + str(word), color=0x57b28f)
            embed.set_author(name="Kourage Word Analyzer",
                             url="https://www.github.com/koders-in/kourage",
                             icon_url=bot.user.avatar_url)
            if data['definitions'][i]['image_url'] is not None:
                embed.set_thumbnail(url=data['definitions'][i]['image_url'])
            embed.add_field(name="Type",
                            value=data['definitions'][i]['type'],
                            inline=True)
            embed.add_field(name="Meaning",
                            value="**" + data['definitions'][i]['definition'] + "**",
                            inline=False)
            if data['definitions'][i]['example'] is None:
                data['definitions'][i]['example'] = "N/A"
            embed.add_field(name="Example",
                            value="_" + data['definitions'][i]['example'] + "_",
                            inline=False)
            embed.set_footer(text="Made with ❤️️  by Koders")
            await msg.send(embed=embed)
    except Exception as e:
        Logger.error("Something went wrong during parsing JSON. Reason: " + str(e))  # JSON parsing exception
        await msg.send("Can't find its meaning over the database")  # Sending message so user can read

# Bug Feature 
@bot.command()
async def bug(ctx):
    suggestEmbed1 = discord.Embed(colour=0x28da5b)
    suggestEmbed1 = discord.Embed(
        title = 'Please tell me the ID/Name of the Bug',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    suggestEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed1.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed1.timestamp = datetime.utcnow()
    
    sent = await ctx.send(embed = suggestEmbed1)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=120.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            message1 = msg.content
            await msg.delete()    

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 120)
        
    suggestEmbed2 = discord.Embed(colour=0x28da5b)
    suggestEmbed2 = discord.Embed(
        title = 'Please tell me the description/summary of the Bug',
        description = """ If you feel the name is not sufficient, explain the bug in a few words. Share it in easy-to-understand language. Keep in mind that your description might be used to search in your bug tracking application, so make sure to use the right words.
        Environment: Depending on your browser, operating system, zoom level and screen size, websites may behave differently from one environment to another. Make sure your developers know your technical environment. """
        )
    suggestEmbed2.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed2.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed2.timestamp = datetime.utcnow()
    
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
        title = 'Please tell me the console logs of the Bug',
        description = """ By collecting the console logs your developers will find it a lot easier to reproduce and resolve any bug.
        Source URL: Make it easy for your developers spot the problem by including the URL of the page where you found the bug. Big time saver!
        Visual proof: A picture is worth a thousand words. Although it might not be enough, a visual element like a screenshot or a video will help your developers understand the problem better and faster. """
    )
    suggestEmbed3.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed3.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed3.timestamp = datetime.utcnow()
    
    file = discord.File("result.txt")
    sent3 = await ctx.send(embed = suggestEmbed3, file=file)

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

    message3 = msg.attachments[0].url
        
        
    suggestEmbed4 = discord.Embed(colour=0x28da5b)
    suggestEmbed4 = discord.Embed(
        title = 'Please tell me the expected vs. actual results of the Bug',
        description = " Explain what results you expected - be as specific as possible. Just saying 'the app doesn’t work as expected' is not useful. It's also helpful to describe what you actually experienced. "
    )
    suggestEmbed4.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed4.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed4.timestamp = datetime.utcnow()
    
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
        title = ' Steps to reproduce ',
        description = " A screenshot is a proof that you had a problem, but keep in mind that your developer might not be able to reproduce the bug. Make sure to describe, with as much detail as possible, the steps you took before you encountered the bug. "
    )
    suggestEmbed5.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    
    suggestEmbed5.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed5.timestamp = datetime.utcnow()
    
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

        
    sendEmbed = discord.Embed(colour=0x28da5b)
    sendEmbed = discord.Embed(
        title = 'Bug Report',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.utcnow()
    
    sendEmbed.add_field(name='ID/Name: ', value = f'{message1}', inline=False)   
    sendEmbed.add_field(name='Description/Summary', value = f'{message2}', inline=False) 
    sendEmbed.add_field(name='Console log of the Bug ', value = f'{message3}', inline=False)
    sendEmbed.add_field(name='Expected vs actual results', value = f'{message4}', inline=False)
    sendEmbed.set_image(url =  f'{message5}') 


    await ctx.send(embed = sendEmbed)


# Vision command
@bot.command()
@commands.has_any_role("Kore")
async def vision(msg):
    await msg.message.delete()
    embed = EMBEDS.vision()
    await msg.send(embed=embed)


# Remind command
@bot.command()
@commands.has_any_role("Koders")
async def remind(msg, *args):
    await msg.message.delete()
    await asyncio.sleep(float(args[0]) * 60 * 60)
    embed = discord.Embed(title="Hello there! You have a reminder ^_^",
                          color=0x57b28f)
    embed.add_field(name="Don't forget to:",
                    value="{0}".format(args[1]),
                    inline=False)
    embed.add_field(name="By yours truly :ghost:",
                    value="Kourage",
                    inline=False)
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2919/2919780.svg")
    embed.set_footer(text="Made with ❤️️  by Koders")
    await msg.send(embed=embed)
    if len(args) > 2:
        msg = await msg.send(args[2])
        await msg.delete()  # Deletes @person message who got tagged


# Poll command
@bot.command()
@commands.has_any_role('Koders')
async def poll(msg, question, *options: str):
    await msg.message.delete()
    embed = discord.Embed(title="Hello there! Please vote. ^_^",
                          description=question,
                          color=0x54ab8a)
    embed.set_author(name="Koders")
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    for _x, option in enumerate(options):
        embed.add_field(name=reactions[_x],
                        value=option,
                        inline=True)
    embed.set_footer(text="Made with ❤️️  by Koders")
    react_message = await msg.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)


if __name__ == "__main__":
    try:
        attendance_task.start()
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
