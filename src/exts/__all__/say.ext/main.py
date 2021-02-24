#!/usr/bin/python3

import pyttsx3

engine = pyttsx3.init() # sapi5
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
	try:
		engine.say(audio)
		engine.runAndWait()
	except RuntimeError:
		pass
	
def Results(parent):
	return {
		"html": f"<h3> Say ' {parent.text} '",
		"title": f"Say '{parent.text}'",
		"open_url_in_browser": True
	}

def Run(parent):
	speak(parent.text)

