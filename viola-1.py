from posixpath import split
import speech_recognition as sr
from time import ctime, monotonic
from gtts import gTTS
import webbrowser
import os
import random
import locale
locale.setlocale(locale.LC_ALL, 'turkish')
import time

r = sr.Recognizer()
r.energy_threshold = 300

def viola_speak(audio_string):
    tts = gTTS(text=audio_string,lang='tr')
    rand = random.randint(1,10000000)
    audio_file = 'audio-'+str(rand)+'.mp3'
    tts.save(audio_file)
    print(audio_string)

def search(question):
    if question:
        if 'nedir' in question:
            text = question.split('nedir')[0]
            url = 'https://www.google.com/search?q='+text
            webbrowser.get().open(url)
            viola_speak('İşte '+ text +'için bulduğum sonuçlar.')
        else:
            text = question.split('kimdir')[0]
            url = 'https://www.google.com/search?q='+text
            webbrowser.get().open(url)
            viola_speak('İşte '+ text +'için bulduğum sonuçlar.')
        
    else:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:
                search = r.listen(source, timeout=4,phrase_time_limit=5)
                search2 = r.recognize_google(search,language="tr-tr")
                url = 'https://www.google.com/search?q='+search2
                webbrowser.get().open(url)
                viola_speak('İşte '+ search2 +' için bulduğum sonuçlar.')
            except sr.UnknownValueError:
                viola_speak('Afedersiniz, bu ifadeyi anlayamadım.')
            except sr.WaitTimeoutError:
                viola_speak('Dinleme zaman aşımına uğradı')

def find_location(location):
    if location:
        find = location.split(' nerede')[0]
        url = 'https://www.google.nl/maps/place/'+find
        webbrowser.get().open(url)
        viola_speak('İşte '+ find +' konumu için bulduğum sonuçlar.')
    else:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            try:                
                search = r.listen(source, timeout=4,phrase_time_limit=5)
                search2 = r.recognize_google(search,language="tr-tr")
                url = 'https://www.google.nl/maps/place/'+search2
                webbrowser.get().open(url)
                viola_speak('İşte '+ search2 +' konumu için bulduğum sonuçlar.')
            except sr.UnknownValueError:
                viola_speak('Afedersiniz, bu ifadeyi anlayamadım.')
            except sr.WaitTimeoutError:
                viola_speak('Dinleme zaman aşımına uğradı')

def respond(text_data):
    if 'adın ne' in text_data:
        viola_speak('Benim adım Viola! Senin adın ne?')
    elif 'benim adım' in text_data:
        viola_speak('Memnun oldum!')
    elif 'selam' in text_data:
        viola_speak('Merhaba! Nasıl yardımcı olabilirim?')
    elif 'saat kaç' in text_data:
        viola_speak( ctime())
    elif 'araştır' in text_data:
        viola_speak('Neyi araştırmamı istersiniz?')
        search('')
    elif 'nedir' in text_data:
        search(text_data)
    elif 'kimdir' in text_data:
        search(text_data)
    elif 'konum bul' in text_data or 'neresi' in text_data:
        viola_speak('Hangi konumu bulmak istersiniz?')
        find_location('')
    elif 'nerede' in text_data:
        find_location(text_data)
    elif 'yok et' in text_data:
        exit()

while 1:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=4,phrase_time_limit=5)
            voice_data = r.recognize_google(audio,language="tr-tr")
            if 'viyola' in voice_data:
                viola_speak("Merhaba! Nasıl yardımcı olabilirim?")
                while 1:
                    try:
                        audio1 = r.listen(source, timeout=4,phrase_time_limit=5)
                        voice_data1 = r.recognize_google(audio1,language="tr-tr")
                        respond(voice_data1)
                    except sr.UnknownValueError:
                        viola_speak('Afedersiniz, bu ifadeyi anlayamadım.')
                    except sr.WaitTimeoutError:
                        viola_speak("Dinleme zaman aşımına uğradı")
        except sr.UnknownValueError:
            pass
        except sr.WaitTimeoutError:
            pass
