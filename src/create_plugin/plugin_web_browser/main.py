# -*- coding: utf-8 -*-

import os

from UIBox import web
from PyQt5.QtCore import QObject, QUrl, pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi 

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(35x35)

class MyApp(QObject):
    def __init__(self, parent: object = None) -> None:
        super().__init__(parent)

    ################## simple function for call python in javascript
    @pyqtSlot(str)  # type of arguments/options
    def get_name(self, text: str):
        """ get name from <h1> and print it from python code"""
        print("You'r using: ", text.strip(), " App")


## Class for Import from UIBox
## don't edit this to another name
class Results(QWidget): # You can use QMainWindow or QWidget
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        ## define main variables
        self.parent = parent                       # parent window functions
        self.ui = loadUi(base_dir + "UI.ui", self) # load ui file to class

        web.get_settings()

        self.frame = self.web_view.page().mainFrame()
        self.frame.addToJavaScriptWindowObject("uibox", MyApp(self)) # share MyApp class with js code
        self.document = self.frame.documentElement()
        
        self.ui.web_view.loadProgress.connect(self.load_progress_bar) # load progress bar
        self.parent.return_pressed(self.set_url) # open url on QLineEdit Return Pressed
        
        self.ui.web_view.load(QUrl("about:blank")) # set default url

        self.parent.set_auto_complete([]) # auto compelete

    def init_ui(self):
        pass
    
    ############### Load Progress bar change value
    def load_progress_bar(self, value: int):
        self.progressBar.setValue(value)
        if value == 100:
            self.progressBar.setValue(0)

    ############### Set Url and Web Setting
    def set_url(self):
        text = self.text.strip()
        self.ui.web_view.load(QUrl().fromUserInput(text))

    def run_js(self, script: str):
        self.document.evaluateJavaScript(script)

    ## Line Input Return Pressed CallBack
    def __run__(self):
        pass
