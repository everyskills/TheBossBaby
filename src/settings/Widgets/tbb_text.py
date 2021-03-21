from PyQt5.QtWidgets import QLabel, QTextEdit


class UIB_Text_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        if self._json.get("title", ""):
            title = QLabel(self._json.get("title", ""))
            self._p.gridLayout.addWidget(title)

        text = QTextEdit(self._json.get("value", ""))

        text.setObjectName(self._id)
        self._p.gridLayout.addWidget(text)

        self.obj_changed(text)

        if self._json.get("subtitle", ""):
            subtitle = QLabel(self._json.get("subtitle", ""))
            self._p.gridLayout.addWidget(subtitle)

    def obj_changed(self, obj):
        obj.textChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.toPlainText()}
        self._p.edit_settings(obj.objectName(), data)
