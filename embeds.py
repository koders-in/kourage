import asyncio
import json
import os
import time
import logging
import platform
import datetime
import discord
from colorama import init
from termcolor import colored

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
        
def simple_embed(title, description):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=0x11806a
            )
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.set_footer(text="Made with ❤️️  by Koders")
    embed.timestamp = datetime.datetime.utcnow()
    return embed

        
async def ctx_input(ctx, bot, embed, timeout):
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await embed.delete()
            _id = msg.content
            await msg.delete()
            return _id

    except asyncio.TimeoutError as err:
        await embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = timeout)
        return None
