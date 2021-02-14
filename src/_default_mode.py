#!/usr/bin/python3

import os
import _pkg

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget
from _item import Ui_Item
from ui.default_mode_ui import Ui_Form

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class DefaultModeItems(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(DefaultModeItems, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        
        self.parent = parent
        self.count = 0
        self.exts = {} # {index: "key"}

        self.list_widget.itemClicked.connect(self.get_current_item)
        self.enter = QAction("Enter", self.list_widget,
                            shortcut="Return",
                            triggered=self.get_current_item)
        
        # self.list_widget.addAction(self.enter)
        
        # keys = []
        # keys.extend(list(self.parent.exts.keys()))
        # keys.extend(list(self.parent.user_cmd.keys()))

        keys = list(self.parent.exts.keys())
        for D in keys:
            inp = self.parent.input.text().strip()
            
            if D in keys:
                self.list_widget.addAction(self.enter)

                data = self.parent.exts.get(D.strip())
                title = data.get("json").get("name")
                tag = data.get("json").get(
                    "description", 
                    "no description").strip()

                icon = data.get("icon")
            
            # if D in list(self.parent.user_cmd.keys()):
                # data = self.parent.user_cmd.get(D.strip())
                # title = data.get("name")
                # tag = data.get("tag")
                # icon = data.get("icon")

            if inp.lower() in title.lower() and self.count != 10:
                list_item = _pkg.add_item(
                    self.list_widget,
                    QIcon(icon),
                    icon_size=(30, 30))

                item = _pkg.add_item_widget(
                    list_item,
                    Ui_Item,
                    title,
                    tag,
                    D,
                    item_size=(260, 50))
                
                _pkg.set_item_widget(self.list_widget, item)
                self.exts.update({self.count: D})
                self.count += 1

            else:
                self.list_widget.removeAction(self.enter)

    def get_current_item(self):
        item = self.list_widget.currentItem()
        _key = item.listWidget().itemWidget(item).shortcut.text()
        self.parent.input.setText(_key + " ")
        self.parent.input.setFocus()










        # for D in list(self.parent.exts.keys()):
        #     data = self.parent.exts.get(D.strip())
        #     inp = self.parent.input.text().strip()
        #     title = data.get("json").get("name")
            
        #     if D in list(self.parent.exts.keys()):
        #         title = 
        #         tag = 
        #         icon =
        #         key = 
                 
        #     if inp.lower() in title.lower() and self.count != 10:
        #         self.list_widget.addAction(self.enter)

        #         list_item = _pkg.add_item(
        #             self.list_widget,
        #             QIcon(data.get("icon")),
        #             icon_size=(30, 30))

        #         item = _pkg.add_item_widget(
        #             list_item,
        #             Ui_Item,
        #             title,
        #             data.get("json").get("description", "no description").strip(),
        #             D,
        #             item_size=(260, 50))
                
        #         _pkg.set_item_widget(self.list_widget, item)
        #         self.exts.update({self.count: D})
        #         self.count += 1
        #     else:
        #         self.list_widget.removeAction(self.enter)
