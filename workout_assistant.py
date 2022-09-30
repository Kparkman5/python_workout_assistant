from __future__ import print_function

import datetime
import os.path
from time import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    

    muscle_group_list = ['chest', 'biceps', 'triceps', 'shoulders']

    chest = {
        'Incline Chest Fly 4-6 reps': [40,40,40],
        'Flat Chest Fly 4-6 reps': [40,45,45],
        'Decline Chest Fly 4-6 reps': [35,40,40]
        }

    biceps = {
        'Dumbbell Curls 4-6 + 3 assisted reps': [25,30,30],
        'Incline bench curls 6-8 reps': [17.5,20,20],
        'Hammer curl slow decline 4-6 reps': [22.5,25,25]
        }

    triceps = {
        'Close grip Press 6-8 reps': [30,30,35],
        'Incline dumbbell kickbacks 10-15 reps': [10,10,12.5]
        }

    shoulders = {
        'Seated Shoulder Extension 4-6 reps': [35,40,40],
        '3 Part Shoulder Workout 4-5 reps': [15,15,17.5]
        }

    def print_workout(muscle):
        description_string = ''
        for i in muscle:
            print(i, end = '')
            description_string += (str(i) + '\n')
            input()
            print("\033[A")
            for j in muscle[i]:
                print(j, end = '')
                description_string += (str(j) + '\n')
                input()
        description_string += '\n'
        return(description_string)

    now = datetime.datetime.now().isoformat('T')
    start = (str(now)[0:16] + ':00-07:00')
    end_hour = int(start[11:13]) + 1
    end = start[0:11] + str(end_hour) + start[13:26]
    print("What are you excercising today?\nEnter: 'chest' 'biceps' 'triceps' 'shoulders'")
    user_input = input("Enter muscle group: ")

    while user_input not in muscle_group_list:
        print ("Enter muscle from list")
        user_input = input("Enter muscle group: ")
    user_input_string = user_input
    print ()
    muscle_group = locals()[user_input]
    description = user_input + '\n'
    description += print_workout(muscle_group)

    user_input2 = input("Would you like to do another workout?\nEnter: 'chest' 'biceps' 'triceps' 'shoulders'\nor hit 'return' to exit\n")

    while user_input2 in muscle_group_list:
        description += user_input2 + '\n'
        muscle_group = locals()[user_input2]
        user_input_string += " / " + user_input2
        description += print_workout(muscle_group)
        user_input2 = input("Would you like to do another workout?\nEnter: 'chest' 'biceps' 'triceps' 'shoulders'\nor hit 'return' to exit\n")
        print ()
    print("Have a nice day!\n")



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