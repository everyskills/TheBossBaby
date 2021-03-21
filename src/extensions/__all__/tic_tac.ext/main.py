#!/usr/bin/python3

import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def Results(parent):
	return {
		"html": base_dir + "index.html",
		"items": [{"title": "Tic Tac Game is running."}],
		"open_url_in_browser": True
	}


