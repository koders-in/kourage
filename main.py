# NOTE: Please specify the 'admin' channel ID at line #405 accordingly.

# Manual file imports
from datetime import date
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
import redmine_api

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

logger = embeds.Logger("kourage-work")

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~")

@bot.event
async def on_ready():  # Triggers when bot is ready
    logger.success("Kourage is running at version {0}".format("0.1.0"))

@bot.command()
async def status(ctx):
    # Show all issues
    if not 'REDMINE_KEY' in os.environ:
        logger.error("[ENV ERROR] 'REDMINE_KEY' doesn't exist in environment variable")
        return
    logger.info('~status called for ' + os.environ.get('REDMINE_KEY'))
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
    embed = embeds.simple_embed(ctx, "Choose status id", description)
    status_embed = await ctx.send(embed = embed)
    status_id, status_embed = await embeds.take_reaction(ctx, 6, _embed = status_embed, bot = bot)
    await status_embed.delete()
    logger.info("Change status Id requested : "+ str(status_id))

# FIXME: Module issues has no attribute 'change_status_id'
    if issues.change_status_id(key, issue_id, status_id):
        logger.info("Successfully changed status to " + status_id + " on " + issue_id)
        await ctx.send("Successfully changed status to " + status_id + " on " + issue_id)
    else:
        logger.info("Something went wrong while making changes in the status id")
        await ctx.send("Something went wrong while making changes in the status id")

@bot.command()
async def test(ctx):
    if not 'REDMINE_KEY' in os.environ:
        logger.error("[ENV ERROR] 'REDMINE_KEY' doesn't exist in environment variable")
        return
    logger.info("~test called for " + os.environ.get('REDMINE_KEY'))

    key = os.environ.get('REDMINE_KEY')
    description = issues.show_projects(key)
    description += "\n\n"
    description += "Enter project id" + "\n" + "_E.g - 28_"
    embed = embeds.simple_embed(ctx, "Projects", description)
    project_all_embed = await ctx.send(embed=embed)

    project_id = await embeds.ctx_input(ctx, bot, project_all_embed)
    if not project_id:
        logger.error("Project ID not defined.")
        return
    # TRACKER ID INPUT
    description = """
    Tracker ID
    1 - Bug
    2 - Feature
    3 - Support
    4 - Task
    """
    embed = embeds.simple_embed(ctx, "Choose tracker id", description)
    tracker_embed = await ctx.send(embed=embed)

    tracker_id, tracker_embed = await embeds.take_reaction(ctx, 4, tracker_embed, bot)

    logger.info("Tracker ID : " + str(tracker_id))
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
    embed = embeds.simple_embed(ctx, "Choose priority id", description)
    priority_embed = await ctx.send(embed=embed)

    priority_id, priority_embed = await embeds.take_reaction(ctx, 5, priority_embed, bot)

    await priority_embed.delete()
    logger.info("Priority ID : " + str(priority_id))

    # SUBJECT INPUT
    subject_embed = embeds.simple_embed(ctx, "Enter subject", "e.g - Issue generator via discord")
    subject_embed = await ctx.send(embed=subject_embed)
    subject = await embeds.ctx_input(ctx, bot, subject_embed)
    if not subject:
        logger.error("Subject timed out.")
        return
    logger.info("Subject : " + subject)
    # DESCRIPTION INPUT
    description_embed = embeds.simple_embed(ctx, "Enter description", "e.g - Issue creation for redmine under discord")
    description_embed = await ctx.send(embed=description_embed)

    description = await embeds.ctx_input(ctx, bot, description_embed)
    if not description:
        logger.error("Description timed out.")
        return
    logger.info("Description : " + description)
    # DUE DATE INPUT
    due_date_embed = embeds.simple_embed(ctx, "Enter due date[YYYY-MM-DD]", "e.g - 2022-06-23")
    due_date_embed = await ctx.send(embed=due_date_embed)

    due_date = await embeds.ctx_input(ctx, bot, due_date_embed)
    if not due_date:
        logger.error("Due date timed out.")
        return
    logger.info("Due date : " + due_date)

    # ESTIMATED HOURS INPUT
    estimated_hour_embed = embeds.simple_embed(ctx, "Enter estimated hours", "e.g - 5")
    estimated_hour_embed = await ctx.send(embed=estimated_hour_embed)

    estimated_hours = await embeds.ctx_input(ctx, bot, estimated_hour_embed)
    if not estimated_hours:
        logger.error("Estimated hours timed out.")
        return
    logger.info("Estimated hours : " + estimated_hours)

    # MEMBER ALLOCATION
    # FIXME: JSONDecodeError("Expecting value", s, err.value) <- None
    description = issues.show_members(key, project_id)
    member_embed = embeds.simple_embed(ctx, "Available members", description)
    member_embed = await ctx.send(embed=member_embed)

    assigned_to = await embeds.ctx_input(ctx, bot, member_embed)
    if not assigned_to:
        logger.error("'Assigned to' input timed out.")
        return
    logger.info("Assigned to " + assigned_to)

    if issues.create_issue(key, project_id, tracker_id, priority_id, subject, description, due_date, estimated_hours, assigned_to):
        await ctx.send("Issue created successfully")
        logger.success("Issue created successfully")
        await ctx.message.delete()
    else:
        await ctx.send("Something went wrong. Issue creation failed")
        logger.error("Something went wrong. Issue creation failed")
        await ctx.message.delete()

