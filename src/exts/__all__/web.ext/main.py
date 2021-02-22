# -*- coding: utf-8 -*-

import os

from glob import glob
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebKit import QWebSettings
from PyQt5.uic import loadUi 

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Plugin(QWidget):
    def __init__(self, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)

        self.parent = parent
        self.ui = loadUi(base_dir + "UI.ui", self)
                
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

        self.parent.return_pressed(self.set_url)
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

    def set_url(self):
        text = self.parent.text.strip()
        self.ui.web_view.load(QUrl().fromUserInput(text))

        settings = QWebSettings.globalSettings()
        settings.setDefaultTextEncoding("utf-8")
    
        settings.setAttribute(QWebSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        settings.setAttribute(QWebSettings.WebAudioEnabled, True)
        settings.setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled, True)
        settings.setAttribute(QWebSettings.PluginsEnabled, True)
        settings.setAttribute(QWebSettings.CSSGridLayoutEnabled, True)
        settings.setAttribute(QWebSettings.CSSRegionsEnabled, True)
        settings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebSettings.JavaEnabled, True)
        settings.setAttribute(QWebSettings.PrivateBrowsingEnabled, True)
        settings.setAttribute(QWebSettings.PrintElementBackgrounds, True)
        settings.setAttribute(QWebSettings.NotificationsEnabled, True)
