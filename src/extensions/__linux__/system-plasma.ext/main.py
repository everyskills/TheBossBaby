import time
from UIBox import pkg

def create_item(parent, name, icon, subtitle, command):
    return {
        "title": name,
        "subtitle": subtitle,
        "icon": icon,
        "icon_theme": True,
        "key": command,
        "filter": False if str(parent.text).isdecimal() else True
    }

def Run(parent, item):
    if str(parent.text).isdecimal():
        parent.post_message(parent.icon, item.title, str(item.subtitle) + f" after {parent.text} Secound", 3000)
        time.sleep(float(parent.text))
        pkg.run_app(item.key)
    else:
        pkg.run_app(item.key)

def Results(parent):
    items_cache = [
        create_item(parent, "Lock", "system-lock-screen", "Lock Screen", "dbus-send --dest=org.freedesktop.ScreenSaver --type=method_call /ScreenSaver org.freedesktop.ScreenSaver.Lock"),
        create_item(parent, 'Logout', 'system-log-out', 'Session logout', 'qdbus org.kde.ksmserver /KSMServer logout 0 3 3'),
        create_item(parent, 'Reboot', 'system-reboot', 'Reboot computer', 'qdbus org.kde.ksmserver /KSMServer logout 0 1 3'),
        create_item(parent, 'Shutdown', 'system-shutdown','Shutdown computer', 'qdbus org.kde.ksmserver /KSMServer logout 0 2 3'),
        create_item(parent, 'Suspend', 'system-suspend', 'Suspend computer', 'dbus-send --system --print-reply --dest="org.freedesktop.login1" /org/freedesktop/login1 org.freedesktop.login1.Manager.Suspend boolean:true'),
        create_item(parent, 'Hibernate', 'system-suspend-hibernate', 'Hibernate computer', 'dbus-send --system --print-reply --dest="org.freedesktop.login1" /org/freedesktop/login1 org.freedesktop.login1.Manager.Hibernate boolean:true'),
    ]

    return items_cache
