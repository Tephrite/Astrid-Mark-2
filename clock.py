from datetime import datetime
import pytz
import dateutil.parser

from Learning.Conversation.entity_recognition_training import get_location, extract_time

text = "set a timer for 1 minute"
local = "Brighton"

alarms = []
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
    
def get_timezone(country):
    for tz in pytz.common_timezones:
        if country in tz:
            return(tz)

def get_time_difference(sentence):
    print("THIS IS TIME DIFFERENCE")  
    

#Makes a check to see if a timer has been set for the current time
def check_alarms():
    current_hour = int(datetime.now().strftime("%I"))
    current_min = int(datetime.now().strftime("%M"))
    
    for alarm in alarms:
        if current_hour == alarm[0]:
            if current_min == alarm[1]:
                print("RING DING DING")
    
def set_alarm(sentence):
    time = extract_time(sentence)
    h = time[0]
    m = time[1]
    
    alarm = [h,m]
    
    alarms.append(alarm)
    
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
    alarms.pop(0)
    
    return("Alarm deactivated")

def snooze_alarm(sentence):
    try:
        time = extract_time(sentence)
        hour = time[0]
        minute = time[1]
    except:
        hour = int(datetime.now().strftime("%I"))
        minute = int(datetime.now().strftime("%M"))
        
        
    for alarm in alarms:
        print("for")
        if hour == alarm[0]:
            if minute == alarm[1]:
                if minute > 54:
                    # TODO: Account for if its 23:55
                    alarm = [hour+1, minute-55]
                else:
                    alarm = [hour, minute+5]
    
    return("Alarm Snoozed")
    
def set_timer(sentence):
    time = extract_time(sentence)
    h = time[0]
    m = time[1]
    
    current_h = int(datetime.now().strftime("%I"))
    current_m = int(datetime.now().strftime("%M"))
    
    timer_h = current_h + h
    timer_m = current_m + m
    
    if timer_m > 54:
        timer_h += 1
        timer_m -= 55
    
    timer = [timer_h, timer_m]
    timers.append(timer)
    
    return_string = "Timer set for "
    
    if h == 0:
        return_string += str(m)
        if m > 0:
            return_string += " minutes"
        else:
            return_string += " minute"
    if m == 0:
        return_string += str(h)
        if h > 0:
            return_string += " hours"
        else:
            return_string += " hour"
        
    return return_string
    
def stop_timer(sentence):
    timers.pop(0)
    
    return("Timer deactivated")
    
#Makes a check to see if a timer has been set for the current time
def check_timers():
    current_hour = int(datetime.now().strftime("%I"))
    current_min = int(datetime.now().strftime("%M"))
    
    for timer in timers:
        if current_hour == timer[0]:
            if current_min == timer[1]:
                print("RING DING DING")
                