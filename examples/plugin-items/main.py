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

## Function for Import from UIBox
## don't edit this to another name
def Results(parent):
    List = []

    for i in range(10):
        List.append({
            "icon": "",
            "title": f"Item Number '{i}'",
            "subtitle": "Test Plugin Items",
            "key": f"num{i}"
        })

    return List

## will run this function when the line input was clicked
def Run(parent):
    """ 
    :param parent: main window events and simple methods
    :param item: return clicked item content
    """
    pass

## will run this function when the item was selected
def ItemSelected(parnet, item):
    pass

## will run this function when the item was clicked
def ItemClicked(parent, item):
    pass
