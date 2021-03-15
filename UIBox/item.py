#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.gridLayout.addWidget(self.title, 0, 1, 1, 1)
        self.subtitle = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.subtitle.setFont(font)
        self.subtitle.setText("")
        self.subtitle.setObjectName("subtitle")
        self.gridLayout.addWidget(self.subtitle, 1, 1, 1, 1)

        self.subtitle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.subtitle.setAlignment(QtCore.Qt.AlignLeft)

        self.image = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setText("")
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 2, 1)
        self.hotkey = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hotkey.sizePolicy().hasHeightForWidth())
        self.hotkey.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.hotkey.setFont(font)
        self.hotkey.setText("")
        self.hotkey.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.hotkey.setObjectName("hotkey")
        self.gridLayout.addWidget(self.hotkey, 0, 2, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setStyleSheet("""
        #subtitle {
            padding-left: 3px;
            font-size: 11px;
            color: #929a90;
        }
        #hotkey {
            padding-left: 5px;
        }

        #title {padding-left: 2px}
        """)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
