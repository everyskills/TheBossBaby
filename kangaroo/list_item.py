# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from kangaroo import item, pkg

class KUi_List(object):
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
                "tag": item_widget.desc.text(),
                "hotkey": item_widget.shortcut.text()
            }
            return dic
        except AttributeError:
            return {}

    def add_item(self, icon: str="", title: str="", tag: str="", hotkey: str=""):
        list_item = pkg.add_item(self.list_widget, QtGui.QIcon(icon), icon_size=(30, 30))
        item_widget = pkg.add_item_widget(list_item, item.KUi_Item, title, tag, hotkey, item_size=(260, 50))
        pkg.set_item_widget(self.list_widget, item_widget)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.list_widget.setSortingEnabled(True)