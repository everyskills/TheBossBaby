
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QSpinBox

class UIB_Num_type:
    def __init__(self, parent: object, key: str, value: dict):
        self._p = parent
        self._id = key
        self._json = value

        try:
            if self._json.get("title", ""):
                title = QLabel(self._json.get("title", ""))
                self._p.gridLayout.addWidget(title)

            if self._json.get("type", "") in ("float", "double"):
                spin = QDoubleSpinBox()
            else:
                spin = QSpinBox()

            spin.setValue(float(self._json.get("value", 0.0)))
            spin.setPrefix(self._json.get("prefix", ""))
            spin.setSuffix(self._json.get("suffix", ""))

            spin.setStyleSheet("padding: 2px; font-size: 14px;")

            spin.setObjectName(self._id)
            self._p.gridLayout.addWidget(spin)

            self.obj_changed(spin)

            if self._json.get("subtitle", ""):
                subtitle = QLabel(self._json.get("subtitle", ""))
                subtitle.setStyleSheet("padding-left: 3px; font-size: 11px; margin-bottom: 15px;")
                self._p.gridLayout.addWidget(subtitle)
            else:
                spin.setStyleSheet(spin.styleSheet() + "margin-bottom: 10px;")

        except Exception:
            pass

    def obj_changed(self, obj):
        obj.valueChanged.connect(lambda: self.save_settings(obj))

    def save_settings(self, obj):
        data = {"value": obj.value()}
        self._p.edit_settings(obj.objectName(), data)
