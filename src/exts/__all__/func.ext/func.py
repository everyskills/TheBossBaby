#!/usr/bin/python3

from datetime import datetime

def get_time(val: str):
    if not val:
        return datetime.now()
    else:
        return datetime.now().strftime(val)

def get_eval(val: str):
    return eval(val)

def get_exec(val: str):
    return exec(val) 