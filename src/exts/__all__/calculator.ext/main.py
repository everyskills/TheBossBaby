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
from .calculator import evaluate, _FUNCTIONS

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Plugin",]

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Plugin(QWidget):
    math_vars = {}
    def __init__(self, parent):
        QWidget.__init__(self)
        
        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self) 

        self.ui.image.setPixmap(QIcon(base_dir + "icon.png").pixmap(300, 300))
        self.ui.line_search.textChanged.connect(self.search_func)
        self.ui.list_widget.itemDoubleClicked.connect(self.set_func)

        self.parent.return_pressed(self.copy_result)

        self.init_ui()

    def init_ui(self):
        self.search_func()
        
        try:
            self.set_vars()
            if self.parent.text.strip() and not self.parent.text.startswith("set"):
                self.set_result(str(evaluate(self.parent.text, self.math_vars)))
        except Exception as math_err:
            self.title.setText(str(math_err))

    def copy_result(self):
        text = self.ui.title.text().strip()
        self.parent.text_copy(text if text else self.ui.text_edit.toPlainText())

    def set_result(self, text: str=""):
        if len(text) > 60:
            self.ui.text_edit.setHtml(text)
        else:
            self.ui.title.setText(text)

    def search_func(self, text: str=""):
        self.ui.list_widget.clear()
        text = text.strip()

        for i in _FUNCTIONS:
            if text in i or not text:
                self.ui.list_widget.addItem(i)

    def set_func(self):
        item = self.ui.list_widget.currentItem()
        self.parent.insert_in_cursor(item.text() + "(")

    def set_vars(self):
        txt = str(self.parent.text.strip())
        try:
            patt =re.compile(r"set\s*\((.*)\)")
            data = patt.findall(txt)[0].strip().split(";")
            for i in data:
                k, v = i.split("=")
                if not k.lower().strip() in "_abcdefghijklmnopqrstuvwxyz" or not evaluate(v.strip()):
                    self.title.setText(f"Error: {k} not support try choose char")
                else:
                    self.text_edit.insertHtml(
                        f"{k} = {str(evaluate(v))}   \
                            <font color='#38d23a'>Done...</font><br>")
                    self.math_vars.update({k.strip(): evaluate(v.strip())})
        except IndexError:
            pass
        except ValueError as math_err:
            raise Exception(math_err)

if __name__ == "__main__":
    print(f"Test-{__keyword__}: Ok")
    app = QApplication([])
    win = Plugin()
    win.show()
    exit(app.exec_())
