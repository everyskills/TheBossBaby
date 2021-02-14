# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(QtWidgets.QWidget):
    def __init__(self, win) -> None:
        super().__init__(win)
        QtWidgets.QWidget.__init__(self)

        self.win = win

        # self.listWidget.itemClicked

        self.resize(538, 148)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 6)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.status = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setText("")
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtWidgets.QListWidget(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("background: transparent;")
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listWidget.setIconSize(QtCore.QSize(50, 50))
        self.listWidget.setMovement(QtWidgets.QListView.Static)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setLayoutMode(QtWidgets.QListView.Batched)
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.listWidget.itemSelectionChanged.connect(self.set_pluging)

        self.setStyleSheet("""
        QListWidget:item {
            border-style: outset;
            border-width: 0px;
            border-radius: 30px;
            border-color: black;
            padding: 5px;
        }

        QListWidget {
            padding-left: 5px;
            padding-right: 5px;
        }
        """)


    def set_pluging(self):
        item = self.listWidget.currentItem()

        self.win.input.setText(item.text() + " ")
        self.set_status(item.text())
        self.win.btn_ext.setIcon(item.icon())
        self.win.input.setFocus()

    def set_status(self, text: str):
        self.status.setText("(" + str(self.win.count) + ") Plugins,  " + str(text
        ) + " - " + str(self.win.exts.get(text).get("json").get("description")))
