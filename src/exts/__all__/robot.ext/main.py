#!/usr/bin/python3

import pyttsx3

engine = pyttsx3.init() # sapi5
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Plugin(parent):
	return {
		"html": f"<h3> Say ' {parent.text} '",
		"title": f"Say '{parent.text}'",
		"open_url_in_browser": True
	}

def run(parent):
	speak(parent.text)