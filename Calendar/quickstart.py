from __future__ import print_function

import datetime
from itertools import count
import os.path
import speech_recognition
from tts import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Learning.Conversation.entity_recognition_training import get_activity, get_date, get_time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
recognizer = speech_recognition.Recognizer()

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

def stringify_event(events):
    # Prints the time and name of the event
    return_string = ""
    # Prints the time and name of the event
    for i, event in enumerate(events):
        start = str(event['start'].get('dateTime'))
        if i == 0:
            return_string += "You have:" +"\n"
        return_string += event['summary'] 
        
        if "T" in start:
            start = start.split("T")[1]
            start = [start.split(":")[0], start.split(":")[1]]
            if int(start[0]) > 12:
                start[0] = str(int(start[0]) - 12)
            return_string += " at "+start[0]+":"+start[1] +"\n"
        else: 
            start = "all day"
            return_string += start +"\n"
            
        
        
    print(return_string)
    return return_string
    
    
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

        return_string = stringify_event(events)
        return return_string

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

        return_string = stringify_event(events)
        return return_string

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
        
        return_string = stringify_event(events)
        return return_string

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_x_days_events(sentence):
    print("GET X DAYS EVENTS")
    date = get_date(sentence)
    
def add_event(sentence):
    print("ADD EVENT")
    creds = get_credentials()
    date = get_date(sentence)
    time = get_time(sentence)
    activity = get_activity(sentence)
    
    if activity: print("Activity:", activity)
    if date: print("Date:", date)
    if len(time) == 1: print("Start Time:", time[0])
    if len(time) == 2: print("End Time:", time[1])
    
    try:    
        
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            
            #If activity wasn't found
            if activity == []:
                speakText("What would you like the event to be called")
                audio = recognizer.listen(mic)
                activity = recognizer.recognize_google(audio)
                print("Activity:", activity)
            
            #If date wasn't found
            if not date:           
                speakText("What day is "+ activity)
                audio = recognizer.listen(mic)
                date = recognizer.recognize_google(audio)
                date = get_date(time)
                print("Date:", date)
            
            #If time wasn't found
            if not time:
                speakText("What time is"+ activity)
                audio = recognizer.listen(mic)
                time = recognizer.recognize_google(audio)
                time = get_time(time)
                print("Start Time:", time[0])
                
            #If only start time was found
            if len(time) == 1:
                speakText("What time does"+ activity+ "finish")
                audio = recognizer.listen(mic)
                time2 = recognizer.recognize_google(audio)
                time.append(get_time(time2)[0])
                print("End Time:", time[1])
                          
            #Convert to usable format
            start_dateTime = datetime.datetime(date[2], date[1], date[0], time[0][0], time[0][1]).isoformat() + 'Z'
            end_dateTime = datetime.datetime(date[2], date[1], date[0], time[1][0], time[1][1]).isoformat() + 'Z'
            
            #Create event
            event = {
                    'summary': activity,
                    'start': {
                        'dateTime': start_dateTime,
                    },
                    'end': {
                        'dateTime': end_dateTime,
                    },
                    }
            
            try:
                service = build('calendar', 'v3', credentials=creds)
                event = service.events().insert(calendarId='primary', body=event).execute()
                speakText(activity + "has been added to the calendar")
            except HttpError as error:
                print('An error occurred: %s' % error)
                        
            
    except speech_recognition.UnknownValueError:
        print("I didn't understand, please try again")
    
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
          
