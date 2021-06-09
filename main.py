import discord
import platform
import logging
import time
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

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.warning("Kourage is running at version {0}".format(CONFIG.VERSION))

@bot.command()
@commands.has_any_role("@everyone")
async def ff(msg):
    """
    This module fast forwards the messages from one channel to another
    Usage: prefix + `ff` + number_of_message =< 10 + channel_name
    Return: None
    """
    last_n_messages=int(msg.message.content.split(' ')[1])+1
    max_messages=100
    if last_n_messages-1 > max_messages:
        await msg.channel.send(f"maximum masseges limit to be forwarded is {max_messages} you have entered {last_n_messages-1}")
        return

    message_details=await msg.channel.history(limit=int(last_n_messages)).flatten() 
    channel_name=msg.message.content.split(' ')[2]
    channel_name=channel_name[2:(len(channel_name)-1)]
    channel=bot.get_channel(int(channel_name))
    print(message_details[1].id)
    if channel is not None:
        loop_itterator=1
        message_to_be_sent_id=[]
        message_to_be_forwarded=[]
        
           
        while loop_itterator<last_n_messages:
            if message_details[loop_itterator].attachments:
                image=message_details[loop_itterator].attachments[0]
                await channel.send(image)
            message_to_be_sent_id.append((message_details[loop_itterator]).id)
            loop_itterator=loop_itterator+1   
        for each_id in message_to_be_sent_id:
                message_to_be_forwarded.append((await msg.fetch_message(each_id)).content)
        message_to_be_forwarded.reverse()
        for each in message_to_be_forwarded:
            await channel.send(each)
    else:
        await msg.channel.send('Channel name not found')

if __name__ == "__main__":
    try:
        bot.run(CONFIG.TOKEN)
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
