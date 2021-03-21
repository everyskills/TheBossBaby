from PyQt5.QtWidgets import QLabel, QComboBox

class UIB_Select_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        if self._json.get("title", ""):
            title = QLabel(self._json.get("title", ""))
            title.setStyleSheet("padding-left: 0px;")
            self._p.gridLayout.addWidget(title)

        select = QComboBox()

        select.addItems(self._json.get("options", []))
        
        select.setCurrentText(self._json.get("selected", self._json.get("value", "")))
        select.setObjectName(self._id)

        self._p.gridLayout.addWidget(select)

        self.obj_changed(select)

        if self._json.get("subtitle", ""):
            subtitle = QLabel(self._json.get("subtitle", ""))
            subtitle.setStyleSheet("padding-left: 4px; font-size: 11px; margin-bottom: 15px;")
            self._p.gridLayout.addWidget(subtitle)
        else:
            select.setStyleSheet("margin-bottom: 10px;")

    def obj_changed(self, obj):
        obj.currentTextChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"selected": obj.currentText()}
        self._p.edit_settings(obj.objectName(), data)
