#!/usr/bin/python3
#-*- coding: utf-8 -*-

def Results(parent):
    List = []

    for i in range(20):
        List.append({
            "title": f"Item Number '{i}'",
            "subtitle": "Test Plugin Items",
            "icon": "",
            "key": f"num{i}",
            "keep_app_open": True
        })

    return List

def Run(parent, item):
    print("TEXT: ", parent.text)
    print("KEY: ", item.key)
    print("ITEM: ", item.title)

    if item.key == "num1":
        print("You'r number 1")
    else:
        print("You'r in any number")

def ItemSelected(parent, item):
    print(item.key)

def ItemClicked(parent, item):
    Run(parent, item)
    return [{"keep_app_open": True}]