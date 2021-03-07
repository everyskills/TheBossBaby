#!/usr/bin/python3

import os
import sqlite3
import phonenumbers as ph
from phonenumbers import carrier

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

con = sqlite3.connect(base_dir + "database.db")
cur = con.cursor()

keys = {}

script = """
CREATE TABLE Contact (
	id		INTEGER PRIMARY KEY UNIQUE,
	name    TEXT UNIQUE,
	phone   INTEGER UNIQUE
);
"""

try:
  cur.execute(script)
  con.commit()
except sqlite3.OperationalError as err:
    pass

def get_ph_ty(ty: object, phone: object):
    try:
        number = f"+{ty} {phone}"
        service_num = ph.parse(number, "RO")
        return str(carrier.name_for_number(service_num, "en"))
    except ph.phonenumberutil.NumberParseException:
        pass

def add_contact(name, phone):
    try:
        cur.execute(f"INSERT INTO Contact (name, phone) VALUES ('{name}', {int(phone)}) ")
        con.commit()
    except sqlite3.IntegrityError as sqerr:
        if "phone" in str(sqerr):
            keys['error'] = "This Phone is already Exists"
        elif "name" in str(sqerr):
            keys['error'] = "This Name is already Exists"

def delete_contact(query):
    where = f"name='{query}'" if not query.isdigit() else f"phone={int(query)}"
    cur.execute(f"DELETE FROM Contact WHERE {where}")
    con.commit()

def update_contact(old, new):
    who = f"name='{new}'" if not new.isdigit() else f"phone={int(new)}"
    where = f"name='{old}'" if not old.isdigit() else f"phone={int(old)}"
    cur.execute(f"UPDATE Contact SET {who} WHERE {where}")
    con.commit()

def Results(parent):
    """ main function for start plugin from kangaroo """

    items = []
    keys.update({
        'color' : 'black' if not parent.style == 'dark' else 'white',
        'bg' : parent.dark_color if parent.style == 'dark' else parent.light_color
    })

    if parent.text.startswith("+"):
        pt = get_ph_ty(parent.text[1:4], parent.text[4:])
        keys.update({
            'name' : pt,
            'phone' : f"{parent.text[0]}({parent.text[1:4]}) {parent.text[4:]}",
            'ph_ty' : pt
        })

    elif parent.text:
        # _or = f"OR phone LIKE '{int(parent.text)}%'" if parent.text.isalnum() else ""
        data = cur.execute(f"SELECT * FROM Contact WHERE name LIKE '{parent.text}%' OR phone LIKE '{parent.text}%'").fetchall()
        for i in data:
            keys.update({
                'name' : i[1],
                'phone' : i[2],
                'ph_ty' : get_ph_ty("967", keys.get("phone"))
            })

            items.append({"key": i[2], "title": i[1],
                          "icon": base_dir + "personal.png",
                          "subtitle": i[2]})

    else:
        keys.update({
            'name' : "You",
            'phone' : "000000000",
            'ph_ty' : "Company"
        })

    return {
        "html": base_dir + "index.html",
        "jinja": True,
        "keywords": keys,
        "open_url_in_browser": True,
        "items": items if items else [{"title": "no match found for '%s' in contact" % parent.text}]
    }
    
def Run(parent):
    new_name = parent.by_key("new", "")
    del_name = parent.by_key("del", "")
    up_old_name = parent.by_key("up", "")
    up_new_name = parent.by_key("to", "")
    
    if new_name:
        add_contact(new_name, parent.by_key(new_name))
    elif del_name:
        delete_contact(del_name)
    elif up_old_name:
        update_contact(up_old_name, up_new_name)

def ItemSelected(parent, item):
    keys.update({
        "name": item.title,
        "phone": item.key,
        "ph_ty": get_ph_ty("967", item.key)
    })

    return {"keywords": keys}

def ItemClicked(parent, item):
    parent.text_copy(str(item.key))
