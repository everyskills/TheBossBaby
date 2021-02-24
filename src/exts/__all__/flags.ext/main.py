#!/usr/bin/python3

import os

from glob import glob
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self)

        self.init_ui()

    def init_ui(self):
        dd = self.parent.text.replace("-", "/")
        path = ""
        file = dd

        if len(dd.split(":")) > 1:
            type = dd.split(":")
            if type[0].strip() in ("w", "world"):
                file = type[1].strip()
                path = "World/"

        for rd in sorted(glob(base_dir + f"icons/{path}{file}*.png")):
            _file = os.path.splitext(os.path.split(rd)[1])[0]
            self.ui.image.setPixmap(QIcon(rd).pixmap(QSize(700, 700)))
            self.ui.name.setText(_file)
