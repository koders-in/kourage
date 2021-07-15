import json
import embeds
import os
import datetime
import discord
import requests
ifport redmine_api
from discord.ext import commands
from discord.ext.tasks import loop
import discord
from discord import client
from discord.ext import commands
import function
from urllib import parse, request
import re
import asyncio
from discord.ext import commands
import time
import glob
from discord.utils import get




logger = embeds.Logger("kourage-operations")

bot = commands.Bot(command_prefix="~")

## Change the webpage accordingly.
webpage = "http://checkos.m.redmine.org/"

hdr1 = {'X-Redmine-API-Key' : os.environ.get('REDMINE_KEY'),
        'Content-Type': 'application/json'}

@bot.event
async def on_ready():
    logger.success("Kourage is running at version {0}".format("0.1.0"))



@bot.command()
async def show_issues(ctx):
    await ctx.channel.purge(limit = 1)
    initial_embed = discord.Embed(colour=0x11806a)
    desc=function.project_list()
    initial_embed=discord.Embed(title="This is the current list of project", description=desc, color=0x11806a)
    initial_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    initial_embed.timestamp = datetime.datetime.utcnow()
    initial_embed.set_footer(text="Made with ❤️️  by Koders")
    initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    message  = await ctx.send(embed = initial_embed,delete_after=90)

   
    due_embed=embeds.simple_embed(title="Enter the name of the project?", description="please write in this format only eg. Kourage-Bot")
    message=await ctx.send(embed=due_embed,delete_after=60)
    project_name = await embeds.ctx_input(ctx, bot, message)
    if not project_name:
      return 
     
    response=function.issues(project_name)
    due_embed=discord.Embed(title="List of issues", description=response, color=0x11806a)
    await ctx.send(embed=due_embed,delete_after=60)

# Channel creation
@bot.command()
async def channel(ctx, name):
   
    await ctx.guild.create_text_channel(name=name)

@bot.command()
async def new_project(ctx):
    await ctx.channel.purge(limit = 1)
    initial_embed = discord.Embed(colour=0x11806a)
    initial_embed=discord.Embed(title="New project bot", description="", color=0x11806a)
    initial_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    initial_embed.timestamp = datetime.datetime.utcnow()
    initial_embed.set_footer(text="Made with ❤️️  by Koders")
    initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    message  = await ctx.send(embed = initial_embed,delete_after=60)

   
    due_embed=embeds.simple_embed(title="", description="Enter the name of the project")
    message=await ctx.send(embed=due_embed,delete_after=60)
    name = await embeds.ctx_input(ctx, bot, message)
    if not name:
      return 
    due_embed=embeds.simple_embed(title="", description="Enter the identifier for the project")
    message=await ctx.send(embed=due_embed,delete_after=60)
    identifier = await embeds.ctx_input(ctx, bot, message)
    if not identifier:
      return 
    response=function.new_project(name,identifier)
    await ctx.guild.create_text_channel(name=name)
    due_embed=discord.Embed(title="", description=response, color=0x11806a)
    await ctx.send(embed=due_embed,delete_after=60)
        
 


# FIXME: Project ID should be given for now.
@bot.command()
async def add_person(ctx, project_id):
    if not 'REDMINE_KEY' in os.environ:
        logger.error("'REDMINE_KEY' doesn't exist in the environment variables")
        return
    logger.info("~add_person called for " + os.environ.get('REDMINE_KEY'))
    udict = dict()
    ujson_data = redmine_api.get_json(webpage + 'users.json', hdr1)
    desc = ""
    for i in ujson_data['users']:
        udict[i['id']] = i['firstname'] + " " + i['lastname']
        desc += str(i['id']) + " " + str(udict[i['id']]) + "\n"

    ujson_embed = embeds.simple_embed(ctx,
            title = "Enter user ID",
            description = desc
            )

    sent = await ctx.send(embed = ujson_embed)
    ulist = await embeds.ctx_input(ctx, bot, sent)
    if not ulist:
        logger.error("User List input timed out.")
        return
    logger.info("Ulist : " + ulist)

    ulist = list(map(int, ulist.split()))
    # TODO: Let the user of bot know too what's wrong with the input
    for i in ulist:
        if not i in udict:
            logger.error("ID " + str(i) + " not in user dict.")
            return

    rset = set()
    rjson_data = redmine_api.get_json(webpage + 'roles.json', hdr1)
    desc = ""
    for i in rjson_data['roles']:
        rset.add(i['id'])
        desc += str(i['id']) + " " + i['name'] + '\n'
    rjson_embed = embeds.simple_embed(ctx,
            title = 'Select the role',
            description = desc
            )

    sent = await ctx.send(embed = rjson_embed)
    rlist = await embeds.ctx_input(ctx, bot, sent)
    if not rlist:
        logger.error("Role input timed out.")
        return
    logger.info("Rlist : " + rlist)

    rlist = list(map(int, rlist.split()))
    for i in rlist:
        if not i in rset:
            logger.error("Role " + str(i) + "not in role set.")
            return
    print(ulist)
    for uid in ulist:
        payload = json.dumps({
            "membership": {
                "user_id": uid,
                "role_ids": rlist
            }
        })
        print("Payload", payload)
        preq = redmine_api.post_data(webpage + "projects/" + project_id + "/memberships.json", hdr1, payload)
        print("send req : ", preq)

