#!/usr/bin/python3

import datetime

def get_time(val):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    format = "<font size='3'>%A</font> %d %B %Y %r"

    dic = {
        "today": today.strftime(format),
        "yesterday": yesterday.strftime(format),
        "tomorrow": tomorrow.strftime(format)
    }

    try:
        return dic[val]
    except KeyError:
        if not val:
            return datetime.datetime.now()
        else:
            return datetime.datetime.now().strftime(val)

def get_eval(val: str):
    return eval(val)

def get_exec(val: str):
    return exec(val)
