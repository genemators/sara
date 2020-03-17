"""
APP: SARA - VOICE ASSISTANT
AUTHOR: Genemator Sakhib
VERSION: 0.0.1 alpha
STATUS: Rolling
"""

#
# Starting import process here
#
from __future__ import print_function

try:
    print('Importing "os" Module')
    import os

    print('"os" Module import completed successfully')

    print('Importing "time" Module')
    import time

    print('"time" Module import completed successfully')

    print('Importing "playsound" Module')
    import playsound

    print('"playsound" Module import completed successfully')

    print('Importing "SpeechRecognition" Module')
    import speech_recognition as sr

    print('"SpeechRecognition" Module import completed successfully')

    print('Importing "gtts" Module')
    from gtts import gTTS

    print('"gtts" Module import completed successfully')

    print('Importing "subprocess" Module')
    import subprocess

    print('"subprocess" Module import completed successfully')

    print('Importing "webbrowser" Module')
    import webbrowser

    print('"webbrowser" Module import completed successfully')

    import datetime
    import pickle
    import os.path
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

#
# Ending import section and if error occurs
# It will be consoled with explanation
#

except ImportError as e:
    print("Import of modules has failed with error of: " + e)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


#
# The Speak Function
# Used to make assistant speak something
#

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


#
# The Listen Function
# Used to make assistant listen user and get audio
#

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception " + str(e))

    return said


#
# The Google Authentication Function
# Used to make assistant authenticate user to google
#

def authenticate_google():
    creds = None

    #
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    #
    # If there are no (valid) credentials available, let the user log in.
    #

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        #
        # Save the credentials for the next run
        #

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


#
# The Google Event Handler
# Used to make assistant authenticate user to google
#

def get_events(n, service):
    #
    # Call the Calendar API
    #

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


#
# The Note Function
# Used to make assistant save notes
#

def note(note_string):
    date = "03:17:2020"
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(note_string)

    subprocess.Popen(["notepad.exe", file_name])


#
# The Telegram Function
# Used to make assistant open Telegram Application
#

def open_telegram():
    telegram_application = 'start telegram desktop'
    subprocess.run([telegram_application], shell=True)


def close_telegram():
    subprocess.run('Taskkill /IM Telegram Desktop.exe /F', shell=True)


#
# The Mail Function
# Used to make assistant Mail Application
#

def mail():
    mail_application = "*"
    subprocess.Popen([mail_application])


#
# Creating main function that handles all logic
#

def main():
    #
    # Letting the bot to introduce himself
    #

    speak("Hello, my name is Sarah and I am your voice assistant!")
    speak("What would you like to do with me?")

    #
    # Converting input to string variable and saving as variable
    #
    service = authenticate_google()
    get_events(2, service)
    text = get_audio()

    #
    # There begins our logic
    #

    # Just ordinary speech to speech responses
    if "hello" in text:
        speak("Hello, how are you?")

    if "what is your name" in text:
        speak("My name is Sara")

    if "anime" in text:
        anime_website_url = "https://mover.uz/video/anime/"
        speak("Opening animes in browser")
        webbrowser.open(anime_website_url)

    if "news" in text:
        news_website_url = "https://review.uz"
        speak("Opening fresh news page")
        webbrowser.open(news_website_url)

    # Saving notes with Sara
    NOTE_STR = ["make a note", "write this down", "remember this"]
    for phrase in NOTE_STR:
        if phrase in text:
            speak("What would you like me to save?")
            note_text = get_audio().lower()
            note(note_text)
            speak("I saved your notes")


if __name__ == '__main__':
    main()