@bot.command()
async def remove_user(ctx, project_id):
    if not 'REDMINE_KEY' in os.environ:
        logger.error("'REDMINE_KEY' doesn't exist in the environment variables")
        return
    logger.info("~remove_person called for " + os.environ.get('REDMINE_KEY'))

    #Show all the member working on the project
    desc = ""
    udict = dict()
    mjson = redmine_api.get_json(webpage + "projects/" + project_id + "/memberships.json", hdr1)
    for i in mjson['memberships']:
        udict[i['user']['id']] = i['id']
        desc += str(i['user']['id']) + " " + i['user']['name'] + "\n"

    mjson_embed = embeds.simple_embed(ctx,
            title = 'Select the ID(space seperated)',
            description = desc
            )

    sent = await ctx.send(embed = mjson_embed)
    mlist = await embeds.ctx_input(ctx, bot, sent)
    if not mlist:
        logger.error("Member input timed out.")
        return
    logger.info("Mlist : " + mlist)

    mlist = set(map(int, mlist.split()))
    for i in mlist:
        if not i in udict:
            logger.error("Member " + str(i) + "not in member set.")
            return
        else:
            ecode = requests.delete(webpage + "memberships/" + str(udict[i]) + ".json", headers = hdr1)
            print(ecode)
            logger.success("Removed user ID: " + str(i) + "\n")
    return
