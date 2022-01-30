import nltk
import spacy

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
        
def extract_time(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    
    for ent in doc.ents:
        print(ent, ent.label_)
        if ent.label_ == "TIME" or ent.label_ == "DATE" or ent.label_ == "CARDINAL":
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
