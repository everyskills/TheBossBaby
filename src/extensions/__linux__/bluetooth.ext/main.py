#!/usr/bin/python3

from UIBox import pkg

def Results(parent):
    items = []
    results = pkg.get_cmd_output("bluetoothctl", "devices").readlines()

    for i in results:
        phone = i.split(maxsplit=2)
        items.append({
            "title": phone[2],
            "subtitle": "MAC: " + phone[1],
            "key": phone[1],
            "keep_app_open": True,
            "search_from_index": 2
        })

    return items

def Run(parent, item):
    command = "connect" if parent.key == "btc" else "disconnect"
    action = pkg.get_cmd_output("bluetoothctl", command, item.key).readlines()
    parent.post_message(parent.icon, item.title, action[0] + "\n" + action[2])

def ItemClicked(parent, item):
    Run(parent, item)
