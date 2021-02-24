#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def get_info(i):
    print(f"You clicked item {i} with text")

def Results(parent):
    List = []

    for i in range(20):
        List.append({
            "title": f"Item Number '{i}'",
            "subtitle": "Test Plugin Items",
            "icon": "",
            "key": f"num{i}"
        })

    return List

def Run(parent, item):
    print("TEXT: ", parent.text)
    print("KEY: ", item.key)
    if item.key == "num1":
        print("You'r number 1")
    else:
        print("You'r in any number")