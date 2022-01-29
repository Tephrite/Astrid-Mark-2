from datetime import datetime
import pytz
import dateutil.parser

from Learning.Conversation.entity_recognition_training import get_location

text = "set an alarm for 2:12"
local = "Brighton"
timers = []

# Get time from location
def get_time(sentence):
    
    location = get_location(sentence)
    
    if location == local:
        now = datetime.now()
        time = now.strftime("%I:%M %p")
        
        print("The time is "+time)
        return("The time is "+time)
    else:
        tz = get_timezone(location)
        country = pytz.timezone(tz)
        country_time = datetime.now(country)
        
        print("The time in "+location+" is " + country_time.strftime("%I:%M %p"))
        return ("The time in "+location+" is " + country_time.strftime("%I:%M %p"))

#Extract time from sentence
def extract_time(sentence):
    datetime = dateutil.parser.parse(sentence, fuzzy=True)
    return datetime
    
    
def get_timezone(country):
    for tz in pytz.common_timezones:
        if country in tz:
            return(tz)

def get_time_difference(sentence):
    print("THIS IS TIME DIFFERENCE")  

#Makes a check to see if a timer has been set for the current time
#TODO: Double check that this works with multiple alarm
def check_timers():
    current_hour = int(datetime.now().strftime("%I"))
    current_min = int(datetime.now().strftime("%M"))
    
    for alarm in timers:
        if current_hour == alarm[0]:
            if current_min == alarm[1]:
                print("RING DING DING")
                timers.pop(0)
    
def set_alarm(sentence):
    h = extract_time(sentence).hour
    m = extract_time(sentence).minute
    alarm = [h,m]
    
    timers.append(alarm)
    
    if h < 9:
        hour = "0"+str(h)
    else:
        hour = str(h)
        
    if m < 9:
        min = "0"+str(m)
    else:
        min = str(m)
        
    return("Alarm set for "+hour+":"+min)
    
def stop_alarm(sentence):
    print("STOP ALARM")
    
def set_timer(sentence):
    print("SET TIMER")
    
def stop_timer(sentence):
    print("STOP TIMER")
    