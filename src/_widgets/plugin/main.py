#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Plugin",]

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(35x35)
## NOTE: You can use QMainWindow and QWidget as the main Container

## Class for Import from Kangaroo
class Plugin(QWidget): # use Widget type
    def __init__(self, pkg, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)
        
        ## define main variables
        self.parent = parent                # parent window functions
        self.pkg = pkg                      # some built in functions for use
        self.text = self.parent.get_text()  # text value
        self.ui = loadUi(base_dir + "UI.ui", self) # include UI file

        ## run init plugin code
        self.init_ui()

    ## init plugin code
    def init_ui(self):
        pass

if __name__ == "__main__":
    print(f"Test-{__keyword__}: Ok")
