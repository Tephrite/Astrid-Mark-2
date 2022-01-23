from Learning.Conversation.entity_recognition_training import get_location
import requests

text = "Astrid what is the weather in Madrid"
local = "Brighton"
api_key = "91a4c385826ebd652b9004604c47d572"

def get_api(location):
    key = "http://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api_key
    
    api_link = requests.get(key)
    api_data = api_link.json()
    
    if api_data['cod'] == '404':
        print("Invalid Location: {}, Please check your location".format(location))
    else:
        return api_data
    
def get_temp(sentence):
    location = get_location(sentence)
    api_data = get_api(location)
    temp = ((api_data['main']['temp']) - 273.15)
    
    print("The current temperature in {l} is {t:.0f} degrees".format(l=location, t=temp))
    return("The current temperature in {l} is {t:.0f} degrees".format(l=location, t=temp))
