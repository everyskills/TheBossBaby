#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Item(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Item, self).__init__()

        self.LClick, self.LHover, self.LDClick = [], [], []

        self.setObjectName("Form")
        self.setMouseTracking(True)

        # self.resize(321, 54)
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
            padding-top: 4px;
            font-size: 11px;
            color: #929a90;
        }
        #title {
            padding-left: 2px;
        }
        """)
    
    def clicked(self, call):
        self.LClick.append(call)
    
    def hoverd(self, call):
        self.LHover.append(call)

    def doubl_clicked(self, call):
        self.LDClick.append(call)

    def mouseMoveEvent(self, event) -> None:
        for func in self.LHover: func(self)
        
    def mouseDoubleClickEvent(self, event) -> None:
        for func in self.LDClick: func(self)

    # def mousePressEvent(self, event) -> None:
    #     for func in self.LClick: func(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
