import Calendar.quickstart as cal
import Learning.Conversation.entity_recognition_training as ent

### Calendar Tests

def get_day_events_tests():
    cal.get_day_events("21st February")

    cal.get_day_events("January 23rd")
    
    cal.get_day_events("4th")

    cal.get_day_events("January 23rd 2024")

    cal.get_day_events("the 1st")

    cal.get_day_events("1st April")
    
    cal.get_day_events("do I have anything on the 12th")
    
    cal.get_day_events("what do I have tomorrow")

def add_event_tests():
    cal.add_event("Add an event for the 21st at 1:20pm") 
    
    cal.add_event("Add an event on the 21st at 1 a.m. and finishes at 4:15 p.m.") 
    
    cal.add_event("Add gym at 6 p.m on the 21st to the calendar") 
    
    
### Entity Recognition Tests
   
def get_time_tests():
    print(ent.get_time("Add an event for the 21st at 1:20 p.m."))
    
    print(ent.get_time("Set a timer for 20 minutes"))
    
    print(ent.get_time("Set a timer for 1 hour 20 minutes"))
    
    print(ent.get_time("Set a timer for 2 hours 20 minutes"))
    
    print(ent.get_time("Set a timer for 2 hours and 20 minutes"))
    
    print(ent.get_time("Set an alarm for 8 a.m."))

    print(ent.get_time("Set an alarm for 8 p.m."))
    
    print(ent.get_time("Set an alarm for 5"))

def get_date_tests():
    print(ent.get_date("Add an event for the 21st at 1:20pm"))
    
    print(ent.get_date("what do I have tomorrow"))
    
    print(ent.get_date("21st February"))
    
    print(ent.get_date("January 23rd "))
    
    print(ent.get_date("January 23rd 2024"))
    
    print(ent.get_date("4th"))
    
    print(ent.get_date("the 1st"))
    
    print(ent.get_date("1st April"))
    
    print(ent.get_date("do I have anything on the 12th"))
    