import discord
import platform
import logging
import asyncio
import time
from colorama import init
from discord import channel
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands
import attendance_info as attendance_info
import datetime
import matplotlib.pyplot as plt
import requests
from discord.utils import get
import json
from discord.ext.tasks import loop

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
import config as CONFIG  # Capitals for global
import embeds as EMBEDS

attendance_marked_by=[]  #global variable

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

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))


@bot.event
async def on_member_join(member):  # Triggers when members joins the server
    #await member.send('Thank you for joining Koders') # Have an embed there
    role = get(member.guild.roles, id=726643908624515195)
    await member.add_roles(role)
    


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
        attendance_marked_by.append(user)
        channel = await user.create_dm()
        date_time = datetime.datetime.now()
        embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
        await channel.send(embed=embed)
        end = time.time()
        timeout = timeout - (end - start)
        logger.warning(user)
        
        print(attendance_marked_by)
        r='''
        # Write into Gsheet Username Time Date
        GSHEET.insert(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), user)
        logger.warning(user)'''
        await take_reaction(ctx, timeout=timeout)


@bot.command()
@commands.has_any_role("@everyone")
async def marked(msg):
    dateandtime=str(datetime.date.today())
    names_present=[]
    total_names=[]
    names_absent=[]
    save_filename=f'./graphs/present_or_absent/present_or_absent_{dateandtime}.jpg'
    all_members = msg.guild.get_role(852801843527417896).members
    await msg.channel.send(all_members)
    for each_member in all_members:
        total_names.append(each_member)

    for name in attendance_marked_by:
        names_present.append(name)
    for each in total_names:
        if each in names_present:
            print(f'{each} is present')
        else:
            names_absent.append(each)
    present_people=len(names_present)
    absent_people=len(names_absent)

    for each in names_absent:
        print(dir(each))


    
    mylabels=[f'Present {present_people}',f'Absent {absent_people}']
    y=[present_people,absent_people]
    plt.title('Present Vs Absent')
    plt.pie(y, labels = mylabels,  startangle = 0)
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename)
    plt.close()
    await msg.send(file=discord.File(save_filename))

@bot.command()
@commands.has_any_role("@everyone")   
async def take_attendance_morning(ctx):
    embed = EMBEDS.attendance("11:00", "14:00")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    print('hi')
    await take_reaction(msg)


async def take_attendance_lunch(ctx):
    embed = EMBEDS.attendance("3:00", "3:20")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    await take_reaction(msg)


@loop(minutes=1)
async def attendance_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(852444225828159488)  # attendance channel id
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




@bot.command()
@commands.has_any_role("@everyone")
async def attendance(msg):
    await msg.send(attendance_info.func_list)
@bot.command()
@commands.has_any_role("@everyone")
async def my_attendance(msg):
    name=str(msg.author)
    name=name.lower()
    counter=attendance_info.search_by_name(name)
    await msg.send(f'Name-> {name} Shifts Present-> {counter} total Shifts-> {len(attendance_info.dates)*2}')
@bot.command()
@commands.has_any_role("@everyone")
async def overall_attendance_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    counter=attendance_info.search_by_name(name)
    await msg.send(f'Name-> {name} Shifts Present-> {counter} total Shifts-> {len(attendance_info.dates)*2}')
@bot.command()
@commands.has_any_role("@everyone")
async def total_attendance(msg):
    attendance=attendance_info.overall_attendance()
    await msg.send(attendance)  
@bot.command()
@commands.has_any_role("@everyone")
async def weekly_attendance(msg):
    save_filename=attendance_info.weekly_bar()
    await msg.send(file=discord.File(save_filename))
@bot.command()
@commands.has_any_role("@everyone")
async def monthly_attendance(msg):
    save_filename=attendance_info.monthly_bar()
    await msg.send(file=discord.File(save_filename))
@bot.command()
@commands.has_any_role("@everyone")
async def pie_graph_of(msg):
    name=str(msg.message.content)
    name=name.split()[1]
    save_filename=attendance_info.visualize_pie_graph_search_by_name(name)
    await msg.channel.send(file=discord.File(save_filename))
@bot.command()
@commands.has_any_role("@everyone")
async def compare_bar(msg):
    names=str(msg.message.content)
    names=names.split()[1]
    names=names.split(',')
    save_filename=attendance_info.compare_bar(names)
    await msg.channel.send(file=discord.File(save_filename))
@bot.command()
@commands.has_any_role("@everyone")
async def compare_pie(msg):
    names=str(msg.message.content)
    names=names.split()[1]
    names=names.split(',')
    save_filename=attendance_info.pie_compare(names)
    await msg.channel.send(file=discord.File(save_filename))
@bot.command()
@commands.has_any_role("@everyone")
async def dates_absent_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_absent=attendance_info.days_absent(name)
    await msg.send(f'Name-> {name}    dates absent=>{dates_absent}')
@bot.command()
@commands.has_any_role("@everyone")
async def dates_present_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_present=attendance_info.days_present(name)
    await msg.send(f'Name-> {name}    dates present=>{dates_present}')
@bot.command()
@commands.has_any_role("@everyone")
async def weekly_dates_absent_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_absent=attendance_info.week_dates_absent(name)
    await msg.send(f'Name-> {name}    dates absent=>{dates_absent}')
@bot.command()
@commands.has_any_role("@everyone")
async def weekly_dates_present_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_present=attendance_info.week_dates_present(name)
    await msg.send(f'Name-> {name}    dates absent=>{dates_present}')
@bot.command()
@commands.has_any_role("@everyone")
async def monthly_dates_absent_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_absent=attendance_info.month_dates_absent(name)
    await msg.send(f'Name-> {name}    dates absent=>{dates_absent}')
@bot.command()
@commands.has_any_role("@everyone")
async def monthly_dates_present_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    dates_present=attendance_info.month_dates_present(name)
    await msg.send(f'Name-> {name}    dates present=>{dates_present}')
@bot.command()
@commands.has_any_role("@everyone")
async def custom_dates_absent_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    no_of_days=int(msg.message.content.split(' ')[2])
    dates_absent=attendance_info.custom_dates_absent(name,no_of_days)
    await msg.send(f'Name-> {name}    dates absent=>{dates_absent}') 
@bot.command()
@commands.has_any_role("@everyone")
async def custom_dates_present_of(msg):
    name=msg.message.content.split(' ')[1]
    name=name.lower()
    no_of_days=int(msg.message.content.split(' ')[2])
    dates_absent=attendance_info.custom_dates_present(name,no_of_days)
    await msg.send(f'Name-> {name}    dates absent=>{dates_absent}') 
@bot.command()
@commands.has_any_role("@everyone")
async def custom_days_bar(msg):
    no_of_days=int(msg.message.content.split(' ')[1])
    save_filename=attendance_info.custom_bar(no_of_days)
    await msg.channel.send(file=discord.File(save_filename))


if __name__ == "__main__":
    try:
        attendance_info.initialize()
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
