#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(35x35)


def Plugin(parent):
    ## [(title, subtitle, func), ...]
    return [
        {
            "title": "Item number 1",
            "subtitle": "Test Plugin Items",
            "icon": "",
            "func": lambda: print(f"You clicked item 1 with text: {parent.text}")
        },

        {
            "title": "Item number 2",
            "subtitle": "Test Plugin Items 2",
            "icon": "",
            "func": lambda: print(f"You clicked item 2 with text: {parent.text}")
        }
    ]
