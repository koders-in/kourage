import requests
import json
import pdfkit 
from datetime import date
import datetime

item_data="""
					<tr>
						<td><a class="cut">-</a><span>{sno}</span></td>
						<td><span>{item}</span></td>
						<td><span>{qty}</span></td>
						<td><span data-prefix>Rs. </span><span>{rate}</span></td>
						<td><span data-prefix>Rs. </span><span>{amnt}</span></td>
					</tr>
				
				"""

class Main:
 operation_id="1"
 url = "http://0.0.0.0:3000/projects/test/operations/"+operation_id+".json"

 payload={}
 headers = {
  'X-Redmine-API-Key': 'your key',
  }

 response = requests.request("GET", url, headers=headers, data=payload).json()
 data=response["operation"]["description"]
 data1 = json.loads(data)
 date=response["operation"]["operation_date"]
 dates=str(date)
 due_date=""
 for element in dates[0:10:1]: 
	 due_date=due_date+element

 date_time_obj = datetime.datetime.strptime(due_date, '%Y-%m-%d')
 final_duedate=(datetime.datetime.strftime(date_time_obj,'%b %d, %Y'))
 current_date=(datetime.datetime.strftime(datetime.date.today(),'%b %d, %Y'))
 name=str(data1["Billed_To"]["name"])
 address=str(data1["Billed_To"]["Address"])
 email=str(data1["Billed_To"]["Email"])
 payment_method=str(data1["payment_method"])
 invoice_id=str(data1["Invoice"]["id"])

 
 items=""
 Total_Amount=0
 for i in data1["Items"]:
   Total_Amount=Total_Amount+(int(i["Rate"])*int(i["Quantity"]))
   items += item_data.format(sno=str(i["id"]),item=str(i["name"]),qty=str(i["Quantity"]),rate=str(i["Rate"]),amnt=str(int(i["Rate"])*int(i["Quantity"])))
   
 
 





HTML_File=open('index.html','r')
s = HTML_File.read().format(p=Main)
HTML_File.close()
invoice_html=open("out.html",'w')
invoice_html.write(s)
invoice_html.close()
pdfkit.from_file('out.html', 'Invoice_' + str(Main.invoice_id) + '.pdf')
