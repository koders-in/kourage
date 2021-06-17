import os
import discord
import platform
import logging
import time
from colorama import init
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands
import attendance_info as attendance_info

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

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
    logger.warning("Kourage is running at version {0}".format("0.1.0"))


 # Ping command
@bot.command()
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
        bot.run(os.environ.get("TOKEN"))
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
