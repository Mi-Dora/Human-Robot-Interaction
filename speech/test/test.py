import os

os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'
import speech_recognition as sr
import json

r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    print('say something: ')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print('you said: {}'.format(text))
    except:
        print('sorry could not recognize what you said')
