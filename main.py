import discord
import os
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

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
