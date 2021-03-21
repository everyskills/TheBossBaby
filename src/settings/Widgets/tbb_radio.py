from PyQt5.QtWidgets import QLabel, QRadioButton


class UIB_Radio_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        if self._json.get("title", ""):
            title = QLabel(self._json.get("title", ""))
            self._p.add_new_widget(f"{self._id}_title", title)

        line = QLineEdit(self._json.get("value", ""))
        self._p.add_new_widget(self._id, line)
        self.obj_changed(line)

    def obj_changed(self, obj):
        obj.textChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.text()}
        self._p.edit_settings(obj.objectName(), data)
