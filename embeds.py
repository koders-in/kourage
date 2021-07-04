import asyncio
import json
import os
import logging
import platform
import time
import discord
from colorama import init
from termcolor import colored
import datetime
machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def success(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', color))

logger = Logger("kourage-suggestions")

def simple_embed(ctx, title, description):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=0x28da5b
            )
    embed.set_author(name = f'{ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    #embed.thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed

_rxn = {'1️⃣' : 1, '2️⃣' : 2, '3️⃣' : 3, '4️⃣' : 4, '5️⃣' : 5, '6️⃣' : 6}

async def take_reaction(ctx, rxn_amnt, _embed, bot, timeout=300.0):
    rxn = dict()
    _i = 1
    for i in _rxn:
        if _i > rxn_amnt:
            break
        rxn[i] = _i
        _i += 1

    for i in rxn:
        await _embed.add_reaction(i)

    def check(reaction, user):
        _c1 = user.bot is not True and user == ctx.author
        return _c1 and str(reaction.emoji) in rxn

    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
        reaction, user = result

        ret = (None, rxn[str(reaction)]) [ str(reaction) in rxn ]
        return ret, _embed

    except asyncio.TimeoutError:
        await ctx.delete()


async def ctx_input(ctx, bot, embed, timeout = 60.0):
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