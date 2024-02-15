from __future__ import print_function

import datetime
import os.path
from datetime import datetime
from datetime import date
from time import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# library for google sheets
import gspread

sa = gspread.service_account()
sh = sa.open("Python Workout Data")

wks = sh.worksheet("Sheet1")

# col = wks.cell(1,5)
# cell = wks.find("chest")
# print(cell)

# print(col.col)

color = {
    'red':0/255,
    'green':93/255,
    'blue':93/255
    }


start_col = wks.cell(1,1)
for i in range(3, wks.col_count):
    c = wks.cell(1,i)
    if c.value == None:
        start_col = c.col
        break


# wks.update('A1:D1', [['chest','arms', 'back','shoulders']])


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

    except HttpError as error:
        print('An error occurred: %s' % error)


    # start of my Workout assistant code, everything above is essential for using G-Cal API
    

    muscle_group_list = ['chest', 'arms', 'shoulders', 'back']

    # chest = {
    #     'Incline Chest Fly 4-6 reps': [40,45,45],
    #     'Flat Chest Fly 4-6 reps': [45,50,50],
    #     'Decline Chest Fly 4-6 reps': [45,45,50]
    #     }

    # arms = {
    #     'Biceps': [],
    #     'Dumbbell Curls 4-6 + 3 assisted reps': [30,35,35],
    #     'Incline bench curls 6-8 reps': [22.5,25,25],
    #     'Hammer curl slow decline 3-5 reps': [25,30,30],
    #     'Triceps': [],
    #     'Close grip Press 6-8 reps': [35,40,40],
    #     'Incline dumbbell kickbacks 6-8 reps': [10,12.5,12.5]
    #     }

    # shoulders = {
    #     'Seated Shoulder Extension 4-6 reps': [40,40,45],
    #     'Lateral Raise 4-6 reps': [20,20,20],
    #     'Front Raise 4-6 reps': [20,22.5,22.5]
    #     }

    # back = {
    #     'Pull Ups': ['Max Out (4-5)'],
    #     'Hop Pull Ups': [8]
    #     }

 

    def print_workout(muscle):
        # muscle = 'chest'
        
        latest = wks.findall(muscle)
        col = latest[len(latest) - 1].col
        row_value = 1
        col_values = wks.col_values(col)
        wks.update_cell(row_value, start_col, muscle)
        wks.update_cell(1, start_col + 1, str(date.today()))
        row_value += 1
        # col_values.pop(0)
        # print(col_values) 
        description_string = ''

        for i in range(1, len(col_values)):
            print(col_values[i] + ': ', end = '')
            if col_values[i].replace(".", "").isnumeric() == False and col_values[i+1].replace(".", "").isnumeric():
                print('\n' + 'previously ' + str(col_values[i+1:i+4]), end = '')
            value = input()
            if value.isdigit():
                description_string += (str(value) + '\n')
                wks.update_cell(row_value, start_col, value)
                row_value += 1
            else:
               description_string += (str(col_values[i]) + '\n')
               wks.update_cell(row_value, start_col, col_values[i])
               row_value += 1
               
            # wks.format(row, start_col, {
            #     'backgroundColor': color
            #     })

            print("\033[A")

        description_string += '\n'
        return(description_string)
        

    now = datetime.now().isoformat('T')
    start = (str(now)[0:16] + ':00-07:00')
    print("What are you excercising today?\nEnter: 'chest' 'back' 'arms' 'shoulders'")
    user_input = input("Enter muscle group: ")
    current_time = datetime.now().strftime("%I:%M %p")
    print('\nBegan at ' + current_time)

    while user_input not in muscle_group_list:
        print ("Enter muscle from list")
        user_input = input("Enter muscle group: ")
    user_input_string = user_input
    # muscle_group = locals()[user_input]
    description = user_input + '\n'
    description += print_workout(user_input_string)
    

    user_input2 = input("Would you like to do another workout?\nEnter: 'chest' 'back' 'arms' 'shoulders'\nor hit 'return' to exit\n")

    while user_input2 in muscle_group_list:
        description += user_input2 + '\n'
        global start_col
        start_col += 2
        print(start_col)
        # muscle_group = locals()[user_input2]
        user_input_string += " / " + user_input2
        description += print_workout(user_input2)
        user_input2 = input("Would you like to do another workout?\nEnter: 'chest' 'arms' 'shoulders'\nor hit 'return' to exit\n")
        print ()
    print("Have a nice day!\n")
    now = datetime.now().isoformat('T')
    end = (str(now)[0:16] + ':00-07:00')


    event = {
    'summary': user_input_string,
    'location': '791 Kingston Ave',
    'description': description,
    'start': {
        'dateTime': start,
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': end,
        'timeZone': 'America/Los_Angeles',
    }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))




if __name__ == '__main__':
    main()
