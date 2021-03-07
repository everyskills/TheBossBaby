#!/usr/bin/python3
#-*- coding: utf-8 -*-

"""
simple description what plugin do
"""

import os
from PyQt5.QtWidgets import QWidget
from UIBox.list_item import UIBUi_List

__keyword__ = ""
__author__ = ""
__github__ = ""
__all__ = ["Results",]

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

## NOTE: Before create your plugin, please check if not was taken your keyword
## NOTE: Write all Information in package.json for best quality
## NOTE: try using .png file type when you icon choose if you can, size(35x35)

## Class for Import from UIBox
## don't edit this to another name
class Results(QWidget, UIBUi_List):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)

        ## define main variables
        # parent window functions
        self.parent = parent
        
        self.list_widget.itemClicked.connect(self.get_item_clicked_info)

        self.init_ui()
        
    def init_ui(self):
        self.add_item("", "Hello", "", "")
        self.add_item("", "Hello2", "", "")

    def get_item_clicked_info(self):
        print(self.get_clicked_item())

if __name__ == "__main__":
    print(f"Test-{__keyword__}: Ok")
