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
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


from weather import *
from clock import *
from music import *

recognizer = speech_recognition.Recognizer()

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model_gpt = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
step = 0 

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('Learning/Conversation/intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model_intents = load_model('chatbot_model.model')

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
    res = model_intents.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
        
    return return_list

def get_response(message, intents_list):
    tag = intents_list[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
        
    if "func:" in result:
        result = result.replace("func:","")
        result = eval(result + "(message)")
              
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
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
                
            message = recognizer.recognize_google(audio)
            print(message)
            message_l = message.lower()
        
        ints = predict_class(message_l)
        
        if float(ints[0]['probability']) > 0.9999:
            # Use Intent Classification
            result = get_response(message, ints)
        else:
            # Use GPT Conversation    
            new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
            chat_history_ids = model_gpt.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
            result = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        # Speak results
        speakText(result)
            
    except speech_recognition.UnknownValueError:
        print("I didn't understand, please try again")

                
    