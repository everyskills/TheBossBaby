#!/usr/bin/python3

from google_trans_new import google_translator, LANGUAGES

translator = google_translator()

def Results(parent):
    keys = {
        "results": "",
        "text": parent.get_text_index(1)
    }
    return {"html": parent.include_file("index.html"), "jinja": True, "keywords": keys}

def Run(parent):
    split = parent.text.split()[0].strip().lower()
    text = parent.get_text_index(1)

    fr = "en"
    to = split

    if len(split.split(":")) > 1:
        fr = split.split(":")[0]
        to = split.split(":")[1]

    return {"keywords":  {
        "from": LANGUAGES.get(fr, "UnKnow"),
        "to": LANGUAGES.get(to, "UnKnow"),
        "results": translator.translate(text, to, fr),
        "text": text
    }}
