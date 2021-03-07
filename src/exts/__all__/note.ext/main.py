#!/usr/bin/python3

import os
from PyQt5.QtCore import QObject, pyqtSlot

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

note_file = base_dir + ".notes.txt"

html = u"""
	<!DOCTYPE html>
	<html>
	<head>
	
	<style>
	body {
		background-image: url({{image}});
		background-size: 128px;
		font-family: "Helvetica Neue";
		line-height: 1.3;
		margin: 0;
	}
	
	html, body {
		height: 100%;
	}
	
	#field {
		box-sizing: border-box;
		padding: 20px;
		padding-bottom: 50px;
		min-height: 100%;
		outline: none;
	}
	
	#field:empty:before {
		content: "Type some text, or say 'clipboard'";
		opacity: 0.5;
	}
	
	#save {
		background-color: white;
		border-top: 0.5px solid rgba(0,0,0,0.75);
		padding: 10px;
		text-align: center;
		text-transform: uppercase;
		color: rgba(0,0,0,0.5);
		font-weight: bold;
		font-size: small;
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		cursor: pointer;
	}
	</style>
	</head>
	<body>
	
	<div id='field' contentEditable><!--CONTENT--></div>
	
	<div id='save' onClick="backend.save_text(output())">
		Save note
	</div>
	
	<script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
	<script>
		function output() {
			return document.getElementById("field").innerHTML;
		}
		var backend = null;
		new QWebChannel(qt.webChannelTransport, function(channel) {
			backend = channel.objects.note;
		});
	</script>

	</body>
	</html>
	"""

class MyApp(QObject):
    def __init__(self) -> None:
        super(MyApp, self).__init__()

    ################## simple function for call python in javascript
    @pyqtSlot(str) # type of arguments/options
    def save_text(self, text: str):
        """ get name from <h1> and print it from python code"""
        with open(note_file, "w") as _fw:
        	_fw.write(str(text))
        	_fw.close()

def Results(parent):

	content = parent.text
	title = "Create a Note"

	if parent.text == 'clipboard':
		content = parent.text_paste(True)
		title = "Copyed Clipboard to note"

	elif parent.text == 'note':
		with open(note_file) as gr:
			content = gr.read()
		title = "Geting th note from history"

	return {
		"html": html.replace("<!--CONTENT-->", content.replace("\n", "<br/>")).replace("{{image}}", "file://" + base_dir + "background.png"),
        "open_links_in_browser": True,
        "object": {"note": MyApp()},
		"items": [
			{"key": "secound", "icon": "", "title": title}
		]
	}

def Run(parent):
	print("Your text: ", parent.text)
	with open(note_file) as cp:
		parent.text_copy(cp.read())

def ItemClicked(parent, item):
	pass

def ItemSelected(parent, item):
	pass
