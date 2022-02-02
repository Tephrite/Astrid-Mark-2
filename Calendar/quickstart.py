from __future__ import print_function

import datetime
from itertools import count
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Learning.Conversation.entity_recognition_training import get_date

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_credentials():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('Calendar/token.json'):
        creds = Credentials.from_authorized_user_file('Calendar/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('Calendar/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_events(event_count=10):
    creds = get_credentials()
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=event_count, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = str(event['start'].get('dateTime'))
            if "T" in start:
                start = start.split("T")[1]
                start = [start.split(":")[0], start.split(":")[1]]
            else: 
                start = "All Day"
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_todays_events(sentence):
    print("TODAYS EVENTS")
    creds = get_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat() + 'T00:00:00' + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return('You are free the rest of the day')

        return_string = ""
        # Prints the time and name of the event
        for event in events:
            start = str(event['start'].get('dateTime'))
            if "T" in start:
                start = start.split("T")[1]
                start = [start.split(":")[0], start.split(":")[1]]
                return_string += "At "+start[0]+":"+start[1]
            else: 
                start = "All Day"
                return_string += start
                
            return_string += " you have "+event['summary'] +"\n"
            
        print(return_string)
        return(return_string)

    except HttpError as error:
        print('An error occurred: %s' % error)
    
def get_day_events(sentence):
    print("GET SPECIFIC DAY EVENTS")
    date = get_date(sentence)
    creds = get_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)

        print("date:", date)
        # Call the Calendar API
        starting_date = datetime.datetime(date[2],date[1],date[0],0,0,0).isoformat()+ 'Z'
        ending_date = datetime.datetime(date[2],date[1],date[0],23,0,0).isoformat() + 'Z'  # 'Z' indicates UTC time
        
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=starting_date, timeMax=ending_date, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return('You are free all day')
        
        return_string = ""
        
        # Prints the time and name of the event
        for event in events:
            start = str(event['start'].get('dateTime'))
            if "T" in start:
                start = start.split("T")[1]
                start = [start.split(":")[0], start.split(":")[1]]
                return_string += "At "+start[0]+":"+start[1]
            else: 
                start = "All Day"
                return_string += start
                
            return_string += " you have "+event['summary'] +"\n"
            
        print(return_string)
        return(return_string)

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_x_days_events(sentence):
    print("ADD EVENT")
    
def add_event():
    print("ADD EVENT")
    
def delete_event():
    print("DELETE EVENT")
    
def move_event():
    print("MOVE EVENT")
    
def add_reminder():
    print("ADD REMINDER")
    
def delete_reminder():
    print("DELETE REMINDER")

def rename_event():
    print("RENAME EVENT")  
          
