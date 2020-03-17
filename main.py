"""
APP: SARA - VOICE ASSISTANT
AUTHOR: Genemator Sakhib
VERSION: 0.0.1 alpha
STATUS: Rolling
"""

#
# Starting import process here
#

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

#
# Ending import section and if error occurs
# It will be consoled with explanation
#

except ImportError as e:
    print("Import of modules has failed with error of: " + e)


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
