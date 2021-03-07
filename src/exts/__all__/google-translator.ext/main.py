#!/usr/bin/python3

from google_trans_new import google_translator, LANGUAGES

translator = google_translator()

html = """
<h4>From: {0}</h4>
<h4>To: {1}</h4>
<center><h3> Text Translated</h3></center>
<h5>{2}</h5>
"""

def Results(parent):
	return {
		"html": "<h4> Text: </h4><br><center><h3>%s</h3></center>" % parent.text,
		"title": f"Results for '{parent.text}'",
		"open_url_in_browser": True
	}

def Run(parent):
    fr = parent.by_key("from:", "auto")
    to = parent.by_key("to:", "auto")
    trans = parent.get_text("(to|from)\s*:\s*\w+")

    result = translator.translate(trans, to, fr)

    return {"html": html.format(LANGUAGES.get(fr, "auto"), LANGUAGES.get(to, "auto"), result)}
