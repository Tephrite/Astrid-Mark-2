from datetime import datetime
import pytz

from Learning.Conversation.entity_recognition_training import get_location

text = "What time is it in Paris"
local = "Brighton"

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
    

def get_timezone(country):
    for tz in pytz.common_timezones:
        if country in tz:
            return(tz)

def get_time_difference(sentence):
    print("THIS IS TIME DIFFERENCE")    