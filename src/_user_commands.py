#!/usr/bin/python3

import os
import json

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.uic import loadUi
from UIBox import item, pkg

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UserCommandCreator(QWidget):
    def __init__(self, parent=None, keywords: list=[], *args, **kwargs):
        super(UserCommandCreator, self).__init__(parent, *args, **kwargs)
        QWidget.__init__(self)

        self.ui = loadUi(base_dir + "ui/user_command.ui", self)
        self.parent = parent
        self.keywords = keywords
        self.data = {} # {key: {tag: "", command: "", icon: ""}}
        self.def_icon = base_dir + "icons/main/executable.png"

        self.cmd_icon.mousePressEvent = self.edit_image
    
        self.ui.btn_image.setIcon(
            QIcon(base_dir + "icons/main/executable.png"))
            
        self.list_widget.itemSelectionChanged.connect(self.set_info)

        self.btn_alert.clicked.connect(self.frame_alert.hide)
        self.btn_image.clicked.connect(self.set_image)
        self.btn_cancle.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.save_data)
        
        self.set_data()
        self.frame_alert.hide()
        
    def edit_image(self, event):
        if self.key.text().strip():
            self.set_image()
            self.edit_cmd()

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
            "PNG Image Type (*.png);; JPG Image Type (*.jpg);; SVG Image Type (*.svg)", 
            options=options)

        if fileName:
            return fileName
        else:
            return ""

    def set_image(self):
        _path = self.get_image_path()
        icon = _path if _path else self.def_icon
        self.btn_image.setText(icon)
        self.btn_image.setIcon(QIcon(icon))
        self.cmd_icon.setPixmap(QIcon(icon).pixmap(40, 40))

    def get_forms_data(self, name="", key="", tag="", icon="", cmd="", update: bool=False):
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

        self.set_data()

    def set_data(self):
        self.list_widget.clear()
        for k in list(self.parent.user_cmd.keys()):
            key = self.parent.user_cmd.get(k)
            list_item = pkg.add_item(self.list_widget, QIcon(key.get("icon")))
            item_widget = pkg.add_item_widget(list_item, item.UIBUi_Item, 
            key.get("name"), 
            key.get("tag"),  k)
            pkg.set_item_widget(self.list_widget, item_widget)

    def closeEvent(self, event) -> None:
        self.parent.show()

    @staticmethod
    def fw(text: str):
        with open(base_dir + "Json/user_commands.json", "w") as _fwrite:
            _fwrite.write(str(text))

    def set_info(self):
        item = self.list_widget.currentItem()
        item_widget = item.listWidget().itemWidget(item)
        
        self.key.textChanged.connect(self.edit_cmd)

        k = item_widget.shortcut.text()
        key = self.parent.user_cmd.get(k)

        self.cmd_name.setText(key.get("name"))
        self.cmd_tag.setText(key.get("tag"))
        self.cmd_icon.setPixmap(QIcon(key.get("icon")).pixmap(40, 40))

        self.key.setText(k)
        self.name.setText(key.get("name"))
        self.tag.setText(key.get("tag"))
        self.cmd.setText(key.get("cmd"))

    def edit_cmd(self):
        self.get_forms_data(
            name = self.name.text().strip(),
            cmd = self.cmd.text().strip(),
            icon = self.btn_image.text().strip(),
            key = self.key.text().strip(),
            tag = self.tag.text().strip(),
            update = True
            )

    def save_data(self):
        self.get_forms_data(
            name = self.line_name.text().strip(),
            cmd = self.line_cmd.text().strip(),
            icon = self.btn_image.text().strip(),
            key = self.line_key.text().strip(),
            tag = self.line_tag.text().strip()
            )

def main():
    app = QApplication([])
    win = UserCommandCreator()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
