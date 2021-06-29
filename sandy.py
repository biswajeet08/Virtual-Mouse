import os
import sys
import psutil
# from selenium import webdriver
import time
import speech_recognition as sr
import pyttsx3
# import pywhatkit
# import datetime
# import requests
import re
from mousecontrol import VirtualMouse

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    print(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()

    except Exception as e:
        print(e)


def sorry():
    talk("sorry Vicky, didn't get you. Can you come again?")
    ok = listen()
    return ok


def mouse():
    virtual_mouse = VirtualMouse()
    virtual_mouse.mouse_control()


def do_Sandy():
    to_do_list = ['search', 'time', 'message', 'shutdown', 'options', 'date', 'open application', 'close application',
                  'weather report']
    matching_words = ['activate virtual mouse', 'quit', 'logoff']
    ans = None
    while ans == None:
        talk('what do you want me to do?')
        ans = listen()
    for words in matching_words:
        if re.search(fr'\b{words}\b', ans) != None:
            ans = words
        else:
            ans = None

    while ans not in matching_words:
        ans = sorry()
        for words in matching_words:
            if re.search(fr'\b{words}\b', ans) != None:
                ans = words
            else:
                ans = None

    if ans == matching_words[0]:
        mouse()


def hi_Sandy():
    talk('hi Vicky')
    var = listen()

    if not var:
        hi_Sandy()
    else:
        do_Sandy()


if __name__ == '__main__':
    hi_Sandy()
