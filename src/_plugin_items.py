#!/usr/bin/python3

import os
import json

from glob import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from UIBox import item, pkg

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UIBUi_Item(QtWidgets.QWidget):
    def __init__(self):
        super(UIBUi_Item, self).__init__()

        self.setObjectName("Form")
        self.setMouseTracking(True)

        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, -2, 0)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)

        self.title = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title.setFont(font)
        self.title.setText("")
        self.title.setObjectName("title")
        # self.gridLayout.addWidget(self.title, 0, 1, 2, 1)
        self.desc = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.desc.setFont(font)
        self.desc.setText("")
        self.desc.setObjectName("desc")
        self.gridLayout.addWidget(self.desc, 1, 1, 1, 1)
        self.image = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setText("")
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 2, 1)
        self.shortcut = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shortcut.sizePolicy().hasHeightForWidth())
        self.shortcut.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.shortcut.setFont(font)
        self.shortcut.setText("")
        self.shortcut.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.shortcut.setObjectName("shortcut")
        self.gridLayout.addWidget(self.shortcut, 0, 2, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setStyleSheet("""
        /* color: #898b8c; */
        #desc {
            padding-left: 3px;
            font-size: 11px;
            color: #929a90;
        }
        #title {
            padding-left: 2px;
        }
        """)

class Ui_List(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.list_widget = QtWidgets.QListWidget(Form)
        self.list_widget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.list_widget.setStyleSheet("QListWidget {\n"
        "    padding: 0;\n"
        "    margin: 0;\n"
        "    background: transparent;\n"
        "    padding-left: 5px;"
        "    padding-right: 5px;"
        "}")

        self.list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.list_widget.setAutoScroll(True)
        self.list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list_widget.setGridSize(QtCore.QSize(0, 50))
        self.list_widget.setWordWrap(False)
        self.list_widget.setObjectName("list_widget")
        self.gridLayout.addWidget(self.list_widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def add_item(self, icon: str="", title: str="", tag: str="", hotkey: str=""):
        uib_item = item.UIBUi_Item()

        if not tag.strip():
            uib_item.shortcut.hide()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
        else:
            uib_item.shortcut.show()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

        list_item = pkg.add_item(self.list_widget, QtGui.QIcon(icon), icon_size=(30, 30))

        item_widget = pkg.add_item_widget(list_item, uib_item, title, tag, hotkey, item_size=(260, 43))

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
        self.list_widget.itemClicked.connect(lambda: self.item_event(False))
        self.list_widget.itemSelectionChanged.connect(lambda: self.item_event(True))
        self.set_widget_items(self.func)

    def init_ui(self, func):
        self.set_widget_items(func)

    def set_widget_items(self, func):
        self.list_widget.clear()
        self.result.clear()
        
        ret_color = (
            self.parent.methods.light_color
            if self.parent.methods.style == 'dark' 
            else self.parent.methods.dark_color)

        if isinstance(func, list) or isinstance(func, tuple):
            for count, item in enumerate(func):
                if (self.parent.methods.text.lower() in item.get("title", "").strip().lower()): # and count < 11

                    def_icon = self.parent.get_running_plugin
                    icon = item.get("icon", def_icon.get("icon")).strip()
                    item_widget = self.add_item(icon, item.get("title", ""), item.get(
                        "subtitle", ""), "<font size='5' color='%s'>⏎</font>" % ret_color)

                    self.result.update({id(item_widget): item})
                    count += 1

            self.list_widget.blockSignals(True)
            self.list_widget.setCurrentRow(0)
            self.list_widget.blockSignals(False)

    def run_plug_func(self, item):
        data = self.result.get(id(item))

        try:
            if not data.get("func", ""):
                plug = self.parent.exts.get(self.parent.get_kv(self.parent.input.text())[0])
                pp = plug.get("script").Run(self.parent.methods, type("item", (), data))
            else:
                pp = data.get("func")()

            if not data.get("keep_app_open", False):
                self.parent.hide()
            
            if pp:
                self.set_widget_items(pp)
        except Exception as err:
            # print("Error-item-return-pressed-run: ", str(err))
            pass

    def item_event(self, selected: bool=False):
        data = type("item", (), self.result.get(id(self.list_widget.currentItem())))
        try:
            if not selected:
                pp = self.parent.exts.get(self.parent.running).get("script").ItemClicked(self.parent.methods, data)
                if not pp or not data.keep_app_open == True:
                    self.parent.hide()
            else:
                pp = self.parent.exts.get(self.parent.running).get("script").ItemSelected(self.parent.methods, data)

            if pp:
                self.set_widget_items(pp)
        except Exception as err:
            # print("Error-item-clicked-selected: ", str(err))
            pass
