#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from .item import UIBUi_Item
from UIBox import pkg

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
        self.list_widget.setGridSize(QtCore.QSize(0, 48))
        self.list_widget.setObjectName("list_widget")
        self.gridLayout.addWidget(self.list_widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def add_item(self, icon: str="", title: str="", tag: str="", 
    			hotkey: str="", icon_from_theme: bool=False, 
                null_icon: str='', item_size=(0, 40), icon_provider=False):

        uib_item = UIBUi_Item()

        if not tag.strip():
            uib_item.subtitle.hide()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
        else:
            uib_item.subtitle.show()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

        uib_item.title.setText(title)
        uib_item.subtitle.setText(tag)
        uib_item.hotkey.setText(hotkey)

        list_item = pkg.add_item(self.list_widget, icon=icon, icon_theme=icon_from_theme,
                                 icon_provider=icon_provider, icon_size=(30, 30))

        if list_item.icon().isNull():
            list_item.setIcon(QtGui.QIcon(null_icon))

        list_item.setSizeHint(QtCore.QSize(item_size[0], item_size[1]))
        pkg.set_item_widget(self.list_widget, (list_item, uib_item))
        
        return list_item

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.list_widget.setSortingEnabled(True)
