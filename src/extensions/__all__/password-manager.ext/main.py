import os
import json

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

value = ""
password = ""

def save_data(parent, val, passw):
    global value, password

    data = json.load(open(base_dir + "passwords.json"))
    data.update({
        val: {
            "value": val,
            "pass": passw,
            "type": ""
    }})

    with open(base_dir + "passwords.json", "w") as _fw:
        _fw.write(str(json.dumps(data, indent=4)))

    parent.text_clear()
    value = ""
    password = ""
    
    parent.set_key("gpss")

def remove_data(parent, item):
    data = json.load(open(base_dir + "passwords.json"))
    data.pop(item.key)
    with open(base_dir + "passwords.json", "w") as _fw:
        _fw.write(str(json.dumps(data, indent=4)))
    return Results(parent)

def Results(parent):
    data = json.load(open(base_dir + "passwords.json"))
    items = []

    if parent.key == "spss":
        if not value:
            return [{
                "title": "Example: example@gmail.com", 
                "subtitle": "enter to write password", 
                "highlightable": False, 
                "filter": False,
                "keep_app_open": True
            }]

        else:
            return [{
                "title": f"Write Password for '{value}'",
                "subtitle": "enter for save changed",
                "func": lambda p, i: save_data(p, value, parent.text),
                "keep_app_open": True
            }]
    
    else:
        for k, v in data.items():
            items.append({
            	"icon": parent.get_status_icon("log-out"),
                "title": k,
                "subtitle": "enter for choose what action to do" if not parent.key == "rpss" else "enter for remove it",
                "key": v.get("pass", ""),
                "keep_app_open": True
            })
        return items

def Run(parent, item):
    global value, password

    if parent.key == "spss":
        if not password:
            value = parent.text
            parent.text_clear()
        else:
            password = parent.text
    
    elif parent.key == "rpss":
        remove_data(parent, item)

    else:
        parent.text_clear()
        return [
        {
        	"icon": parent.include_file("images/copy.png"),
            "title": "Copy to Clipboard",
            "subtitle": f"entery for copy '{item.title}' password to clipboard",
            "key": item.key,
            "func": lambda p, i: parent.text_copy(i.key),
            "filter": False
        },
        {
            "title": "Paste Password",
            "subtitle": f"enter for paste '{item.title}' password",
            "key": item.key,
            "filter": False
        },
        {
        	"icon": parent.include_file("images/remove.svg"),
            "title": "Remove It",
            "subtitle": f"enter for remove '{item.title}'",
            "key": item.title,
            "func": lambda p, i: remove_data(p, i),
            "filter": False,
            "keep_app_open": True
        },
        {
        	"icon": parent.include_file("images/show.svg"),
            "title": "Show Password",
            "subtitle": f"enter show '{item.title}' password",
            "key": item.key,
            "func": lambda p, i: parent.larg_text(i.key),
            "filter": False
        }][::-1]
