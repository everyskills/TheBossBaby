#!/usr/bin/python3

import os

from threading import Thread
from subprocess import call
from glob import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.uic import loadUi
from UIBox import pkg, item

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
apps = {}

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self)

        self.ui.list_widget.itemDoubleClicked.connect(self.run_clicked_app)
        self.ui.list_widget.itemSelectionChanged.connect(self.get_app_info)

        enterAction = QAction("enter", self, shortcut="Return", triggered=self.get_enter_item)
        self.ui.list_widget.addAction(enterAction)

        self.init_ui()

    def init_ui(self):
        self.query_apps()
        self.def_setup()

    def def_setup(self):
        _icon = QIcon(base_dir + "icon.svg")
        self.ui.image.setPixmap(pkg.set_image(_icon, icon=True, size=200))
        self.ui.title.setText("Apps Plugin")
        self.ui.version.setText("1.0.0")

    def get_enter_item(self):
        self.run_clicked_app(self.ui.list_widget.currentItem())
        self.ui.list_widget.setFocus()

    def query_apps(self):
        self.ui.list_widget.clear()
        self.query = self.parent.get_text()
        
        if not apps:
            # Thread(target=self.set_apps, daemon=True).start()
            self.set_apps()
        else:
            self.search_app()

    def search_app(self):
        for k, v in apps.items():
            if ((self.query and k) and 
                (self.query.lower() in k.lower()) and
                self.ui.list_widget.count() <= 10):

                list_item = pkg.add_item(self.ui.list_widget, v["icon"])
                item_widget = pkg.add_item_widget(list_item, item.UIBUi_Item, k, v['comment'])
                pkg.set_item_widget(self.ui.list_widget, item_widget)
                item_widget[1].mouseDoubleClickEvent = (
                    lambda e: self.run_clicked_app(self.list_widget.currentItem()))

        self.ui.status.setText(f"{self.ui.list_widget.count()} of {len(list(apps.keys()))} apps")

    def get_app_info(self):
        item = self.ui.list_widget.currentItem()
        _name = item.listWidget().itemWidget(item).title.text()

        self.short_title(_name)

        ver = apps[_name]["version"]
        com = self.short_text(apps[_name]["comment"])
        exe = self.short_text(apps[_name]["exec"])

        if ver: self.ui.version.setText(ver) 
        else: self.ui.version.clear()
        
        self.ui.lcomment.setText(com)
        self.ui.lcommand.setText(exe)
        self.ui.image.setPixmap(pkg.set_image(item.icon(), size=200))

        try:
            self.ui.lcategories.setText(apps[_name]["categories"].split(";")[0])
        except AttributeError:
            pass

    def run_clicked_app(self, item):
        try:
            item = item.listWidget().itemWidget(item)
            self.get_app_info()
            exe = apps[item.title.text()]["exec"]
            cmd = self.rep(exe, ["%u", "%U", "%F", "%f", "%i", "%I", "%c", "%C"])
            Thread(target=call, kwargs={"shell": True, "args": cmd}, daemon=True).start()
            self.parent.hide_win()
        except AttributeError:
            pass

    def short_title(self, item: str):
        if len(item) <= 20:
            self.ui.title.setText("V" + item)
        else:
            self.ui.title.setText("V" + item[0:21] + "...")

    def short_text(self, text: str):
        if text and len(text) > 30:
            return text[0:30] + "..."
        else:
            return text

    def get_app(self, _file: str, key: str, value: str=""):
        try:
            app = pkg.Import(base_dir + "desktop_parser.py").DesktopParser(_file)
            app.read()
            return app.get(key)
        except KeyError:
            pass

    def rep(self, _str: str, _new: list):
    	for i in _new:
    		_str = _str.replace(i, "")
    	return _str

    def set_apps(self):
        user_path = glob(os.path.expanduser("~/.local/share/applications/*.desktop"))
        user_path.extend(glob("/usr/share/applications/*.desktop"))

        for i in list(dict.fromkeys(user_path)):
            name = self.get_app(i, "Name") or self.get_app(i, "X-GNOME-FullName")
            _icon = self.get_app(i, "Icon")

            if (_icon and os.path.exists(_icon)):
                icon = QIcon(_icon)
            else:
                icon = pkg.get_sys_icon(_icon) if _icon else pkg.icon_path("executable-icon.png", True)

            if (name and self.get_app(i, "Exec")):
                apps.update({name: {
                    "version": self.get_app(i, "Version"), 
                    "comment": self.get_app(i, "Comment"),
                    "exec": self.get_app(i, "Exec"),
                    "categories": self.get_app(i, "categories"),
                    "path": i,
                    "icon": icon}})
