#!/usr/bin/python3

import os

from PyQt5 import QtCore, QtGui, QtWidgets
from UIBox import item, pkg

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Ui_List(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(3, 0, 3, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.list_widget = QtWidgets.QListWidget(Form)
        self.list_widget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.list_widget.setStyleSheet("QListWidget {\n"
        "    padding: 0;\n"
        "    margin: 0;\n"
        "    background: transparent;\n"
        "}")

        self.list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_widget.setAutoScroll(False)
        self.list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list_widget.setGridSize(QtCore.QSize(0, 58))
        self.list_widget.setWordWrap(True)
        self.list_widget.setObjectName("list_widget")
        self.gridLayout.addWidget(self.list_widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def get_clicked_item(self):
        try:
            item = self.list_widget.currentItem()
            item_widget = item.listWidget().itemWidget(item)
            dic = {
                "icon": item_widget.image,
                "title": item_widget.title.text(),
                "subtitle": item_widget.desc.text(),
                "hotkey": item_widget.shortcut.text()
            }
            return dic
        except AttributeError:
            return {}

    def add_item(self, icon: str="", title: str="", tag: str="", hotkey: str=""):
        list_item = pkg.add_item(self.list_widget, QtGui.QIcon(icon), icon_size=(30, 30))
        item_widget = pkg.add_item_widget(list_item, item.UIBUi_Item, title, tag, hotkey, item_size=(260, 50))
        pkg.set_item_widget(self.list_widget, item_widget)

        return item_widget[0]

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.list_widget.setSortingEnabled(True)

class UIBIPlugin(QtWidgets.QWidget, Ui_List):
    __type__ = "item"

    def __init__(self, parent=None, func: object=None) -> None:
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        
        self.parent = parent
        self.func = func
        self.result = {}

        enterAction = QtWidgets.QAction(
            "enter",
            self.list_widget,
            shortcut="Return",
            triggered=lambda: self.run_plug_func(self.list_widget.currentItem()))

        self.list_widget.addAction(enterAction)

        self.list_widget.itemClicked.connect(self.run_plug_func)
        self.set_widget_items(self.func)

    def init_ui(self, func):
        self.set_widget_items(func)

    def set_widget_items(self, func):
        self.list_widget.clear()
        if isinstance(func, list) or isinstance(func, tuple):
            for count, item in enumerate(func):
                if (self.parent.methods.text.lower() and 
                    self.parent.methods.text.lower() in item.get("title", "").strip().lower() and
                    count < 10):
            
                    icon = item.get("icon").strip()
                    if not os.path.exists(icon):
                        icon = base_dir + "icons/main/unknow.png"

                    item_widget = self.add_item(icon, item.get("title", ""), item.get("subtitle", ""), "<font size='5'>↩️</font>")
                    self.result.update({id(item_widget): item})
                    count += 1

            self.list_widget.blockSignals(True)
            self.list_widget.setCurrentRow(0)
            self.list_widget.blockSignals(False)

    def run_plug_func(self, item):
        key = self.result.get(id(item))

        if not key.get("func", ""):
            plug = self.parent.exts.get(self.parent.get_kv(self.parent.input.text())[0])
            plug.get("script").Run(self.parent.methods, type("item", (), key))
        else:
            key.get("func")()

        self.parent.hide()
