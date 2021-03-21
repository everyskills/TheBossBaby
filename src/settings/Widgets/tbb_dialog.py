
import os
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QToolButton, QWidget
from UIBox import dialog

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UIB_Dialog_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value
        self._dialog = dialog.UIBDialog()

        self.dic = {
            "file": {"icon": "../../icons/main/open.png", "func": self._dialog.get_open_file_name},
            "color": {"icon": "../../icons/main/color.png", "func": self._dialog.get_color},
            "dir": {"icon": "../../icons/main/open.png", "func": self._dialog.get_save_dir},
            # "font": {"icon": "", "func": }
        }

        if self._json.get("title", ""):
            title = QLabel(self._json.get("title", ""))
            self._p.gridLayout.addWidget(title)

        dialog_widget = QWidget()
        dialog_graidLayout = QGridLayout() 
        self.line = QLineEdit(self._json.get("value", ""))
        btn = QToolButton()

        btn.clicked.connect(self.get_dialog_data)
        btn.setIcon(QIcon(base_dir + self.dic.get(self._json.get("dialog", ""), {}).get("icon", "")))
        btn.setIconSize(QSize(30, 30))
        btn.setAutoRaise(True)

        color = f"""border: 2px solid {self._json.get("value", "")};""" if self._json.get("dialog", "") == "color" else ""
        self.line.setStyleSheet(
            "padding: 2px; font-size: 14px;" + color)
        btn.setStyleSheet("margin-top: 0px; padding-top: 0px;")

        self.line.setObjectName(self._id)

        dialog_widget.setLayout(dialog_graidLayout)
        dialog_graidLayout.addWidget(self.line, 1, 0, 1, 1)
        dialog_graidLayout.addWidget(btn, 1, 1, 1, 1)

        self._p.gridLayout.addWidget(dialog_widget)

        self.obj_changed(self.line)

        if self._json.get("subtitle", ""):
            subtitle = QLabel(self._json.get("subtitle", ""))
            subtitle.setStyleSheet("padding-left: 3px; font-size: 11px; margin-bottom: 15px;")
            self._p.gridLayout.addWidget(subtitle)
        else:
            self.line.setStyleSheet(self.line.styleSheet() + "margin-bottom: 10px;")

    def obj_changed(self, obj):
        obj.textChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.text()}
        self._p.edit_settings(obj.objectName(), data)

    def get_dialog_data(self):
        data = self.dic.get(self._json.get("dialog", "")).get("func", lambda: ())()
        if self._json.get("dialog", "") == "color":
            data = data.name()
            self.line.setStyleSheet(
                f"padding: 2px; font-size: 14px; border: 2px solid {data};")
        if data:
            self.line.setText(str(data))
