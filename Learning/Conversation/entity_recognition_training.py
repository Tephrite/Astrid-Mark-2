import nltk

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
        
