
from PyQt5.QtWidgets import QLabel, QLineEdit
class UIB_Input_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        if self._json.get("title", ""):
            title = QLabel(self._json.get("title", ""))
            self._p.gridLayout.addWidget(title)

        line = QLineEdit(self._json.get("value", ""))
        line.setStyleSheet("padding: 2px; font-size: 14px;")

        line.setObjectName(self._id)
        self._p.gridLayout.addWidget(line)

        self.obj_changed(line)

        if self._json.get("subtitle", ""):
            subtitle = QLabel(self._json.get("subtitle", ""))
            subtitle.setStyleSheet("padding-left: 3px; font-size: 11px; margin-bottom: 15px;")
            self._p.gridLayout.addWidget(subtitle)
        else:
            line.setStyleSheet(line.styleSheet() + "margin-bottom: 10px;")

    def obj_changed(self, obj):
        obj.textChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.text()}
        self._p.edit_settings(obj.objectName(), data)
