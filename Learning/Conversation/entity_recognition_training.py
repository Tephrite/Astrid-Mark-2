import nltk
import spacy
from datetime import datetime

def get_location(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    chunks = nltk.ne_chunk(pos_tags, binary=False)
    location = ""
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            location = ''.join(c[0] for c in chunk)

    if location == "":
        location = "Brighton"
    print ("Using: " + location)
    return location

def get_activity(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    chunks = nltk.ne_chunk(pos_tags, binary=False)
    result = []
    
    for chunk in chunks:
        if "CD" in chunk:
            chunk = str(chunk)
            time = chunk[chunk.find("('")+2:chunk.find("',")]
            #Handle all time formats
            # for fmt in ('%I:%M%p','0%I:%M%p',
            #             '%I a.m.',
            #             '%I p.m.',
            #             '%I',
            #             '%I hour and %M minute', '%I hours and %M minute', '%I hour and %M minutes', '%I hours and %M minutes', 
            #             '%I hour %M minute', '%I hours %M minute', '%I hour %M minutes', '%I hours %M minutes',
            #             '%I hour', '%I hours',
            #             '%M minute', '%M minutes'):
            #     try:
            #         if fmt == '%I p.m.':
            #             result.append([int(datetime.strptime(str(time), fmt).hour)+12, datetime.strptime(str(time), fmt).minute])
            #         else:
            #             result.append([datetime.strptime(str(time), fmt).hour, datetime.strptime(str(time), fmt).minute])
                        
            #     except ValueError:
            #         pass            
    return result   
          
def extract_time(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    print(sentence)
    for ent in doc.ents:
        print(ent, ent.label_)
        if ent.label_ == "TIME" or ent.label_ == "DATE" or ent.label_ == "CARDINAL":
            try:
                if ":" in str(ent):
                    hour = str(ent).split(':')[0]
                    minute = str(ent).split(':')[1]
                elif "minute" in str(ent):
                    hour = 0
                    minute = str(ent).split(" minute")[0].split(" ")
                    minute = minute[len(minute)-1]        
                elif "hour"  in str(ent) and "minute" in str(ent):
                    hour = str(ent).split(" hour")[0]
                    minute = str(ent).split(" minute")[0].split(" ")
                    minute = minute[len(minute)-1]
                elif "hour" in str(ent):
                    minute = 0
                    hour = str(ent).split(" hour")[0].split(" ")
                    if "an" in str(ent) or "a " in str(ent):
                        hour = 1 
                    else:
                        hour = hour[len(hour)-1]
                        
                time = [int(hour), int(minute)]
                print(time)
                return time
            
            except:
                pass      
                
def get_time(sentence):
    words = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(words)
    chunkGram = r""" 
        Chunk:
            {<CD><NN.?>*<.>*<CC>*<CD><NN.?>*<.>*<CC>*} 
            {<CD><NN.?>*<.>*} 
        """
    chunkParser = nltk.RegexpParser(chunkGram)
    chunks = chunkParser.parse(pos_tags)
    
    result = []
    
    for chunk in chunks:
        if "Chunk" in str(chunk):
            chunk = str(chunk)
            time = (chunk[chunk.find("(Chunk ")+7:chunk.find(")")].replace("/CD","")).replace("/NNS","")
            if "NN" in time:
                time = time.replace("/NN","")               
            if " ./" in time:
                time = time.replace(" ./", "")
            if "/CC" in time:
                time = time.replace("/CC", "")
            #Handle all time formats
            for fmt in ('%I:%M%p','0%I:%M%p', '%I:%M a.m.', '%I:%M p.m.',
                        '%I a.m.',
                        '%I p.m.',
                        '%I',
                        '%I hour and %M minute', '%I hours and %M minute', '%I hour and %M minutes', '%I hours and %M minutes', 
                        '%I hour %M minute', '%I hours %M minute', '%I hour %M minutes', '%I hours %M minutes',
                        '%I hour', '%I hours',
                        '%M minute', '%M minutes'):
                try:
                    if fmt == '%I p.m.' or fmt == '%I:%M p.m.':
                        result.append([int(datetime.strptime(str(time), fmt).hour)+12, datetime.strptime(str(time), fmt).minute])
                    else:
                        result.append([datetime.strptime(str(time), fmt).hour, datetime.strptime(str(time), fmt).minute])
                        
                except ValueError:
                    pass      
    return result            

#Returns date in the format [day, month, year]
def get_date(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    today = datetime.now()
    result = ""
    
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ == "DATE" or ent.label_ == "ORDINAL":
                if ":" not in str(ent):
                    #Handle format 21st February 2020
                    for fmt in ('%dst %B %Y', '%dnd %B %Y', '%drd %B %Y', '%dth %B %Y', 'the %dst of %B %Y', 'the %dnd of %B %Y', 'the %drd of %B %Y', 'the %dth of %B %Y'):
                        try:
                            result = [datetime.strptime(str(ent), fmt).day, datetime.strptime(str(ent), fmt).month, datetime.strptime(str(ent), fmt).year]
                        except ValueError:
                            #Handle format February 21st 2020
                            for fmt in ('%B %dst %Y', '%B %dnd %Y', '%B %drd %Y', '%B %dth %Y'):
                                try:
                                    result = [datetime.strptime(str(ent), fmt).day, datetime.strptime(str(ent), fmt).month, datetime.strptime(str(ent), fmt).year]
                                except ValueError:
                                    #Handle format 21st February
                                    for fmt in ('%dst %B', '%dnd %B', '%drd %B', '%dth %B', 'the %dst of %B', 'the %dnd of %B', 'the %drd of %B', 'the %dth of %B'):
                                        try:
                                            result = [datetime.strptime(str(ent), fmt).day, datetime.strptime(str(ent), fmt).month, today.year]
                                        except ValueError:
                                            #Handle format February 23rd
                                            for fmt in ('%B %dst', '%B %dnd', '%B %drd', '%B %dth'):
                                                try:
                                                    result = [datetime.strptime(str(ent), fmt).day, datetime.strptime(str(ent), fmt).month, today.year]
                                                except ValueError:
                                                    #Handle format 21nd 
                                                    for fmt in ('%dst', '%dnd', '%drd', '%dth', 'the %dst', 'the %dnd', 'the %drd', 'the %dth', 'the %dst at', 'the %dnd at', 'the %drd at', 'the %dth at'):
                                                        try:
                                                            #Check if day has already past
                                                            if today.day > datetime.strptime(str(ent), fmt).day:
                                                                result = [datetime.strptime(str(ent), fmt).day, today.month+1, today.year]
                                                            else:
                                                                result = [datetime.strptime(str(ent), fmt).day, today.month, today.year]
                                                        except ValueError:
                                                            #Handle english phrasing
                                                            for fmt in ('%d'):
                                                                try:
                                                                    if "after tomorrow" in sentence:
                                                                        result = [today.day+2, today.month, today.year]
                                                                    elif "tomorrow" in sentence:
                                                                        result = [today.day+1, today.month, today.year]
                                                                    elif "before yesterday" in sentence:
                                                                        result = [today.day-2, today.month, today.year]  
                                                                    elif "yesterday" in sentence:
                                                                        result = [today.day-1, today.month, today.year]
                                                                except ValueError:
                                                                    pass
    else:           
        #Handle exceptions
        emp_lis = ""
        for z in sentence:
            if z.isdigit():
                emp_lis += z
            
        for fmt in ('%dst', '%dnd', '%drd', '%dth', '%d'):
            try:
                #Check if day has already past
                if today.day > datetime.strptime(emp_lis, fmt).day:
                    result = [datetime.strptime(emp_lis, fmt).day, today.month+1, today.year]
                else:
                    result = [datetime.strptime(emp_lis, fmt).day, today.month, today.year]
            except ValueError:
                pass
    if result:            
        result = date_fix(result)
    return result

#Checks that date exists and if not, reformats (eg. 33rd of the 13th month changes to, 2nd of the 1st month next year)
def date_fix(date):
    is_leapyear = date[2] % 4 == 0 and (date[2] % 100 != 0 or date[2] % 400 == 0)
    thirty_one = [1, 3, 5, 7, 8, 10] #all months with 31 except december
    thirty = [4, 6, 9, 11] #remaining months except february
    
    #Handle months with 31
    for month in thirty_one:
        if date[1] == month:
            if date[0] > 31:
                date[1] += 1
                date[0] -= 31
    
    #Handle months with 30
    for month in thirty:
        if date[1] == month:
            if date[0] > 30:
                date[1] += 1
                date[0] -= 30
                
    #Handle February
    if is_leapyear:
        if date[1] == 2:
            if date[0] > 29:
                date[1] += 1
                date[0] -= 29
    else:
        if date[1] == 2:
            if date[0] > 28:
                date[1] += 1
                date[0] -= 28
                
    #Handle December
    if date[1] == 12:
        if date[0] > 31:
            date[1] -= 11
            date[0] -= 31
            date[2] += 1

    return(date)