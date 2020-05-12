import speech_recognition as sr
from time import ctime
import webbrowser, time,pyttsx3, requests, json
import config

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate',160)

r1 = sr.Recognizer()
r2 = sr.Recognizer()
r3 = sr.Recognizer()

def rec_audio(ask = False):
    if ask:
        returnSpeech(ask)
    with sr.Microphone() as source:
        audio = r3.listen(source)
        voice_data = ''

        try:
            voice_data = r3.recognize_google(audio)

        except sr.UnknownValueError:
            returnSpeech('Sorry, I do not understand you')
        except sr.RequestError:
            returnSpeech('Sorry, Speech server is down')

        return voice_data

def returnSpeech(audio_str):

    engine.say(audio_str)
    engine.runAndWait()
    print(audio_str)

def respond(voice_data):

    if 'what is the time' in voice_data:
        returnSpeech(ctime())

    if 'what is your name' in voice_data:
        returnSpeech("My name is Jimmy, Samuel's voice assistant. what is yours? ")

        with sr.Microphone() as source:
            reply = r2.listen(source)
            response = r2.recognize_google(reply)

        returnSpeech('Nice to meet you ' + response)
        returnSpeech('Do you want to search something on google, know your current location, the time or the weather, ask me')

    if 'who are you' in voice_data:
        returnSpeech('')

    if 'who you' in voice_data:
        returnSpeech('I am not a preacher of love, I AM the liquid metal, I am war , I am a fight, I am indaboski bahose')

    if 'search' in voice_data:
        search = rec_audio('What do you want to search for')
        url = 'https://www.google.com/search?q=' + search
        webbrowser.get().open_new(url)
        returnSpeech('here is what I found for ' + search)

    if "my location" in voice_data:
        location = rec_audio('What is the location?')
        url = 'https://www.google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open_new(url)
        returnSpeech('here is the location of ' + location)

    if 'can you hear' in voice_data:
        returnSpeech('Yes I can hear you')


    if 'weather' in voice_data:
        loc = rec_audio('what is the location?')

        resp = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+loc+'&appid=' + config.api_key + "'")
        if resp.status_code == 200:
            data = [resp.json()]
            for i in data:
                weather = i['weather']
                temp = [i['main']]

            for j in weather:
                main = j['main']
                des = j['description']
                print(main)
                returnSpeech('The current weather in ' + loc + ' is ' + main + '. \n Overall, It is ' + des)

            for k in temp:
                temp = str(int(k['temp'] - 273))
                feels = str(int(k['feels_like'] - 273))

                returnSpeech('The current temperature is '+ temp + ' degrees')
                returnSpeech('It Feels like ' + feels + ' degrees')

        else:
            print('Error ' + str(resp.status_code) + ' occurred')

    if 'exit' in voice_data:
        returnSpeech('Goodbye')
        exit()

time.sleep(1)


returnSpeech('Hi How may I help you?')
while 1:
    voice_data = rec_audio()
    respond(voice_data)
