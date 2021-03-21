from PyQt5.QtWidgets import QCheckBox

class UIB_Check_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        check = QCheckBox(self._json.get("name", ""))
        check.setStyleSheet("margin-bottom: 10px;")
        check.setChecked(self._json.get("value", False))
        check.setObjectName(self._id)
        self._p.gridLayout.addWidget(check)

        self.obj_changed(check)

    def obj_changed(self, obj):
        obj.stateChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.isChecked()}
        self._p.edit_settings(obj.objectName(), data)
