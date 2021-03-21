#!/usr/bin/python3

import os
from UIBox import pkg

def Results(parent):
    data = os.popen("apt-cache search " + parent.text, "r").readlines()
    if not parent.text:
        return [{
            "title" : "Start typing the package name",
            "subtitle" : "Remember, you can use regular expresions For example: apty ^steam",
            "key": ""
        }]

    if not data:
        return [
            {
                "title": "No package " + parent.text + " could be found",
                "highlightable": False,
                "subtitle":"Are your repositories updated? (sudo apt update) "
                            "Remember, you can use regular expresions For example: apty ^steam",
            }
        ]

    results = []
    for i in range(int(parent.settings("max_results", 12))):
        package = data[i]
        package_name = package.split(" - ")[0]
        package_description = package.split(" - ")[1]
        results.append(
            {
                "title": package_name,
                "subtitle": package_description,
                "func": lambda p, i: pkg.run_app(f"{parent.settings('term', 'terminal')} '{parent.settings('cmd', 'sudo apt install -u')} {i.title}'"),
                "ctrl_enter": lambda p, i: parent.text_copy(i.title)
            }
        )

    return results
