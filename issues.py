import requests
import json
import os

# tracker_id - Task, Bug, Feature, Support
# priority_id
# status_id should be 0
# subject
# description
# assigned_to_id
# estimated hours

def show_projects(key): # Redmine api key
    url = "https://kore.koders.in/projects.json"
    payload={}
    headers = {
      'X-Redmine-API-Key': key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    for project in data['projects']:
        print(str(project['id']) + " - " + project['name'])

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
    print(response)

def show_members(key, project_id):
    url = "https://kore.koders.in/projects/" + str(project_id) + "/memberships.json"
    payload={}
    headers = {
      'X-Redmine-API-Key': key,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    for member in data['memberships']:
        print(str(member['user']['id']) + " - " + member['user']['name'])

key = os.environ.get('REDMINE_KEY')
show_projects(key)
project_id = input("Enter project id:")
print("""
Tracker ID:
1 - Bug
2 - Feature
3 - Support
4 - Task
""")
tracker_id = input("Enter tracker id:")
print("""
Priority ID
1 - Low
2 - Normal
3 - High
4 - Urgent
5 - Immediate
""")
priority_id = input("Enter priority id:")
subject = input("Enter subject:")
description = input("Enter description:")
due_date = input("Enter due date[YYYY-MM-DD]:")
estimated_hours = input("Enter estimated hours:")
show_members(key, project_id)
assigned_to = input("Enter assigned to:")
create_issue(key, project_id, tracker_id, priority_id, subject, description, due_date, estimated_hours, assigned_to)
