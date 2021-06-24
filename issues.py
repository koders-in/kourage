import requests
import json
import os
import discord

# TODO
# Set things to discord

def show_projects(key): # Redmine api key
    url = "https://kore.koders.in/projects.json"
    payload={}
    headers = {
      'X-Redmine-API-Key': key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    res = ""
    for project in data['projects']:
        res += str(project['id']) + " - " + project['name']
        res += "\n"
    return res

def create_issue(key, project_id, tracker_id, priority_id, subject, description, due_date, estimated_hours, assigned_to):
    url = "https://kore.koders.in/issues.json"
    payload={'issue[project_id]': project_id,
    'issue[tracker_id]': tracker_id,
    'issue[priority_id]': priority_id,
    'issue[subject]': subject,
    'issue[description]': description,
    'issue[due_date]': due_date,
    'issue[assigned_to_id]': assigned_to,
    'issue[estimated_hours]': estimated_hours}
    headers = {
      'X-Redmine-API-Key': key,
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    try:
        if response.status_code == 200:
            return True
    except:
        print("Unable to get status code")
        return False

def show_members(key, project_id):
    url = "https://kore.koders.in/projects/" + str(project_id) + "/memberships.json"
    payload={}
    headers = {
      'X-Redmine-API-Key': key,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    result = ""
    for member in data['memberships']:
        result += str(member['user']['id']) + " - " + member['user']['name']
        result += "\n"
    return result

#key = os.environ.get('REDMINE_KEY')
#
## SHOW PROJECTS
#show_projects(key)
#
#project_id = input("Enter project id:")
## SHOW TRACKER ID
#print("""
#Tracker ID:
#1 - Bug
#2 - Feature
#3 - Support
#4 - Task
#""")
#tracker_id = input("Enter tracker id:")
## SHOW PRIORITY ID
#print("""
#Priority ID
#1 - Low
#2 - Normal
#3 - High
#4 - Urgent
#5 - Immediate
#""")
#priority_id = input("Enter priority id:")
## SHOW SUBJECT
#subject = input("Enter subject:")
## SHOW DESCRIPTION
#description = input("Enter description:")
## SHOW DUE DATE
#due_date = input("Enter due date[YYYY-MM-DD]:")
## SHOW ESTIMATED HOURS
#estimated_hours = input("Enter estimated hours:")
## SHOW MEMBERS
#show_members(key, project_id)
#assigned_to = input("Enter assigned to:")
#create_issue(key, project_id, tracker_id, priority_id, subject, description, due_date, estimated_hours, assigned_to)
