#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import re
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from .calculator import evaluate, _FUNCTIONS
from .func import get_help

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Results",]

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Results(QWidget):
    math_vars = {}
    def __init__(self, parent):
        QWidget.__init__(self)
        
        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self) 

        self.ui.image.setPixmap(QIcon(base_dir + "Icon.png").pixmap(300, 300))
        self.ui.line_search.textChanged.connect(self.search_func)
        self.ui.list_widget.itemDoubleClicked.connect(self.set_func)

        self.init_ui()

    def init_ui(self):
        self.search_func()
        
        if not self.parent.text:
            self.title.clear()
            self.text_edit.clear()

        try:
            self.set_vars()
            new_att = re.findall("^(help|rmset)\s*\((.*)\)", self.parent.text)

            if new_att:
                if new_att[0][0] == "help":
                    self.set_result(get_help(new_att[0][1].strip()))

                elif new_att[0][0] == "rmset":
                    split = new_att[0][1].split(",")
                    if len(split) > 0:
                        for i in split:
                            self.math_vars.pop(i.strip(), "")
                    else:
                        self.math_vars.pop(str(new_att[0][1]).strip(), "")
                    
                    self.set_result(f"Removed: {new_att[0][1]}")

            elif self.parent.text.strip() and not self.parent.text.startswith("set"):
                self.set_result(str(evaluate(self.parent.text, self.math_vars)))

        except Exception as math_err:
            self.title.setText(str(math_err))

    def __run__(self):
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
            data = re.findall(r"^set\s*\((.*)\)", txt)[0].strip().split(";")
            for i in data:
                k, v = i.split("=")
                if not k.lower().strip() in "_abcdefghijklmnopqrstuvwxyz" or not evaluate(v.strip()):
                    self.title.setText(f"Error: {k} not support try choose char")
                else:
                    self.text_edit.setHtml(
                        f"{k} = {str(evaluate(v))} \
                        <font color='#38d23a'>Done...</font><br>")
                    self.math_vars.update({k.strip(): evaluate(v.strip())})
                    self.title.clear()
        except IndexError:
            pass

        except ValueError as math_err:
            raise Exception(math_err)