@bot.command()
async def feedback(ctx):
    
    channel = bot.get_channel(os.environ.get('CHANNEL_ID')) 
    front_embed=discord.Embed(title="CLIENT FEEDBACK BOT", description="As a software company we at Koders, value our clients feedback and want to have a continuous developing service and growth.We would really appreciate if you could spare a few minutes and fill in the details of this form so as to help us in improving or Quality and service.Your input would be highly confidential and valuable. \n\n For any queries please feel free to contact us :\nMail - support@koders.in\nPhone Number - 7008493497,7017799756",colour=0x11806a)
    front_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    front_embed.set_image(url ="https://cdn.discordapp.com/attachments/860047404903956480/860926678784278528/Black_and_Blue_Business_Linkedln_Banner_11.png")
    front_embed.set_footer(text="Thank you for choosing Koders ❤️️")
    front_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    front_embed.timestamp = datetime.datetime.utcnow()
    front=await ctx.send(embed=front_embed)
    
    project_name_embed=discord.Embed(title="",description="What was your Project/Channel Name ?",colour=0x11806a)
    project=await ctx.send(embed=project_name_embed,delete_after=60)
    project_name = await embeds.ctx_input(ctx, bot, project)
    if not project_name:
         return 
    hear_us= {1:"News/Banners", 2:"Social media handles", 3:"Recommendation",4:"others"} 
    hear_embed=discord.Embed(title="How did you hear about us?",description="1) News/Banners\n2) Social media handles\n3) Recommendation\n4) Others",colour=0x11806a)
    hear_0=await ctx.send(embed=hear_embed)
    var,hear_embed=await embeds.take_reaction_no(ctx,4,hear_0,bot)
    if(var==4): 
        other_embed=discord.Embed(title="",description="What is the other source?",colour=0x11806a)
        other_source=await ctx.send(embed=other_embed,delete_after=60)
        hear_us = await embeds.ctx_input(ctx, bot, other_source)
        if not hear_us:
         return
    else: 
        hear_us=hear_us[var]
    await hear_0.delete()
    experience_embed=discord.Embed(title="",description="How was your experience with Koders? Has any aspect of our company exceeded your expectations?",colour=0x11806a)
    exp=await ctx.send(embed=experience_embed,delete_after=60)
    experience = await embeds.ctx_input(ctx, bot, exp)
    if not experience:
         return
     
    ratings={1:"😍 Excellent",2:"🙂 Satisfactory",3:"😑 Average",4:"😕 Bad",5:"😡 Worst"}
    rate_embed=discord.Embed(title="Rate us",description="😍 Excellent\n\n🙂 Satisfactory\n\n😑 Average\n\n😕 Bad\n\n😡 Worst",colour=0x11806a)
    rate_card=await ctx.send(embed=rate_embed,delete_after=60)
    
    communication_embed=discord.Embed(title="",description="Communication ?",colour=0x11806a)
    communication=await ctx.send(embed=communication_embed)
    var,communication_embed=await embeds.take_reaction(ctx,5,communication,bot)
    communication_rating=ratings[var]
    await communication.delete()
    
    responsiveness_embed=discord.Embed(title="",description="Responsiveness ?",colour=0x11806a)
    responsiveness=await ctx.send(embed=responsiveness_embed)
    var,responsiveness_embed=await embeds.take_reaction(ctx,5,responsiveness,bot)
    responsiveness_rating=ratings[var]
    await responsiveness.delete()
    
    costs_embed=discord.Embed(title="",description="Costs ?",colour=0x11806a)
    costs=await ctx.send(embed=costs_embed)
    var,costs_embed=await embeds.take_reaction(ctx,5,costs,bot)
    costs_rating=ratings[var]
    await costs.delete()
    
    overall_embed=discord.Embed(title="",description="Overall knowledge and understanding of the project ?",colour=0x11806a)
    overall=await ctx.send(embed=overall_embed)
    var,overall_embed=await embeds.take_reaction(ctx,5,overall,bot)
    overall_rating=ratings[var]
    await overall.delete()
    await rate_card.delete() 
    
    next_embed=discord.Embed(title="If we could make something for you the next time, what would you like?",description="",colour=0x11806a)
    next_embed.set_footer(text="If you wanna skip this press ❌, if you wanna answer press ✅")
    next=await ctx.send(embed=next_embed)
    var,next_embed=await embeds.take_reaction_NA(ctx,2,next,bot)
    if(var==1): 
         next_time="NA"
         await next.delete()
    elif(var==2):
      optional_embed=discord.Embed(title="",description="Type your response",colour=0x11806a)
      optional=await ctx.send(embed=optional_embed)
      next_time = await embeds.ctx_input(ctx, bot,optional)
      await next.delete()
      if not next_time:
         return
    
    additional_embed=discord.Embed(title="Any additional feedback ",description="Based on your experience, please give brief suggestions(if any) on how the experience could have been better for both of us. It may be related to the tools and services we used, the timeline, cost, how we communicated throughout the project, etc. This would mean a lot to us and will try to incorporate the suggestions made by you.",colour=0x11806a)
    additional_embed.set_footer(text="If you wanna skip this press ❌, if you wanna answer press ✅")
    additional=await ctx.send(embed=additional_embed,delete_after=60)
    var,additional_embed=await embeds.take_reaction_NA(ctx,2,additional,bot)
    if(var==1): 
         additional_feedback="NA"
         await additional.delete()
    elif(var==2):
     optional_embed=discord.Embed(title="",description="Type your response",colour=0x11806a)
     optional=await ctx.send(embed=optional_embed)
     additional_feedback = await embeds.ctx_input(ctx, bot,optional)
     await additional.delete()
     if not additional_feedback:
         return
    
    thankyou_embed=embeds.simple_embed(title="Thank You for the valuable feedback",description="We value your time and efforts!")
    await ctx.send(embed=thankyou_embed,delete_after=60)
    await front.delete()
    
    sendEmbed=embeds.simple_embed(title="\nFEEDBACK REPORT",description="")
    sendEmbed.set_author(name = f'Feedback from : {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    sendEmbed.add_field(name='Project Name: ', value = str(project_name)+"\n\n\n", inline=False) 
    sendEmbed.add_field(name='How did you hear about us?', value = str(hear_us)+"\n\n", inline=False) 
    sendEmbed.add_field(name='How was your experience with Koders? Has any aspect of our company exceeded your expectations?', value = str(experience)+"\n\n\n", inline=False)
    sendEmbed.add_field(name='Rate us:', value ="Communication :  "+communication_rating+"\n\n Responsiveness :  "+responsiveness_rating+"\n\nCosts :  "+costs_rating+"\n\n Overall knowledge and understanding of the project :  "+overall_rating+"\n\n\n", inline=False)
    sendEmbed.add_field(name='If we could make something for you the next time, what would you like?', value = str(next_time)+"\n\n\n", inline=False)
    sendEmbed.add_field(name='Any additional feedback: ', value = str(additional_feedback)+"\n\n\n", inline=False)
        
    await channel.send(embed=sendEmbed)

async def _archive(ctx, singleChannel):
    id = (ctx.guild.id, ctx.channel.id) [singleChannel]

    fptr = open(r'stream/dce_stdin', 'w+')
    data = ('guild: ', 'channel: ') [singleChannel] + str(id) + '\n' + 'token: ' + os.environ.get('DISCORD_KEY')
    print(data)
    fptr.writelines(data)
    fptr.close()
    while not os.path.exists('stream/o_stdin'):
        time.sleep(1)

    os.remove('stream/o_stdin')

    files = glob.glob('stream/files/*')
    for file in files:
        await ctx.send(file = discord.File(file))
        #os.remove(file)

    fptr = open(r'stream/dce_stdin', 'w+')
    fptr.write('done')
    fptr.close()

client = discord.Client()
@bot.command()
async def archive_guild(ctx):
    await _archive(ctx, False)

@bot.command()
async def archive_channel(ctx):
    await _archive(ctx, True)
    await _archive(ctx, True)

if __name__ == "__main__":
    try:
        bot.run(os.environ.get('TOKEN'))
    except Exception as _e:
        logger.error("Exception found at main worker.\n" + str(_e))
