#!/usr/bin/python3
#-*- coding: utf-8 -*-

def Results(parent):
    List = []

    for i in range(20):
        List.append({
            "title": f"Item Number '{i}'",
            "subtitle": "Test Plugin Items",
            "key": f"num{i}",
            "keep_app_open": True
        })

    return List

def Run(parent, item):
    print("TEXT: ", parent.text)
    print("KEY: ", item.key)
    print("ITEM: ", item.title)

    return Results(parent)
    
def ItemSelected(parent, item):
    print(item.key)

def ItemClicked(parent, item):
    Run(parent, item)
    return Results(parent)