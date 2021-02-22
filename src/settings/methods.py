#!/usr/bin/python3.8

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QCheckBox, QKeySequenceEdit, QLineEdit, QSpinBox

setting = QSettings("kangaroo")

def L_changed(obj: QLineEdit) -> None:
    obj.returnPressed.connect(lambda: setting.setValue(obj.objectName(), obj.text()))

def K_changed(obj: QKeySequenceEdit):
    obj.keySequenceChanged.connect(lambda: setting.setValue(
        obj.objectName(), obj.keySequence()))

def C_changed(obj: QCheckBox):
    obj.stateChanged.connect(lambda: setting.setValue(obj.objectName(), obj.isChecked()))

def S_changed(obj: QSpinBox):
    obj.valueChanged.connect(lambda: setting.setValue(obj.objectName(), obj.value()))

def key_sequence_value(obj: QKeySequenceEdit):
    return obj.keySequence().toString()

def set_key_sequence(obj: QKeySequenceEdit, default):
    obj.setKeySequence(setting.value(obj.objectName(), default))

def set_text(obj: QLineEdit, default):
    obj.setText(setting.value(obj.objectName(), default, str))

def set_spin_value(obj: QSpinBox, default):
    obj.setValue(setting.value(obj.objectName(), default, int))

def set_check(obj: QCheckBox, default):
    obj.setChecked(setting.value(obj.objectName(), default, bool))