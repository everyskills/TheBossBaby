# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.resize(560, 480)
        
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.UIB_frame = QtWidgets.QFrame(Form)
        self.UIB_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.UIB_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.UIB_frame.setObjectName("UIB_frame")
        
        self.gridLayout_7 = QtWidgets.QGridLayout(self.UIB_frame)
        self.gridLayout_7.setContentsMargins(0, 4, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.UIB_input_frame = QtWidgets.QFrame(self.UIB_frame)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UIB_input_frame.sizePolicy().hasHeightForWidth())
        self.UIB_input_frame.setSizePolicy(sizePolicy)
        self.UIB_input_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.UIB_input_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.UIB_input_frame.setObjectName("UIB_input_frame")        
        self.gridLayout_2 = QtWidgets.QGridLayout(self.UIB_input_frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.btn_ext = QtWidgets.QToolButton(self.UIB_input_frame)
        # self.btn_ext.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ext.setText("")
        self.btn_ext.setStyleSheet("padding-right: 5px;")
        self.btn_ext.setIconSize(QtCore.QSize(35, 35))
        self.btn_ext.setAutoRaise(True)
        self.btn_ext.setObjectName("btn_ext")
        self.gridLayout_2.addWidget(self.btn_ext, 0, 2, 1, 1)
        
        self.btn_setting = QtWidgets.QToolButton(self.UIB_input_frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_setting.setFont(font)
        self.btn_setting.setStyleSheet("padding-left: 5px;")
        self.btn_setting.setText("")
        self.btn_setting.setIconSize(QtCore.QSize(30, 30))
        self.btn_setting.setAutoRaise(True)
        self.btn_setting.setObjectName("btn_setting")
        self.gridLayout_2.addWidget(self.btn_setting, 0, 0, 1, 1)
        
        self.input = QtWidgets.QLineEdit(self.UIB_input_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input.sizePolicy().hasHeightForWidth())
        self.input.setSizePolicy(sizePolicy)
        
        font = QtGui.QFont()
        font.setPointSize(13)
        self.input.setFont(font)
        self.input.setMaxLength(999999999)

        # self.input.setTextMargins(left, top, right, bottom)
        # self.input.setTextMargins(0, 0, 0, 0)

        self.input.setFrame(False)
        self.input.setCursorPosition(0)
        self.input.setClearButtonEnabled(False)
        self.input.setObjectName("input")
        self.input.setAcceptDrops(True)        
        self.gridLayout_2.addWidget(self.input, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.UIB_input_frame, 0, 0, 1, 2)
        self.UIB_main_frame = QtWidgets.QFrame(self.UIB_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UIB_main_frame.sizePolicy().hasHeightForWidth())
        self.UIB_main_frame.setSizePolicy(sizePolicy)
        self.UIB_main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.UIB_main_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.UIB_main_frame.setObjectName("UIB_main_frame")
        self.main_grid_layout = QtWidgets.QGridLayout(self.UIB_main_frame)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.main_grid_layout.setObjectName("main_grid_layout")
        self.gridLayout_7.addWidget(self.UIB_main_frame, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.UIB_frame, 0, 0, 1, 1)

        self.input.dragEnterEvent = self.input_drag_event

    def input_drag_event(self, event: QtGui.QDragEnterEvent):
        data = event.mimeData()

        event.setAccepted(True)

        if data.hasUrls():
            text = data.urls()[0].toLocalFile()
        elif data.hasHtml():
            text = data.html().strip()
        elif data.hasColor():
            text = data.colorData().name()
        else:
            text = data.text()

        self.input.insert(text)