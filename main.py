import discord
import platform
import logging
import time
import datetime
import asyncio
import embeds
from colorama import init
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands
import os

machine = platform.node()
init()

bot = commands.Bot(command_prefix="~")

# Bug Command
@bot.command()
async def bug(ctx):
    initial_embed = embeds.simple_embed(
        title = 'Please tell me the ID/Name of the Bug',
        description = " Keep it brief and use correct terms. A best practice is to include the name of the feature where you found an issue. A good example could be 'CART - Unable to add new item to my cart'. "
    )
    
    initial_sent = await ctx.send(embed = initial_embed)
    id_name=await  embeds.ctx_input(ctx,bot,initial_sent,timeout = 90.0)
    if not id_name:
        embeds.logger.error("no bug id received")
    
    description_embed = embeds.simple_embed(
        title = 'Please tell me the description/summary of the Bug',
        description = """ If you feel the name is not sufficient, explain the bug in a few words. Share it in easy-to-understand language. Keep in mind that your description might be used to search in your bug tracking application, so make sure to use the right words.
        Environment: Depending on your browser, operating system, zoom level and screen size, websites may behave differently from one environment to another. Make sure your developers know your technical environment. """
        )
    
    description_sent = await ctx.send(embed = description_embed)
    description=await  embeds.ctx_input(ctx,bot,description_sent,timeout = 90.0)
    if not description:
        embeds.logger.error("no bug description received")
        return
    
    console_log_embed = embeds.simple_embed(
        title = 'Please tell me the console logs of the Bug',
        description = """ By collecting the console logs your developers will find it a lot easier to reproduce and resolve any bug.
        Source URL: Make it easy for your developers spot the problem by including the URL of the page where you found the bug. Big time saver!
        Visual proof: A picture is worth a thousand words. Although it might not be enough, a visual element like a screenshot or a video will help your developers understand the problem better and faster. """
    )
   
    console_log_embed_sent = await ctx.send(embed = console_log_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await console_log_embed_sent.delete()
            console_log = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await console_log_embed_sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 100)

    console_log = msg.attachments[0].url
    
    result_embed = embeds.simple_embed(
        title = 'Please tell me the expected vs. actual results of the Bug',
        description = " Explain what results you expected - be as specific as possible. Just saying 'the app doesn’t work as expected' is not useful. It's also helpful to describe what you actually experienced. "
    )
   
    result_sent = await ctx.send(embed = result_embed)
    result=await embeds.ctx_input(ctx,bot,result_sent,timeout=90)
    if not result:
        embeds.logger.error("no expected vs. actual results received")
        return
    
    ss_embed = embeds.simple_embed(
        title = ' Steps to reproduce ',
        description = " A screenshot is a proof that you had a problem, but keep in mind that your developer might not be able to reproduce the bug. Make sure to describe, with as much detail as possible, the steps you took before you encountered the bug. "
    )
    
    ss_sent = await ctx.send(embed = ss_embed)
    ss=await embeds.ctx_input(ctx,bot,ss_sent,timeout=90)
    if not ss:
        embeds.logger.error("no ss received")
        return
    
    report_Embed = embeds.simple_embed(
        title = '',
        description = ""
    )
    report_Embed.set_author(name = f'Bug Report from : {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    report_Embed.add_field(name='ID/Name: ', value = f'{id_name}', inline=False)   
    report_Embed.add_field(name='Description/Summary', value = f'{description}', inline=False) 
    report_Embed.add_field(name='Console log of the Bug ', value = f'{console_log}', inline=False)
    report_Embed.add_field(name='Expected vs actual results', value = f'{result}', inline=False)
    report_Embed.set_image(url =  f'{ss}')               

    # ADMIN CHANNEL ID
    channel = bot.get_channel(os.environ.get("ADMIN_CHANNEL_ID"))  
    

    message = await channel.send(embed =report_Embed )
    await message.add_reaction('✅')
    await message.add_reaction('❌')

    from uuid import uuid4
    #event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    #unique_id = event_id[48:].upper()

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
                report_Embed.add_field(name='Suggestion Approved by: ', value = f'{user}'+"\n\n We thank you for your valuable time!", inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = report_Embed)
                
                await channel.send('Suggestion has been approved!')
                return
            if str(reaction.emoji) == "❌":
                await ctx.send('Sorry your Suggestion has not been approved')
                report_Embed.add_field(name='Suggestion Dissapproved by: ', value = f'{user}'+"\n\n We thank you for your valuable time!", inline=False) 
                await ctx.send("Your Suggestion was: ")
                message1 = await ctx.send(embed = report_Embed)
                    
                await channel.send('Suggestion has not been approved!')
                return
    except asyncio.TimeoutError:
        await ctx.send("Your suggestion was timed out. Please try again!")
        return
    
@bot.event
async def on_ready():  # Triggers when bot is ready
    embeds.logger.warning("Kourage is running at version {0}".format("0.1.0"))

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
        
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
