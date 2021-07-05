import requests
import json
import datetime
import os

get_json = lambda _url, _hdr : requests.get(_url, headers = _hdr)

# Will give the data of the given API Key only. for now we are hard-coding it.
# but, a DB can be used


hdr1 ={'X-Redmine-API-Key':os.environ.get('REDMINE_KEY') }

def new_project(name,identifier):
   url = "http://koders.m.redmine.org/projects.json"

   
   payload = json.dumps({
   "project": {
    "name": name,
    "identifier": identifier,
    "enabled_module_names": "issue_tracking"
    }
    })
  
   headers = {
  'X-Redmine-API-Key': os.environ.get('REDMINE_KEY'),
 'Content-Type': 'application/json',
  
   }
   
   response = requests.request("POST", url, headers=headers, data=payload)
   print(response)
   if(str(response)== "<Response [201]>"): 
      return("CONGRATS 🤩"+"\nProject created successfully!")
   else:
    return(str(response)+ "\nSorry error occured!")

def project_list():
     url = "https://www.kore.koders.in/projects.json"
     projects = get_json(url, hdr1).json()
     project_list =""
     
     j=0;
     for i in projects["projects"]:
          j=j+1
          project_list=project_list+str(j)+") "+str((i["name"]))+"\n"
          
     return project_list


def issues(project_name):
     url = "https://www.kore.koders.in/projects.json"
     
     ctime = datetime.datetime.now()
     name=str(project_name)
     issue_url = "https://www.kore.koders.in/projects/"+name+"/issues.json?set_filter=1"
     issues = get_json(issue_url, hdr1).json()
     #print(issues)
     list =""
     for i in issues["issues"]:
          
          due=i["due_date"]
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
               else:
                 list=list+("Issue #"+str(i["id"])+" ( Expires in "+str(delta.days)+" days )"+"\nStatus: "+str(i["status"]["name"])+"\nAssigned by: "+str(i["author"]["name"])+"\nAssigned to: "+str(i["assigned_to"]["name"])+"\nSubject: "+str(i["subject"])+"\nDue Date is: "+str(due)+"\n\n")
                 
                 
     return list
     

