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

def show_issues(key): # Redmine api key
    url = "https://kore.koders.in/issues.json"
    payload={}
    headers = {
      'X-Redmine-API-Key': key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    result = ""
    for issue in data['issues']:
        result += str(issue['id']) + " - " + issue['subject']+ " - "  + issue['project']['name']
        result += "\n"
    return result

def change_issue_status(key, issue_id, status_id):
    url = "https://kore.koders.in/issues/" + str(issue_id) + ".json"
    payload={'issue[status_id]': status_id }
    headers = {
      'X-Redmine-API-Key': key,
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    try:
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        print("Something went wrong")
        return False

print(show_issues(os.environ.get("REDMINE_KEY")))
