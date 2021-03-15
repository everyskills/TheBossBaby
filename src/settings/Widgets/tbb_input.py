
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QLineEdit, QSizePolicy, QToolButton

class UIB_Input_type:
    def __init__(self):
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.name = QLabel(self.frame)
        self.name.setObjectName(u"name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.name, 0, 1, 1, 1)

        self.button = QToolButton(self.frame)
        self.button.setObjectName(u"button")

        self.gridLayout_2.addWidget(self.button, 1, 0, 1, 1)

        self.input = QLineEdit(self.frame)
        self.input.setObjectName(u"input")

        self.gridLayout_2.addWidget(self.input, 1, 1, 1, 1)

        self.description = QLabel(self.frame)
        self.description.setObjectName(u"description")
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.description, 2, 1, 1, 1)
