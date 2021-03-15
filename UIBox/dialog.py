#!/usr/bin/env python

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QColorDialog, QDialog, QErrorMessage, QFileDialog, QFontDialog,
                            QInputDialog, QLineEdit, QMessageBox)

class UIBDialog(QDialog):
    def __init__(self, parent=None):
        super(UIBDialog, self).__init__(parent)

        self.openFilesPath = ''
        self.errorMessageDialog = QErrorMessage(self)

    def get_integer(self, title: str="integer dialog", prefix: str="", value: int=0, min_value: int=0, max_value: int=100, step: int=1):    
        i, ok = QInputDialog.getInt(self, title, prefix, value, min_value, max_value, step)
        if ok: return i
        else: return None

    def get_double(self, title: str="", prefix: str="", value: float=0.0, min_value: int=-100, max_value: int=100, diget: int=2):
        d, ok = QInputDialog.getDouble(self, title, prefix, value, min_value, max_value, diget)
        if ok: return d
        else: return None

    def get_item(self, title: str="", prefix: str="", items: list=[], start: int=0, editable: bool=False):
        item, ok = QInputDialog.getItem(self, title, prefix, items, start, editable)
        if ok and item: return item
        else: return None

    def get_text(self, title: str="", prefix: str="", mode: str="normal", value: str=""):
        text, ok = QInputDialog.getText(self, title, prefix, QLineEdit.EchoMode(2 if mode.lower().strip() == "pass" else 0), value)
        if ok and text != '': return text
        else: return None

    def get_color(self):    
        color = QColorDialog.getColor(Qt.white, self)
        if color.isValid(): return color
        else: return None 

    def get_font(self):    
        font, ok = QFontDialog.getFont(self)
        if ok: return font
        else: return None

    def get_save_dir(self, title: str="", path: str=""):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, title, path, options=options)
        if directory: return directory
        else: return None

    def get_open_file_name(self, title: str="", value: str="", types: str="All Files (*);; Text Files (*.txt)", native_dialog: bool=False):
        options = QFileDialog.Options()
        if native_dialog:
            options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, title, value, types, options=options)
        if fileName: return fileName
        else: return None

    def get_open_file_names(self, title: str="", value: str="", types: str="All Files (*);; Text Files (*.txt)", native_dialog: bool=False):    
        options = QFileDialog.Options()
        if native_dialog:
            options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, title, value, types, options=options)
        if files: return files
        else: return None

    def get_save_file_name(self, title: str="", value: str="", types: str="All Files (*);; Text Files (*.txt)", native_dialog: bool=False):
        options = QFileDialog.Options()
        if native_dialog:
            options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, title, value, types, options=options)
        if fileName: return fileName
        else: return None

    def critical_message(self, title: str="Critical Message", message: str=""):    
        reply = QMessageBox.critical(self, title, message, QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore)
        
        if reply == QMessageBox.Abort:
            return "abort"
        elif reply == QMessageBox.Retry:
            return "retry"
        else:
            return "ignore"

    def information_message(self, title: str="Information Message", message: str=""):    
        reply = QMessageBox.information(self, title, message)
        
        if reply == QMessageBox.Ok:
            return "ok"
        else:
            return "escape"

    def question_message(self, title: str="Question Message", message: str=""):
        reply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Yes:
            return "yes"
        elif reply == QMessageBox.No:
            return "no"
        else:
            return "cancel"

    def warning_message(self, title: str="Warning Message", message: str=""):
        msgBox = QMessageBox(QMessageBox.Warning, title, message, QMessageBox.NoButton, self)
        msgBox.addButton("&Ok", QMessageBox.AcceptRole)
        msgBox.addButton("&No", QMessageBox.RejectRole)

        if msgBox.exec_() == QMessageBox.AcceptRole: return "ok"
        else: return "no"

    def error_message(self, message: str=""):
        self.errorMessageDialog.showMessage(message)

    def custom_message(self, data: dict={}):        
        btns = {
            "no":     QMessageBox.No,
            "yes":    QMessageBox.Yes,
            "ok":     QMessageBox.Ok,
            "apply":  QMessageBox.Apply,
            "cancel": QMessageBox.Cancel,
            "abort":  QMessageBox.Abort,
            "ignore": QMessageBox.Ignore,
            "retry":  QMessageBox.Retry}

        msgBox = QMessageBox(self)
        btns_2 = {}

        for i in data.get("buttons"):
            try:
                if i and btns[i]:
                    msgBox.addButton(btns[i])
            except KeyError:
                pass

        msgBox.setText(data.get("message"))
        msgBox.setIconPixmap(QPixmap(data.get("logo")))
        msgBox.setWindowTitle(data.get("title"))
        msgBox.setWindowIcon(QIcon(data.get("icon")))

        if not data.get("frame") is None and data.get("frame"):
            msgBox.setWindowFlag(Qt.FramelessWindowHint)

        for k, v in btns.items():
            btns_2[v] = k

        msgBox.show()
        return btns_2[msgBox.exec_()]