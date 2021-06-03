import datetime
import matplotlib.pyplot as plt
import time

from numpy import save
# GLOBAL VALUES
data=[]
dates=[]
names=[]
attendance={}
attendees={}
func_list='''   For your attendance type ~my_attendance
                For attendance by name attendance type ~overall_attendance_of some_name
                For total attendance type ~total_attendance
                For weekly attendance type ~weekly_attendance
                For monthly attendance type ~monthly_attendance 
                For custom bar graph of some no of days type ~custom_days_bar of no of days 
                For pie graph for person type ~pie_graph_of somename
                For bar graph of comparision type ~compare_pie names seperated by a ,
                For bar graph of comparision type ~compare_bar names seperated by a ,
                for dates absent of some person type ~dates_absent_of name
                for dates present of some person type ~dates_present_of name
                for dates weekly absent of some person type ~weekly_dates_absent_of name
                for dates weekly present of some person type ~weekly_dates_present_of name
                for dates monthly absent of some person type ~monthly_dates_absent_of name
                for dates monthly present of some person type ~monthly_dates_present_of name
                for dates custom absent of some person type ~custom_dates_absent_of name days
                for dates custom present of some person type ~custom_dates_present_of name days'''





def input_csv():
    with open("data.csv", "r") as file:
        for line in file.readlines():
            data.append(line.split(","))
        del data[0]

def to_get_dates():
    for each in data:
        if each[0] not in dates:
            dates.append(each[0])

def to_get_names():
    for each in data:
        if each[2] not in names:
            name=each[2]
            name=name.split('#')[0]
            name=name.lower()
            names.append(name)


def to_get_dict():
    for each in dates:
        legnth_of_data_set=len(data)
        names1=[]
        names2=[]
        temp=0
        while temp<legnth_of_data_set:
            if each==data[temp][0] and data[temp][1].startswith('11'):
                name=data[temp][2]
                name=name.lower()
                names1.append(name)
                names1=list(set(names1))
            elif each==data[temp][0] and data[temp][1].startswith('15'):
                name=data[temp][2]
                name=name.lower()
                names2.append(name)
                names2=list(set(names2))
            temp+=1
        attendance[f'{each}']=[names1,names2]      
    return(attendance)

def initialize():
    input_csv()
    to_get_dates()
    to_get_names()
    to_get_dict()


def search_by_name(name):
    try:
        name=name.lower()
        counter, total_counter = 0, len(dates*2)
        for date in dates:
            for each_attendance in attendance[f'{date}']:
                for each in each_attendance:
                    if name in each:
                        counter+=1
        
        return counter
    except Exception as error:
        print("Something went wrong in search_by_name")

def overall_attendance():
    try:
        for each in names:
            count=0
            count=search_by_name(each)
            attendees[f'{each}']=count
        
        return attendees
    except Exception as error:
        print("Something went wrong in overall attendance")

def last_dates(no_of_days):
    current_date = datetime.datetime.today()
    week_dates = []
    dated = []
    temp = 0

    
    while temp < no_of_days:
        previous_date = current_date - datetime.timedelta(days=temp)
        week_dates.append(previous_date)
        temp+=1

    #to convert datetime object into the correct format as required
    for each in week_dates:
        day = each.strftime("%A")
        if day != "Sunday" and day != "Saturday":
            formatted_time = each.strftime("%m/%d/%y")
            dated.append(str(formatted_time))
    
    for each in dated:
        try:
            print(attendance[f'{each}'])
        except Exception as error:
            print("No data Found for ->   " + str(error))
        
    return dated



def visualize_bar_overall_attendance():
    dateandtime=str(datetime.date.today())
    save_filename=f'./graphs/overall_bar_graph/overall_{dateandtime}.jpg'
    x, y = [],[]
    for each in names:
        count=search_by_name(each)
        y.append(count)
        x.append(each)
    y.append((len(dates)*2))
    x.append('Total shifts')
    plt.title('Overall attendance in Bar Chart')
    plt.barh(x, y, color ='green')
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename) 
    plt.show(block=False)
    plt.close()
    return save_filename

