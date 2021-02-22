#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def get_info(i):
    print(f"You clicked item {i} with text")

def Plugin(parent):
    List = []

    for i in range(10):
        List.insert(0, {
            "title": f"Item Number '{i}'",
            "subtitle": "Test Plugin Items",
            "icon": "",
            "func": lambda: get_info(i)
        })

    return List