@bot.command()
async def log(ctx):
    if not 'REDMINE_KEY' in os.environ:
        logger.error("[ENV ERROR] 'REDMINE_KEY' doesn't exist in environment variable")
        return
    logger.info("~log called for " + os.environ.get('REDMINE_KEY'))

    await ctx.channel.purge(limit = 1)
    initial_embed = embeds.simple_embed(ctx, "Work Logger Bot", "")
    initial_embed.add_field(name="Logging Work for", value = f"Logging work for {datetime.datetime.today().strftime('%d-%m-%y')}")
    initial_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    initial_embed.set_author(name = f'Bot initialized for  {ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    message  = await ctx.send(embed = initial_embed)

    # Temporary fix
    username_embed = embeds.simple_embed(
            ctx,
            'Please input your username',
            'This request will timeout after a minute'
        )
    sent = await ctx.send(embed = username_embed)
    username = await embeds.ctx_input(ctx, bot, sent)
    if not username:
        logger.error("Username timed out")
        return
    logger.info("Username : " + username)

    data = []
    for row in cursor.execute('''SELECT RedmineAPI FROM main WHERE Name = ?''', (username, )):
        row1 = row

    finalrow = row1[0]

    def check (reaction, user):
        return not user.bot and  message == reaction.message

    # acquiring data from the website
    headers = {'content-type': 'application/json',
        'X-Redmine-API-Key': f'{finalrow}'}

    json_data = redmine_api.get_json('https://kore.koders.in/projects.json', headers)
    projects = json_data['projects']

    # Project ID

    projectid_embed = embeds.simple_embed(ctx,
        title = 'Please input the project ID of the issue',
        description = ' This request will timeout after a minute'
    )

    for i in range(0,len(projects)):
        projectid_embed.add_field(name = f"{projects[i]['id']}",value = f"{projects[i]['identifier']}" ,inline=False)
    sent = await ctx.send(embed = projectid_embed)
    projectidmessage = await embeds.ctx_input(ctx, bot, sent)
    if not projectidmessage:
        logger.error("Project ID timed out.")
        return
    logger.info("Project ID : " + projectidmessage)
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

    #r1 = requests.get(f'{newurl_issues}', headers=headers)
    #json_data1 = r1.json()
    json_data1 = redmine_api.get_json(f'{newurl_issues}', headers)
    issues = json_data1['issues']

    logger.info('ID Subject Assignee')
    for i in range(len(issues)):
        logger.info(issues[i]['id'] + " " + issues[i]['subject'] + " " + issues[i]['assigned_to']['name'])

    # Task ID

    taskid_embed = embeds.simple_embed(
        ctx,
        title = 'Please input the Issue ID of the issue',
        description = ' This request will timeout after a minute'
    )
    for i in range(len(issues)):
        taskid_embed.add_field(name=f"{issues[i]['id']}",value=f"{issues[i]['subject']}",inline=False)
        # taskid_embed.add_field(name=f"{issues[i]['assigned_to']['name']}",value= "",inline=True)

    sent = await ctx.send(embed = taskid_embed)
    taskidmessage = await embeds.ctx_input(ctx, bot, sent)
    issue_id = taskidmessage
    if not taskidmessage:
        logger.error("Issue ID timed out.")
        return
    logger.info("Issue ID : " + issue_id)
    # hours embed
    hours_embed = embeds.simple_embed(
        ctx,
        title = 'How many hours have you worked for today?',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed =   hours_embed)
    hoursmessage = await embeds.ctx_input(ctx, bot, sent)
    no_of_hours = hoursmessage
    if not hoursmessage:
        logger.error("No. of hours timed out.")
        return
    logger.info("Hours worked : " + no_of_hours)
    # comment embed
    comment_embed = embeds.simple_embed(
        ctx,
        title = 'Any comments on your work today? ',
        description = ' This request will timeout after 5 minutes'
    )
    sent = await ctx.send(embed =   comment_embed)
    commentmessage = await embeds.ctx_input(ctx, bot, sent)
    comments = commentmessage
    if not commentmessage:
        logger.error("Comments timed out.")
        return
    logger.info("Comments : " + comments)

    # Activity ID  embed
    activity_id_embed = embeds.simple_embed(
        ctx,
        title = 'Please Enter the activity ID: (8 -> designing ,9 -> development, 10 -> Management, 11 -> Content Creation, 12 -> Marketing, 13 -> Planning) ',
        description = ' This request will timeout after a minute'
    )
    sent = await ctx.send(embed =   activity_id_embed)
    activity_id_message = await embeds.ctx_input(ctx, bot, sent)
    activity_id = activity_id_message
    if not activity_id_message:
        logger.error("Activity ID timed out.")
        return
    logger.info("Activity ID : " + activity_id)

    # Finally, making a Post Request Now
    payload={'time_entry[hours]': f'{no_of_hours}',
            'time_entry[issue_id]': f'{issue_id}',
            'time_entry[comments]': f'{comments}',
            'time_entry[activity_id]': f'{activity_id}'}

    headers = {'X-Redmine-API-Key':f'{finalrow}'}
    r = redmine_api.post_data('https://kore.koders.in/time_entries.xml', headers, payload)

    logger.info(r.text)
    logger.info(r.status_code)


    #  Final embed with all of the messages included along with activities
    finalembed = embeds.simple_embed(
            ctx = ctx,
            title = 'You have successfully logged in your work for today! ',
            description = "")

    finalembed.add_field(name = 'Task ID', value  = f'{issue_id}',inline=False)
    finalembed.add_field(name = 'Hours worked', value  = f'{no_of_hours}')
    finalembed.add_field(name='Comments ', value = f'{comments}', inline=False)
    _value_dict = {8 : 'Designing', 9 : 'Development', 10 : 'Management',
            11 : 'Content Creation', 12 : 'Marketing', 13 : 'Planning'}

    finalembed.add_field(name = 'Activity Id: ', value = _value_dict[activity_id], inline = False)
    finalembed.set_author(name = f'{ctx.message.author}', icon_url = f'{ctx.author.avatar_url}')
    finalembed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")

    finalmessage = await ctx.send(embed=finalembed)
hdr = {'X-Redmine-API-Key': '59b61c8a459de5a742f94648d0a88f820594f2de'}
@bot.command()
async def no_issue(ctx):
    channel = bot.get_channel(859374150514376734)
    url = "http://checkos.m.redmine.org/users.json"
    ujson = redmine_api.get_json(url, hdr)
    for i in ujson['users']:
        if functions.No_Issue_Assigned_Reminder(hdr, i['id']):
            user_embed = embeds.simple_embed(ctx, 'No issue assigned reminder', i['firstname'] + ' ' + i['lastname'] + ' is idle.')
            sent = await(channel.send(embed = user_embed))


@bot.command()
async def spent_hours(ctx):
    desc3=functions.Spent_hours(hdr)
    issue_embed=discord.Embed(title="Your Current issues are", description=desc3, color=0x11806a)
    await ctx.send(embed=issue_embed,delete_after=60)
    due_embed=discord.Embed(title="", description="Of which issue ID do you want to see spent hours:",color=0x11806a)
    message=await ctx.send(embed=due_embed,delete_after=60)
    issue_id = await embeds.ctx_input(ctx, bot, message)
    if not issue_id:
        return
    issue_data=functions.Spent_hours_Data(issue_id, hdr)
    due_embed=embeds.simple_embed(ctx, title="Your log for issue#"+issue_id+" are", description=issue_data)
    await ctx.send(ctx, embed=due_embed,delete_after=90)

@bot.command()
async def due_date(ctx):
    url = "https://www.kore.koders.in/projects.json"
    projects = redmine_api.get_json(url, hdr)
    project_idlist = {}
    project_list=""
    j=0
    channel = bot.get_channel(859374150514376734)
    for i in projects["projects"]:
        j=j+1
        project_list=project_list+str(j)+") "+(i["name"]+"\n")
        project_idlist[j]=i["id"]
    initial_embed=embeds.simple_embed(ctx, title="Current Projects",description="Please select a project number to see due date:\n"+project_list)
    message  = await ctx.send(embed = initial_embed,delete_after=60)
    project_no = await embeds.ctx_input(ctx, bot, message)
    if not project_no:
        return
    id=int(project_no)
    ctime = datetime.datetime.now()
    project_id=str(project_idlist[id])
    issue_url = "https://www.kore.koders.in/projects/"+project_id+"/issues.json?set_filter=1"
    issues = redmine_api.get_json(issue_url, hdr)
    #print(issues)
    list =""
    channel_list=""
    for i in issues["issues"]:

        due=i["due_date"]
        duedate_msg=str(i["due_date"])
        if not due:
            due="Null"
        else:
            due += " 23:59:59"
            due = datetime.datetime.strptime(due, '%Y-%m-%d %H:%M:%S')
            delta = due - ctime

            if( delta.days <0  ):
                if "assigned_to" not in i:
                    list=list+("Issue #"+str(i["id"])+" ( 𝗘𝗫𝗣𝗜𝗥𝗘𝗗 ) "+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: NULL"+"\nSubject: "+str(i["subject"])+"\nDue Date was: "+str(due)+"\n\n")
                else:
                    list=list+("Issue #"+str(i["id"])+" ( 𝗘𝗫𝗣𝗜𝗥𝗘𝗗 ) "+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: "+str(i["assigned_to"]["name"])+"\nSubject: "+str(i["subject"])+"\nDue Date was: "+str(due)+"\n\n")
            else:
                if "assigned_to" not in i:
                    list=list+("Issue #"+str(i["id"])+" ( Expires in "+str(delta.days)+" days )"+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: NULL"+"\nSubject: "+str(i["subject"])+"\nDue Date is: "+str(due)+"\n\n")
                elif(duedate_msg==str(date.today())):
                    list=list+("Issue #"+str(i["id"])+" ( Expires in "+str(delta.days)+" days )"+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: "+str(i["assigned_to"]["name"])+"\nSubject: "+str(i["subject"])+"\nDue Date is: "+str(due)+"\n\n")
                    due_embed=embeds.simple_embed(ctx, title="Due Date Reminder!",description="Issue #"+str(i["id"])+" ( Expires in "+str(delta.days)+" days )"+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: "+str(i["assigned_to"]["name"])+"\nSubject: "+str(i["subject"])+"\nDue Date is: "+str(due)+"\n\n")
                    await channel.send(embed=due_embed)



    issue_embed=embeds.simple_embed(ctx, title="Issues List:",description=list)
    message  = await ctx.send(embed = issue_embed,delete_after=60)

if __name__ == "__main__":
    try:
        bot.run(os.environ.get("TOKEN"))
    except Exception as _e:
        logging.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
