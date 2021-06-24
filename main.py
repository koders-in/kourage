# Manual file imports
import asyncio
import datetime
import json
import csv
import os
from uuid import uuid4
import discord
import requests
from colorama import init
from discord.utils import get
from discord.ext import commands
from discord.ext.tasks import loop
from termcolor import colored
import sqlite3

# Logging format
import logging
import platform
import time

# Manual imports
import issues
import embeds

from sqlite3.dbapi2 import Cursor
db = sqlite3.connect('db/main.sqlite')
cursor = db.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS main(
    Name TEXT,
    RedmineAPI TEXT
    )
''')

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


logger = Logger("kourage-boilerplate")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.success("Kourage is running at version {0}".format("0.1.0"))

@bot.command()
async def status(ctx):
    # Show all issues
    key = os.environ.get("REDMINE_KEY")
    description = issues.show_issues(key)

    # STATUS ID INPUT
    description += """

    STATUS ID
    1 - New
    2 - In Progress
    3 - Resolved
    4 - Feedback
    5 - Closed
    6 - Rejected

    Enter status ID
    _E.g - 2_
    """
    embed = embeds.simple_embed("Choose status id", description)
    status_embed = await ctx.send(embed=embed)
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']
    for reaction in reactions:
        await status_embed.add_reaction(reaction)

    def check(reaction, user):
        return (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or str(reaction.emoji) == '5️⃣') and user.bot is not True and user == ctx.author

    async def take_reaction(ctx, timeout=300.0):
        status_id = None
        try:
            result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
            reaction, user = result
            if str(reaction)  == '1️⃣':
                status_id = 1
                return status_id
            elif str(reaction) == '2️⃣':
                status_id = 2
                return status_id
            elif str(reaction) == '3️⃣' :
                status_id = 3
                return status_id
            elif str(reaction) == '4️⃣':
                status_id = 4
                return status_id
            elif str(reaction) == '5️⃣':
                status_id = 5
                return status_id
            elif str(reaction) == '6️⃣':
                status_id = 6
                return status_id
            return status_id
        except asyncio.TimeoutError:
            await ctx.delete()

    status_id = await take_reaction(ctx)
    await status_embed.delete()
    print(status_id)

    if issues.change_status_id(key, issue_id, status_id):
        logger.info("Successfully changed status to " + status_id + " on " + issue_id)
        ctx.send("Successfully changed status to " + status_id + " on " + issue_id)
    else:
        logger.info("Something went wrong while making changes in the status id")
        ctx.send("Something went wrong while making changes in the status id")

@bot.command()
async def test(ctx):
    key = os.environ.get('REDMINE_KEY')
    description = issues.show_projects(key)
    description += "\n\n"
    description += "Enter project id" + "\n" + "_E.g - 28_"
    embed = embeds.simple_embed("Projects", description)
    project_all_embed = await ctx.send(embed=embed)

    # PROJECT ID INPUT
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await project_all_embed.delete()
            project_id = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await project_all_embed.delete()
        await project_input_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)


    # TRACKER ID INPUT
    description = """
    Tracker ID
    1 - Bug
    2 - Feature
    3 - Support
    4 - Task
    """
    embed = embeds.simple_embed("Choose tracker id", description)
    tracker_embed = await ctx.send(embed=embed)
    reactions =  ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    for reaction in reactions:
        await tracker_embed.add_reaction(reaction)

    def check(reaction, user):
        return (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣') and user.bot is not True and user == ctx.author

    async def take_reaction(ctx, timeout=300.0):
        tracker_id = None
        try:
            result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
            reaction, user = result
            print(reaction)
            if str(reaction)  == '1️⃣':
                tracker_id = 1
                return tracker_id
            elif str(reaction) == '2️⃣':
                tracker_id = 2
                return tracker_id
            elif str(reaction) == '3️⃣' :
                tracker_id = 3
                return tracker_id
            elif str(reaction) == '4️⃣':
                tracker_id = 4
                return tracker_id
            return tracker_id
        except asyncio.TimeoutError:
            await ctx.delete()

    tracker_id = await take_reaction(ctx)
    print(tracker_id)
    await tracker_embed.delete()

    # PRIORITY ID INPUT
    description = """
    Priority ID
    1 - Low
    2 - Normal
    3 - High
    4 - Urgent
    5 - Immediate

    Enter priority ID
    _E.g - 2_
    """
    embed = embeds.simple_embed("Choose priority id", description)
    priority_embed = await ctx.send(embed=embed)
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    for reaction in reactions:
        await priority_embed.add_reaction(reaction)

    def check(reaction, user):
        return (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or str(reaction.emoji) == '5️⃣') and user.bot is not True and user == ctx.author

    async def take_reaction(ctx, timeout=300.0):
        priority_id = None
        try:
            result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
            reaction, user = result
            print(reaction)
            if str(reaction)  == '1️⃣':
                priority_id = 1
                return priority_id
            elif str(reaction) == '2️⃣':
                priority_id = 2
                return priority_id
            elif str(reaction) == '3️⃣' :
                priority_id = 3
                return priority_id
            elif str(reaction) == '4️⃣':
                priority_id = 4
                return priority_id
            elif str(reaction) == '5️⃣':
                priority_id = 5
                return priority_id
            return priority_id
        except asyncio.TimeoutError:
            await ctx.delete()

    priority_id = await take_reaction(ctx)
    await priority_embed.delete()
    print(priority_id)

    # SUBJECT INPUT
    subject_embed = embeds.simple_embed("Enter subject", "e.g - Issue generator via discord")
    subject_embed = await ctx.send(embed=subject_embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await subject_embed.delete()
            subject = msg.content
        await msg.delete()

    except asyncio.TimeoutError:
        await subject_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # DESCRIPTION INPUT
    description_embed = embeds.simple_embed("Enter description", "e.g - Issue creation for redmine under discord")
    description_embed = await ctx.send(embed=description_embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await description_embed.delete()
            description = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await description_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # DUE DATE INPUT
    due_date_embed = embeds.simple_embed("Enter due date[YYYY-MM-DD]", "e.g - 2022-06-23")
    due_date_embed = await ctx.send(embed=due_date_embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await due_date_embed.delete()
            due_date = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await due_date_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # ESTIMATED HOURS INPUT
    estimated_hour_embed = embeds.simple_embed("Enter estimated hours", "e.g - 5")
    estimated_hour_embed = await ctx.send(embed=estimated_hour_embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await estimated_hour_embed.delete()
            estimated_hours = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await estimated_hour_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # MEMBER ALLOCATION
    description = issues.show_members(key, project_id)
    member_embed = embeds.simple_embed("Available members", description)
    member_embed = await ctx.send(embed=member_embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await member_embed.delete()
            assigned_to = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await member_embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    if issues.create_issue(key, project_id, tracker_id, priority_id, subject, description, due_date, estimated_hours, assigned_to):
        await ctx.send("Issue created successfully")
        await ctx.message.delete()
    else:
        await ctx.send("Something went wrong. Issue creation failed")
        await ctx.message.delete()

@bot.command()
async def log(ctx):
    await ctx.channel.purge(limit = 1)
    initial_embed = discord.Embed(colour=0x28da5b)
    initial_embed=discord.Embed(title="Work Logger Bot", description="", color=0x28da5b)
    initial_embed.add_field(name="Logging Work for", value = f"Logging work for {datetime.datetime.today().strftime('%d-%m-%y')}")
    initial_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    initial_embed.timestamp = datetime.datetime.utcnow()
    initial_embed.set_footer(text="Made with ❤️️  by Koders")
    initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    message  = await ctx.send(embed = initial_embed)

    # Temporary fix
    username_embed = discord.Embed(colour=0x28da5b)
    username_embed = discord.Embed(
        title = 'Please input your Username',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed = username_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            username = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    data = []
    for row in cursor.execute('''SELECT RedmineAPI FROM main WHERE Name = ?''', (username, )):
        row1 = row

    finalrow = row1[0]

    def check (reaction, user):
        return not user.bot and  message == reaction.message

    # acquiring data from the website
    headers = {'content-type': 'application/json',
        'X-Redmine-API-Key': f'{finalrow}'}
    r = requests.get('https://kore.koders.in/projects.json', headers=headers)

    json_data = r.json()
    projects = json_data['projects']

    # Project ID
    projectid_embed = discord.Embed(colour=0x28da5b)
    projectid_embed = discord.Embed(
        title = 'Please input the project ID of the issue',
        description = ' This request will timeout after a minute'
    )
    for i in range(0,len(projects)):
        projectid_embed.add_field(name = f"{projects[i]['id']}",value = f"{projects[i]['identifier']}" ,inline=False)
    sent = await ctx.send(embed = projectid_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            projectidmessage = msg.content
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # To get hold of the projectname
    for i in range(len(projects)):
        if(projects[i]['id'] == int(projectidmessage)):
            projectname = projects[i]['identifier']

    constanturl = 'https://kore.koders.in/projects/'
    newurl = constanturl + projectname

    # for getting issue id, hit a get request with new url
    newurl_issues = newurl + '/issues.json'

    headers = {'content-type': 'application/json',
        'X-Redmine-API-Key': f'{finalrow}'}

    r1 = requests.get(f'{newurl_issues}', headers=headers)
    json_data1 = r1.json()
    issues = json_data1['issues']

    print('ID','Subject','Assignee')
    for i in range(len(issues)):
        print(issues[i]['id'],issues[i]['subject'],issues[i]['assigned_to']['name'])

    # Task ID
    taskid_embed = discord.Embed(colour=0x28da5b)
    taskid_embed = discord.Embed(
        title = 'Please input the Issue ID of the issue',
        description = ' This request will timeout after a minute'
    )
    for i in range(len(issues)):
        taskid_embed.add_field(name=f"{issues[i]['id']}",value=f"{issues[i]['subject']}",inline=False)
        # taskid_embed.add_field(name=f"{issues[i]['assigned_to']['name']}",value= "",inline=True)

    sent = await ctx.send(embed = taskid_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            taskidmessage = msg.content
            issue_id = taskidmessage
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)


    # hours embed
    hours_embed = discord.Embed(colour=0x28da5b)
    hours_embed = discord.Embed(
        title = 'How many hours have you worked for today?',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed =   hours_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            hoursmessage = msg.content
            no_of_hours = hoursmessage
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # comment embed
    comment_embed = discord.Embed(colour=0x28da5b)
    comment_embed = discord.Embed(
        title = 'Any comments on your work today? ',
        description = ' This request will timeout after 5 minutes'
    )
    sent = await ctx.send(embed =   comment_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            commentmessage = msg.content
            comments = commentmessage
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300.0)



    # Activity ID  embed
    activity_id_embed = discord.Embed(colour=0x28da5b)
    activity_id_embed = discord.Embed(
        title = 'Please Enter the activity ID: (8 -> designing ,9 -> development, 10 -> Management, 11 -> Content Creation, 12 -> Marketing, 13 -> Planning) ',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed =   activity_id_embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=60.0,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await sent.delete()
            activity_id_message = msg.content
            activity_id = activity_id_message
            await msg.delete()

    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 60.0)

    # Finally, making a Post Request Now
    payload={'time_entry[hours]': f'{no_of_hours}',
            'time_entry[issue_id]': f'{issue_id}',
            'time_entry[comments]': f'{comments}',
            'time_entry[activity_id]': f'{activity_id}'}

    headers = {'X-Redmine-API-Key':f'{finalrow}'}
    r = requests.post('https://kore.koders.in/time_entries.xml', headers=headers,data=payload)

    print(r.text)
    print(r.status_code)


    #  Final embed with all of the messages included along with activities
    finalembed = discord.Embed(colour = 0x28da5b)
    finalembed = discord.Embed(title='You have successfully logged in your work for today! ')
    finalembed.add_field(name = 'Task ID', value  = f'{issue_id}',inline=False)
    finalembed.add_field(name = 'Hours worked', value  = f'{no_of_hours}')
    finalembed.add_field(name='Comments ', value = f'{comments}', inline=False)
    if(activity_id == '8'):
        finalembed.add_field(name='Activity Id: ', value = 'Designing', inline=False)
    elif(activity_id == '9'):
        finalembed.add_field(name='Activity Id: ', value = 'Development', inline=False)
    elif(activity_id == '10'):
        finalembed.add_field(name='Activity Id: ', value = 'Management', inline=False)
    elif(activity_id == '11'):
        finalembed.add_field(name='Activity Id: ', value = 'Content Creation', inline=False)
    elif(activity_id == '12'):
        finalembed.add_field(name='Activity Id: ', value = 'Marketing', inline=False)
    elif(activity_id == '13'):
        finalembed.add_field(name='Activity Id: ', value = 'Planning', inline=False)
    finalembed.set_author(name = f'{ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    finalembed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    finalembed.timestamp = datetime.datetime.utcnow()
    finalembed.set_footer(text="Made with ❤️️  by Koders")

    finalmessage = await ctx.send(embed=finalembed)

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
