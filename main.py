import discord
import platform
import logging
import time
import datetime
import asyncio
from colorama import init
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands
import os

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

# Bug Command
@bot.command()
async def bug(ctx):
    suggestEmbed1 = discord.Embed(colour=0x28da5b)
    suggestEmbed1 = discord.Embed(
        title = 'Please tell me the ID/Name of the Bug',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    suggestEmbed1.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    suggestEmbed1.set_footer(text="Made with ❤️️  by Koders")
    suggestEmbed1.timestamp = datetime.datetime.utcnow()
    
    sent1 = await ctx.send(embed = suggestEmbed1)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent1.delete()
            message1 = msg.content
            await msg.delete()    

    except asyncio.TimeoutError:
        await sent1.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        
    suggestEmbed2 = discord.Embed(colour=0x28da5b)
    suggestEmbed2 = discord.Embed(
        title = 'Please tell me the description/summary of the Bug',
        description = """ If you feel the name is not sufficient, explain the bug in a few words. Share it in easy-to-understand language. Keep in mind that your description might be used to search in your bug tracking application, so make sure to use the right words.
        Environment: Depending on your browser, operating system, zoom level and screen size, websites may behave differently from one environment to another. Make sure your developers know your technical environment. """
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
        title = 'Please tell me the console logs of the Bug',
        description = """ By collecting the console logs your developers will find it a lot easier to reproduce and resolve any bug.
        Source URL: Make it easy for your developers spot the problem by including the URL of the page where you found the bug. Big time saver!
        Visual proof: A picture is worth a thousand words. Although it might not be enough, a visual element like a screenshot or a video will help your developers understand the problem better and faster. """
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

    message3 = msg.attachments[0].url
        

    suggestEmbed4 = discord.Embed(colour=0x28da5b)
    suggestEmbed4 = discord.Embed(
        title = 'Please tell me the expected vs. actual results of the Bug',
        description = " Explain what results you expected - be as specific as possible. Just saying 'the app doesn’t work as expected' is not useful. It's also helpful to describe what you actually experienced. "
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
        title = ' Steps to reproduce ',
        description = " A screenshot is a proof that you had a problem, but keep in mind that your developer might not be able to reproduce the bug. Make sure to describe, with as much detail as possible, the steps you took before you encountered the bug. "
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

        
    sendEmbed = discord.Embed(colour=0x28da5b)
    sendEmbed = discord.Embed(
        title = 'Bug Report',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    sendEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    sendEmbed.set_footer(text="Made with ❤️️  by Koders")
    sendEmbed.timestamp = datetime.datetime.utcnow()
    
    sendEmbed.add_field(name='ID/Name: ', value = f'{message1}', inline=False)   
    sendEmbed.add_field(name='Description/Summary', value = f'{message2}', inline=False) 
    sendEmbed.add_field(name='Console log of the Bug ', value = f'{message3}', inline=False)
    sendEmbed.add_field(name='Expected vs actual results', value = f'{message4}', inline=False)
    sendEmbed.set_image(url =  f'{message5}')               

    # ADMIN CHANNEL ID
    channel = bot.get_channel(os.environ.get("ADMIN_CHANNEL_ID"))  

    message = await channel.send(embed = sendEmbed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    from uuid import uuid4

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()


    def check (reaction, user):
        return not user.bot and message == reaction.message
    
    try:
        reaction, user = await bot.wait_for('reaction_add',check=check,timeout=604800) # this reaction is checking for adding an emoji, this line is automatically getting run because of like 31,32
        # Role logic
        role_string = ''
        for role in user.roles:
            if(role.name == '@everyone'):
                continue
            else:
                role_string += role.name
                role_string += ','
        role_string = role_string[:-1]
        
        while reaction.message == message:
            if str(reaction.emoji) == "✅":                
                await ctx.send('Suggestion has been approved!')
                #sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                
                await channel.send('Suggestion has been approved!')
                return
            if str(reaction.emoji) == "❌":
                await ctx.send('Suggestion has not been approved. We thank you for your valuable time!')
                #sendEmbed.add_field(name='Approved by:  ', value = f'{user}', inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = sendEmbed)
                    
                await channel.send('Suggestion has not been approved!')
                return
    except asyncio.TimeoutError:
        await ctx.send("Your suggestion was timed out. Please try again!")
        return


@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.warning("Kourage is running at version {0}".format(os.environ.get("VERSION")))

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
