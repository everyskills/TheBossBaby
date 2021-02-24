#!/usr/bin/python3

# google_url = 'https://www.google.com/search?q={}&num={}&hl={}'

def Results(parent):
	return {
        "html": "",
		"title": f"Search for '{parent.text}'",
		"open_url_in_browser": False
	}

def Run(parent):
	return {"html": f"https://www.google.com/search?q={parent.text}"}
    # return {
        # "html": google_url.format(parent.text, 1+1, "en")
    # }
