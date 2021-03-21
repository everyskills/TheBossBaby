
from UIBox import pkg
import requests

def Results(parent):
    if not parent.text:
        return [{
            "title":'No input',
            "filter": False
        }]

    else:
        items = []
        result = requests.get("https://api.github.com/search/repositories?q=%s&sort=stars&page=1&order=desc&per_page=12" % parent.text ).json()

        for i in result["items"]:
            if parent.text in i["full_name"]:
                items.append({
                    "title": i["full_name"],
                    "subtitle": i["description"],
                    "key": i["html_url"],
                    "func": lambda par,ite: pkg.open_url(ite.key)
                })

        return items[:parent.settings("max-results", 12)]
