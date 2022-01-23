from Learning.Conversation.entity_recognition_training import get_location
import requests

text = "Astrid what is the weather in Madrid"
local = "Brighton"
api_key = "91a4c385826ebd652b9004604c47d572"
unit = "celcius"

def get_api(location):
    key = "http://api.openweathermap.org/data/2.5/forecast?q="+location+"&appid="+api_key
    
    api_link = requests.get(key)
    api_data = api_link.json()
    
    if api_data['cod'] == '404':
        print("Invalid Location: {}, Please check your location".format(location))
    else:
        return api_data

## TODO: Write to config file
def change_unit(sentence):
    if "celcius" in sentence:
        unit = "celcius"
    else:
        unit = "farenheit"
        
def convert_temp(temp):
    if "celcius" in unit:
        return (temp-273.15)
    else:
        return temp
    
def get_temp(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    temp = (api_data['list'][0]['main']['temp'])
    temp = convert_temp(temp)

    print("The current temperature in {l} is {t:.0f} degrees".format(l=location, t=temp))
    return("The current temperature in {l} is {t:.0f} degrees".format(l=location, t=temp))

def get_coldest_temp(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    temp = (api_data['list'][0]['main']['temp_min'])
    temp = convert_temp(temp)
    
    print("The lowest it will be today in {l} will be {t:.0f} degrees".format(l=location, t=temp))
    return("The lowest it will be today in {l} will be {t:.0f} degrees".format(l=location, t=temp))

def get_hottest_temp(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    temp = (api_data['list'][0]['main']['temp_max'])
    temp = convert_temp(temp)
    
    print("The highest it will be today in {l} will be {t:.0f} degrees".format(l=location, t=temp))
    return("The highest it will be today in {l} will be {t:.0f} degrees".format(l=location, t=temp))

def get_weather(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    weather = ((api_data['list'][0]['weather'][0])['description'])
    
    if weather == "clear sky":
        weather = "clear skies"
    
    print("It is currently {w} in {l}".format(l=location, w=weather))
    return("It is currently {w} in {l}".format(l=location, w=weather))

## TODO: Incorporate into calendar
def get_precipitation(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    temp = (api_data['list'][0]['pop'])
    
    print("Chance of rain {l} is {t:.0f}".format(l=location, t=temp))
    return("Chance of rain {l} is {t:.0f}".format(l=location, t=temp))

def get_recommendation(sentence):
    precipitation = get_precipitation(sentence)
    if precipitation > 0.5:
        return ("There is a high chance of rain. I'd suggest a hoodie, raincoat or umbrella!")
    return ""