def visualize_pie_graph_search_by_name(name):
    dateandtime=str(datetime.date.today())
    save_filename=f'./graphs/person_pie_graph/{name}_{dateandtime}.jpg'
    count=search_by_name(name)
    y = [len(dates*2),count]
    mylabels = [f"{name} {count}",f"overall attendance {len(dates*2)}"]
    plt.title('Employee attendance in Pie Chart')
    plt.pie(y, labels = mylabels,  startangle = 0)
    figure = plt.gcf()
    figure.set_size_inches(8, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    time.sleep(.1)
    plt.close()
    return(save_filename)
    


def compare_bar(names_to_compare):
    dateandtime=str(datetime.date.today())
    save_filename=f'./graphs/comparision_bar_graph/{names_to_compare}_{dateandtime}.jpg'
    x,y = [],[]
    for name in names_to_compare:
        name=name.lower()
        counter=search_by_name(name)
        x.append(name)
        y.append(counter)
    x.append('Total dates')
    y.append(len(dates)*2)
    plt.title('Comparision of attendance in bar Chart')
    plt.barh(x,y,color ='Red')
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    plt.close()
    return(save_filename)

def pie_compare(namess):
    dateandtime=str(datetime.date.today())
    save_filename=f'./graphs/comparision_pie_graph/{namess}_{dateandtime}.jpg'
    y,mylabels=[],[]
    for name in namess:
        name=name.lower()
        count=search_by_name(name)
        y.append(count)
        mylabels.append(f"{name} {count}")
    plt.title('Comparision of attendance in Pie Chart')
    plt.pie(y, labels = mylabels,  startangle = 0)
    figure = plt.gcf()
    figure.set_size_inches(8, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    time.sleep(.1)
    plt.close()
    return(save_filename)
def weekly_bar():
    dateandtime=str(datetime.date.today())
    save_filename=f'./graphs/weekly_bar/weekly_bar_of_{dateandtime}.jpg'
    weekly_attendees={}
    weekly_name=[]
    dated=last_dates(7)
    for date in dated:
        if date in attendance.keys():
            for each_attendance in attendance[f'{date}']:
                for each in each_attendance:
                    weekly_name.append(each)    
    for each in weekly_name:
        counter=0
        counter=weekly_name.count(each)
        weekly_attendees[f'{each}']=counter
    y =list(weekly_attendees.values())

    x =list(weekly_attendees.keys())

    y.append(10)
    x.append('Total attendance')
    plt.barh(x,y, color='brown')
    plt.title('Total Weekly Attendance')
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    time.sleep(.1)
    plt.close()
    return(save_filename)


def monthly_bar():
    dateandtime=str(datetime.date.today())
    monthly_attendees={}
    monthly_name=[]
    total_dates=0
    save_filename=f'./graphs/monthly_bar/monthly_bar_of_{dateandtime}.jpg'
    dated=last_dates(30)
    for date in dated:
        if date in attendance.keys():
            total_dates+=1
            for each_attendance in attendance[f'{date}']:
                for each in each_attendance:
                    monthly_name.append(each)    
    for each in monthly_name:
        counter=0
        counter=monthly_name.count(each)
        monthly_attendees[f'{each}']=counter
    y =list(monthly_attendees.values())

    x =list(monthly_attendees.keys())

    y.append(total_dates*2)
    x.append('Total attendance')
    plt.barh(x,y, color='cyan')
    plt.title('Total Monthly Attendance')
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    time.sleep(.1)
    plt.close()
    return(save_filename)



def custom_bar(no_of_days):
    dateandtime=str(datetime.date.today())
    custom_attendees={}
    custom_name=[]
    total_dates=0
    save_filename=f'./graphs/custom_bar/custom_bar_of_{dateandtime}.jpg'
    dated=last_dates(no_of_days)
    for date in dated:
        if date in attendance.keys():
            total_dates+=1
            for each_attendance in attendance[f'{date}']:
                for each in each_attendance:
                    custom_name.append(each)    
    for each in custom_name:
        counter=0
        counter=custom_name.count(each)
        custom_attendees[f'{each}']=counter
    y =list(custom_attendees.values())

    x =list(custom_attendees.keys())

    y.append(total_dates*2)
    x.append('Total attendance')
    plt.barh(x,y, color='cyan')
    plt.title(f'Total  Attendance for {no_of_days} days')
    figure = plt.gcf()
    figure.set_size_inches(16, 8)
    plt.savefig(save_filename)
    plt.show(block=False)
    time.sleep(.1)
    plt.close()
    return(save_filename)


def days_present(name):
    present_dates=[]
    for each in data:
        name_check=each[2]
        name_check=name_check.lower()
        if name_check.startswith(name):
            present_dates.append(each[0])
        present_dates=list(set(present_dates))
        present_dates.sort()
    return(present_dates)


def days_absent(name):
    present_dates=days_present(name)
    absent_dates=[]
    for date in dates:
        if date not in present_dates:
            absent_dates.append(date)
    absent_dates.sort()
    return absent_dates

def week_dates_absent(name):
    weekly_absent_dates=[]
    present_dates=days_present(name)
    week_dates=last_dates(7)
    for date in week_dates:
        if date not in present_dates:
            weekly_absent_dates.append(date)
    return weekly_absent_dates

def custom_dates_absent(name,no_of_days):
    custom_absent_dates=[]
    present_dates=days_present(name)
    week_dates=last_dates(no_of_days)
    for date in week_dates:
        if date not in present_dates:
            custom_absent_dates.append(date)
    return custom_absent_dates


def week_dates_present(name):
    weekly_present_dates=[]
    present_dates=days_present(name)
    week_dates=last_dates(7)
    for date in week_dates:
        if date in present_dates:
            weekly_present_dates.append(date)
    return (weekly_present_dates)

def custom_dates_present(name,no_of_days):
    custom_present_dates=[]
    present_dates=days_present(name)
    week_dates=last_dates(no_of_days)
    for date in week_dates:
        if date in present_dates:
            custom_present_dates.append(date)
    return (custom_present_dates)

def month_dates_absent(name):
    monthly_absent_dates=[]
    present_dates=days_present(name)
    month_dates=last_dates(30)
    for date in month_dates:
        if date not in present_dates:
            monthly_absent_dates.append(date)
    return monthly_absent_dates


def month_dates_present(name):
    monthly_present_dates=[]
    present_dates=days_present(name)
    month_dates=last_dates(30)
    for date in month_dates:
        if date in present_dates:
            monthly_present_dates.append(date)
    return (monthly_present_dates)
   
# Driver code
if __name__ == '__main__':
    initialize()
    