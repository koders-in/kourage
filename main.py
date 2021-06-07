# Manual file imports
import asyncio
import datetime
import json

# Logging format
import logging
import platform
import time
from discord import channel, message
from discord.enums import MessageType

from discord.utils import get
import discord
import requests
from colorama import init
from discord.ext import commands
from discord.ext.tasks import loop
from termcolor import colored
from discord.ext.commands import bot

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

import config as CONFIG  # Capitals for global
import embeds as EMBEDS  # Capitals for global
import gsheet as GSHEET  # Capital for global
import attendance_info as attendance_info
import fastforward as ff_id

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

@bot.command()
@commands.has_any_role("@everyone")
async def ff(msg):
    #to get last message
    mos=[]
    last_n_messages=int(msg.message.content.split(' ')[1])+1
    if last_n_messages-1 > 5:
        await  msg.channel.send(f"maximum masseges limit to be forwarded is 5 you have entered {last_n_messages-1}")
        return

    message_details= await msg.channel.history(limit=int(last_n_messages)).flatten() 
    channel_name=msg.message.content.split(' ')[2]
    channel_id2=ff_id.get_channel_id(f'{channel_name}')
    channel=bot.get_channel(channel_id2)
    
   

    if (last_n_messages-1)==1:
        m_id=str(message_details[1]).split(' ')[1].split('=')[1]
        
        message_to_be_forwarded=await msg.fetch_message(m_id)
        mos.append(message_to_be_forwarded.content)
        await  channel.send(message_to_be_forwarded.content)
    
    if (last_n_messages-1)==2:
        m_id1=str(message_details[1]).split(' ')[1].split('=')[1]
        message_to_be_forwarded1=await msg.fetch_message(m_id1)
        mos.append(message_to_be_forwarded1.content)
        

        m_id2=str(message_details[2]).split(' ')[1].split('=')[1]
        message_to_be_forwarded2=await msg.fetch_message(m_id2)
        mos.append(message_to_be_forwarded2.content)

    if (last_n_messages-1)==3:
        m_id1=str(message_details[1]).split(' ')[1].split('=')[1]
        
        message_to_be_forwarded1=await msg.fetch_message(m_id1)
        mos.append(message_to_be_forwarded1.content)
        

        m_id2=str(message_details[2]).split(' ')[1].split('=')[1]
        message_to_be_forwarded2=await msg.fetch_message(m_id2)
        mos.append(message_to_be_forwarded2.content)

        m_id3=str(message_details[3]).split(' ')[1].split('=')[1]
        message_to_be_forwarded3=await msg.fetch_message(m_id3)
        mos.append(message_to_be_forwarded3.content)

    if (last_n_messages-1)==4:
        m_id1=str(message_details[1]).split(' ')[1].split('=')[1]
        
        message_to_be_forwarded1=await msg.fetch_message(m_id1)
        mos.append(message_to_be_forwarded1.content)
        

        m_id2=str(message_details[2]).split(' ')[1].split('=')[1]
        message_to_be_forwarded2=await msg.fetch_message(m_id2)
        mos.append(message_to_be_forwarded2.content)

        m_id3=str(message_details[3]).split(' ')[1].split('=')[1]
        message_to_be_forwarded3=await msg.fetch_message(m_id3)
        mos.append(message_to_be_forwarded3.content)

        m_id4=str(message_details[4]).split(' ')[1].split('=')[1]
        message_to_be_forwarded4=await msg.fetch_message(m_id4)
        mos.append(message_to_be_forwarded4.content)
    
    
    if (last_n_messages-1)==5:
        m_id1=str(message_details[1]).split(' ')[1].split('=')[1]
        
        message_to_be_forwarded1=await msg.fetch_message(m_id1)
        mos.append(message_to_be_forwarded1.content)
        

        m_id2=str(message_details[2]).split(' ')[1].split('=')[1]
        message_to_be_forwarded2=await msg.fetch_message(m_id2)
        mos.append(message_to_be_forwarded2.content)

        m_id3=str(message_details[3]).split(' ')[1].split('=')[1]
        message_to_be_forwarded3=await msg.fetch_message(m_id3)
        mos.append(message_to_be_forwarded3.content)

        m_id4=str(message_details[4]).split(' ')[1].split('=')[1]
        message_to_be_forwarded4=await msg.fetch_message(m_id4)
        mos.append(message_to_be_forwarded4.content)

        m_id5=str(message_details[5]).split(' ')[1].split('=')[1]
        message_to_be_forwarded5=await msg.fetch_message(m_id5)
        mos.append(message_to_be_forwarded5.content)



    
    mos.reverse()
    for each in mos:
        await  channel.send(each)





async def take_attendance_morning(ctx):
    embed = EMBEDS.attendance("11:00", "14:00")
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
        attendance_info.initialize()
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
