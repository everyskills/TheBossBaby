#!/usr/bin/python3

import subprocess

def Results(parent):

    data = subprocess.Popen(["apt-cache", "search", str(parent.text)], stdout=subprocess.PIPE)
    query_results = str(data.communicate())\
        .replace("(b\"", "")\
        .replace("(b'", "")\
        .replace("\\n', None)", "")\
        .replace("\\n\", None)", "")\
        .replace("', None)", "")\
        .replace("\", None)", "")

    if not parent.text:
        return [{
            "title" : "Start typing the package name",
            "subtitle" : "Remember, you can use regular expresions For example: apty ^steam",
            "key": ""
        }]

    if query_results == "":
        return [
            {
                "title": "No package " + parent.text + " could be found",
                "subtitle":"Are your repositories updated? (sudo apt update) "
                            "Remember, you can use regular expresions For example: apty ^steam",
                "key": ""
            }
        ]

    packages = query_results.split("\\n")
    n_results = int(len(packages))

    max_results = 20
    max_range = min(max_results, n_results)
    results = []

    for i in range(int(max_range)):
        package = packages[i]
        package_name = package.split(" - ")[0]
        package_description = package.split(" - ")[1]
        results.append(
            {
                "title": package_name,
                "subtitle": package_description
            }
        )

    return results

    # on_enter=RunScriptAction('%s sudo apt install %s' % (
    #     terminal_app, package_name), []),
    # on_alt_enter=CopyToClipboardAction(package_name)