#!/usr/bin/python3

import os

from threading import Thread
from subprocess import call
from glob import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
apps = {}

class Plugin(QWidget):
    def __init__(self, pkg, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)

        self.pkg = pkg
        self.parent = parent
        self.ui = loadUi(base_dir + "apps.ui", self)

        # self.input.textChanged.connect(lambda: self.query_apps())
        self.ui.list_widget.itemClicked.connect(self.run_clicked_app)
        self.ui.list_widget.itemSelectionChanged.connect(self.get_app_info)

        # self.parent.return_pressed(self.check_command)

        enterAction = QAction("enter", self, shortcut="Return", triggered=self.get_enter_item)
        self.ui.list_widget.addAction(enterAction)

        self.query_apps()
        self.def_setup()

    # def check_command(self):
        # if self.parent.get_text() in ("update", "refresh"):
        #     self.set_apps()
        # elif self.parent.get_text() in ("clear-apps", "clean-apps"):
        #     apps.clear()

    def def_setup(self):
        _icon = QIcon(base_dir + "icon.svg")
        self.ui.image.setPixmap(self.pkg.set_image(_icon, icon=True, size=200))
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

                frame = self.pkg.Import(base_dir + "item.py").Ui_Item
                item = self.pkg.add_item_widget(self.ui.list_widget, frame, v["icon"], k, v['comment'])
                
                self.pkg.set_item_widget(self.ui.list_widget, item)

        self.ui.status.setText(f"{self.ui.list_widget.count()} of {len(list(apps.keys()))} apps")

    def get_app_info(self):
        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        _name = litem.title.text()

        self.short_title(_name)

        ver = apps[_name]["version"]
        com = self.short_text(apps[_name]["comment"])
        exe = self.short_text(apps[_name]["exec"])

        if ver: self.ui.version.setText(ver) 
        else: self.ui.version.clear()
        
        self.ui.lcomment.setText(com)
        self.ui.lcommand.setText(exe)
        self.ui.image.setPixmap(self.pkg.set_image(item.icon(), size=200))

        try:
            self.ui.lcategories.setText(apps[_name]["categories"].split(";")[0])
        except AttributeError:
            pass

    def run_clicked_app(self, item):
        item = item.listWidget().itemWidget(item)

        self.get_app_info()
        exe = apps[item.title.text()]["exec"]
        cmd = self.rep(exe, ["%u", "%U", "%F", "%f", "%i", "%I", "%c", "%C"])
        Thread(target=call, kwargs={"shell": True, "args": cmd}, daemon=True).start()
        self.parent.hide_win()

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
            app = self.pkg.Import(base_dir + "desktop_parser.py").DesktopParser(_file)
            app.read()
            return app.get(key)
        except KeyError:
            pass

    def rep(self, _str: str, _new: list):
    	for i in _new:
    		_str = _str.replace(i, "")
    	return _str

    def set_apps(self):
        paths = []
        user_path = glob(os.path.expanduser("~/.local/share/applications/*.desktop"))
        root_path = glob("/usr/share/applications/*.desktop")
        paths.extend(user_path)
        paths.extend(root_path)

        for i in list(dict.fromkeys(paths)):
            name = self.get_app(i, "Name") or self.get_app(i, "X-GNOME-FullName")
            _icon = self.get_app(i, "Icon")

            if (_icon and os.path.exists(_icon)):
                icon = QIcon(_icon)
            else:
                icon = self.pkg.get_sys_icon(_icon) if _icon else self.pkg.icon_path("executable-icon.png", True)

            if (name and self.get_app(i, "Exec")):
                apps.update({name: {
                    "version": self.get_app(i, "Version"), 
                    "comment": self.get_app(i, "Comment"),
                    "exec": self.get_app(i, "Exec"),
                    "categories": self.get_app(i, "categories"),
                    "path": i,
                    "icon": icon}})
