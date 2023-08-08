import os
import re
from datetime import date as dt
import datetime as dtime
import shutil
from PyPDF2 import PdfReader
import pdfkit
from jinja2 import Environment, FileSystemLoader
from pdfminer.high_level import extract_text


#capture the current working directory
cwd = os.getcwd()

#Jinja2 essential system parameters!
env = Environment(loader=FileSystemLoader(f'{cwd}'))
template = env.get_template(f'template.html') 
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

#system files
system = ['dateScript.py','template.html','requirements.txt', 'Pipfile', 'Pipfile.lock', '.venv','Attendance_generator',]

#regex search terms
term1 = '(Session ran on time and as normal|Session started late but went well| Session ran over allotted time|Session was Curtailed or Cancelled)'
term2 = '([\d]*/[\d]*/[\d]{4})'
term3 = '(Student Name(\s([\w \s]*)\s)Session Conducted By)'


#session events sroted here
# dates = []

def Object():
    data = {
            'name': None,
            'events': [],
            'frequency': None,
            }

    attendance = {
        'Session ran on time and as normal':0,
        'Session started late but went well':0,
        'Session ran over allotted time':0,
        'Session was Curtailed or Cancelled':0,
    }
    return data, attendance

#attendeance tally
def frequency(events,attendance):
   for event in events:
       attendance[event['status']] = attendance.get(event['status']) + 1

#date sorting algorithm
def convert_date(item):
    return dtime.datetime.strptime(item['date'], "%d/%m/%Y").date()

# print(cwd.strip('Attendance_generator'))
# using the os moduile to create a list of all files in cwd
root = cwd.strip('Attendance_generator')
os.chdir(root)

directory = os.listdir()
for folder in directory:
    #condition to ignore systems files
    if (folder in system) or ('_attendance_5_2023.pdf' in folder) or ('.zip' in folder):
        continue
    else:
        data, attendance = Object()
        os.chdir(f'{root}/{folder}/')
        child_directory = os.listdir()

        for file in child_directory:
            print(file)
            try:
                #text from pdf is extracted here
                text = extract_text(file)
                # print(text) #test to make sure search terms work

                #search terms applied and relevent data is saved to variable
                status = re.search(term1,text)[0]
                date = re.search(term2,text)[0]
                student = re.search(term3,text)[2].strip('\n')
                # print(status)
                # print(os.getcwd())
                

                # print(f'{date} {status} {student}') #test to make sure search terms work

                #captured date is stored in event object and appended to dates array
                event = {
                'date':date,
                'status': status,
                }
                # dates.append(event)
                data['events'].append(event)
                data['name'] = student
            except:
                print('oh no')

        #events are filted to exclude any date greater than today dates
        data['events'] = [dat for dat in data['events'] if convert_date(dat) <= dt.today()]
        #we capture the number to events to present as individual sessions
        data['sessions'] = len(data['events'])
        #events are stored accoridng to date
        data['events'].sort(key=convert_date)

        # we print each event to the console
        for event in data.get('events'):
            print(event)

        #we change dircgtory in to the parent folder
        os.chdir(root)

        #we collecte the frequency of each attendance type and assing to data object
        frequency(data['events'],attendance)
        data['frequency'] = attendance

        #we pass the data to render to a html template
        html = template.render(data=data)
        htmlFile_name = f'{student}_attendance_{dt.today().month}_{dt.today().year}.html'
        pdfFile_name = f'{student}_attendance_{dt.today().month}_{dt.today().year}.pdf'
        #html is conveted to a PDF document
        pdfkit.from_string(html, pdfFile_name, configuration=config)
        #folder is removed from file once completed
        shutil.rmtree(folder)
            

    
    
