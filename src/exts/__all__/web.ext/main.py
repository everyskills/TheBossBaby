# -*- coding: utf-8 -*-

import os

from UIBox.web import get_settings
from glob import glob
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi 

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self)

        get_settings()

        self.ListAutoComp = [
            "https://www.",
            "http://www.",
            "ftp://",
            "tcp://",
            "file:///",
            "/"]

        self.ListAutoComp.extend(glob(f"{os.path.expanduser(os.path.expandvars(self.parent.text))}*.html"))

        self.ui.web_view.loadProgress.connect(self.load_progress_bar)
        
        self.frame = self.ui.web_view.page().mainFrame()

        self.ui.web_view.load(QUrl("about:blank"))
        self.parent.set_auto_complete(self.ListAutoComp)

        self.init_ui()

    def init_ui(self):
        if not os.path.exists(self.parent.text):
            self.ui.web_view.setHtml(self.parent.text)

    def load_progress_bar(self, value: int):
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.setValue(0)

    def __run__(self):
        text = self.parent.text.strip()
        self.ui.web_view.load(QUrl().fromUserInput(text))
