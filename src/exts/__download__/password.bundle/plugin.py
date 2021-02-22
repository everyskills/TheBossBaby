#!/usr/bin/python
# coding=utf-8
import random


def to_html(text):
    with open('template_base.html') as f:
        html_template_base = f.read()

    term = "{}".format(text)
    html = html_template_base.replace("#TERM#", term, 1)
    return html


def results(fields, original_query):
    if fields:
        length = fields['~length']
    else:
        length = 14

    password = str()

    for i in range(int(length)):
        password += chr(random.randint(33, 126))

    return {
        "title": "Copy password to the clipboard.".format(length),
        "run_args": [password],
        "webview_transparent_background": True,
        "html": to_html(password)
    }


def run(password):
    import subprocess
    subprocess.call(['printf "{0}" | pbcopy'.format(password)], shell=True)
