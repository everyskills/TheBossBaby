#!/usr/bin/python3

import os
import json

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UserCommandCreator(QWidget):
    def __init__(self, parent=None, keywords: list=[], *args, **kwargs):
        super(UserCommandCreator, self).__init__(parent, *args, **kwargs)
        QWidget.__init__(self)

        self.ui = loadUi(base_dir + "user_command.ui", self)
        self.parent = parent
        self.keywords = keywords
        self.data = {} # {key: {tag: "", command: "", icon: ""}}
        self.def_icon = base_dir + "icons/main/executable.png"

        self.ui.btn_image.setIcon(
            QIcon(base_dir + "icons/main/executable.png"))
            
        self.btn_alert.clicked.connect(self.frame_alert.hide)
        self.btn_image.clicked.connect(self.set_image)
        self.btn_cancle.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.get_forms_data)
        
        self.frame_alert.hide()

    def alert(self, msg: str, what: bool=True):
        self.ui.msg_alert.setText(msg)
        self.ui.frame_alert.setStyleSheet(""" 
        #frame_alert {
            color: white;
            border: 2px solid %s;
            background-color: %s;
            border-radius: 5px;
        }
        """ % ('brown' if not what else 'green', 
            'rgba(255, 75, 70, 0.20)' 
            if not what else 'rgba(82, 255, 117, 0.20)'))
        
        self.ui.frame_alert.show()

    def get_image_path(self, native_dialog: bool = False):
        options = QFileDialog.Options()
        if native_dialog:
            options |= QFileDialog.DontUseNativeDialog
        
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Choose Icon", "", 
            "Image Types (*.png);; (*.png);; (*.svg)", 
            options=options)

        if fileName:
            return fileName
        else:
            return ""

    def set_image(self):
        _path = self.get_image_path()
        self.btn_image.setText(_path if _path else self.def_icon)
        self.btn_image.setIcon(QIcon(_path if _path else self.def_icon))

    def get_forms_data(self):
        name = self.line_name.text().strip()
        key = self.line_key.text().strip()
        tag = self.line_tag.text().strip()
        cmd = self.line_cmd.text().strip()
        icon = self.btn_image.text().strip()

        ## Black List 
        black_list = []
        black_list.extend(self.keywords)
        black_list.extend(list(self.parent.exts.keys()))

        if not name or not key:
            self.alert("Error: name or key is empty value please insert value to continue.", False)

        elif not key in black_list:
            with open(base_dir + "Json/user_commands.json") as _fsetting:
                self.data.update(json.load(_fsetting))
                self.data.update({
                    key: {
                        "name": name,
                        "cmd": cmd, 
                        "tag": tag, 
                        "icon": icon if icon else self.def_icon
                        }
                    })
                    
                self.fw(json.dumps(self.data, indent=4))
                _fsetting.close()

            self.alert(f"Good: ({key}) added to commands history")
        else:
            self.alert(f"Error: ({key}) key is already exists", False)

    def closeEvent(self, event) -> None:
        self.parent.show()

    @staticmethod
    def fw(text: str):
        with open(base_dir + "Json/user_commands.json", "w") as _fwrite:
            _fwrite.write(str(text))

def main():
    app = QApplication([])
    win = UserCommandCreator()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
