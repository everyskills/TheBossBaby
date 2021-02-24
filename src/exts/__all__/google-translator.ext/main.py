#!/usr/bin/python3

from google_trans_new import google_translator

translator = google_translator()

LANGUAGES = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'bn': 'Bengali',
    'ca': 'Catalan',
    'zh': 'Chinese',
    'zh-cn': 'Chinese (Mandarin/China)',
    'zh-tw': 'Chinese (Mandarin/Taiwan)',
    'zh-yue': 'Chinese (Cantonese)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'en-au': 'English (Australia)',
    'en-uk': 'English (United Kingdom)',
    'en-us': 'English (United States)',
    'eo': 'Esperanto',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'el': 'Greek',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pt-br': 'Portuguese (Brazil)',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr': 'Serbian',
    'sk': 'Slovak',
    'es': 'Spanish',
    'es-es': 'Spanish (Spain)',
    'es-us': 'Spanish (United States)',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'th': 'Thai',
    'tr': 'Turkish',
    'vi': 'Vietnamese',
    'cy': 'Welsh'
}

html = """
<h4>From: {}</h4>
<h4>To: {}</h4>
<center><h3> Text Translated</h3></center>
<h5>{}</h5>
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
