#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import re
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from . import func

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Plugin",]

_FUNCTIONS = {
    "time": func.get_time,
    "eval": func.get_eval,
    "exec": func.get_exec
}

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## Class for Import from Kangaroo
class Plugin(QWidget): # use Widget type
    math_vars = {}
    def __init__(self, parent=None):
        # super(Plugin, self).__init__()
        QWidget.__init__(self)
        
        ## define main variables
        self.parent = parent                # parent window functions
        self.ui = loadUi(base_dir + "UI.ui", self) # include UI file

        self.ui.image.setPixmap(QIcon(base_dir + "icon.png").pixmap(200, 200))
        self.ui.line_search.textChanged.connect(self.search_func)
        self.ui.list_widget.itemDoubleClicked.connect(self.set_func)

        ## run init plugin code
        self.init_ui()

    ## init plugin code
    def init_ui(self):
        self.search_func()
        key, val = self.get_code()
        try:
            self.set_result(str(_FUNCTIONS.get(key)(val)))
        except Exception:
            pass

    def search_func(self, text: str = ""):
        self.ui.list_widget.clear()
        text = text.strip()
        for i in _FUNCTIONS:
            if text in i or not text:
                self.ui.list_widget.addItem(i)

    def set_func(self):
        item = self.ui.list_widget.currentItem()
        self.parent.insert_in_cursor(item.text() + "()")

    def set_icon(self, icon: str):
        self.ui.image.setPixmap(QIcon(base_dir + "icons/" + icon.strip()).pixmap(300, 300))

    def set_result(self, text: str):
        if len(text) > 60:
            self.ui.text_edit.setHtml(text)
        else:
            self.ui.title.setText(text)

    def get_code(self):
        patt = re.compile(r"^([a-zA-Z0-9_]+)\s*\((.*)\)$", re.IGNORECASE | re.ASCII)
        try:
            data = patt.findall(self.parent.text)[0]
            return data[0].lower().strip(), data[1].strip()
        except IndexError:
            return ['', '']

if __name__ == "__main__":
    print(f"Test-{__keyword__}: Ok")
    app = QApplication([])
    win = Plugin()
    win.show()
    exit(app.exec_())
