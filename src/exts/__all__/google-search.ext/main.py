#!/usr/bin/python3

# google_url = 'https://www.google.com/search?q={}&num={}&hl={}'

def Results(parent):
	return {
        "html": "",
		"title": f"Search for '{parent.text}'",
		"open_links_in_browser": False,
		"items": [
			{"title": f"Search for '{parent.text}' in Google.", "key": "1"},
		]
	}

def Run(parent):
	return {"html": f"https://www.google.com/search?q={parent.text}"}

def ItemClicked(parent, item):
	# print(item.title)
	pass

def ItemSelected(parent, item):
	# print(item.title)
	pass