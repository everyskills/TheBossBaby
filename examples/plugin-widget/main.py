#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Results", ]

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(35x35)

## Class for Import from UIBox
## don't edit this to another name
class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        # parent window functions:
        # don't edit this to another name
        self.parent = parent

        ## load UI file from a local path
        self.ui = loadUi(base_dir + "UI.ui", self)  # include UI file

        ## run init plugin code
        self.init_ui()

    # don't remove this
    # put your startup code here
    def init_ui(self):
        label = QLabel(f"<font size='7'>Your text:</font> <br>{self.parent.text}")
        label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(label)

    ## Line Input Return Pressed CallBack
    def __run__(self):
        pass

if __name__ == "__main__":
    print(f"Test-{__keyword__}: Ok")