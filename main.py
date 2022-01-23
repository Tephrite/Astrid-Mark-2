import speech_recognition
import pyttsx3 as tts
import sys
import random
import pickle
import numpy as np
import json

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

from weather import *
from clock import *
from music import *

recognizer = speech_recognition.Recognizer()


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('Learning/Conversation/intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
        
    return return_list

def get_response(message, intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        
    if "func:" in result:
        result = result.replace("func:","")
        result = eval(result + "(message)")
        
    speakText(result)               
    return result

def speakText(text):
    
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()

### Main Loop   
speakText("Astrid Initialized")    
while True:
    
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
                
            message = recognizer.recognize_google(audio)
            print(message)
            message_l = message.lower()
        
        ints = predict_class(message_l)
        res = get_response(message,ints,intents)
            
    except speech_recognition.UnknownValueError:
        print("I didn't understand, please try again")

                
    