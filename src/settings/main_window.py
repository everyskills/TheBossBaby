#!/usr/bin/python3

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QListWidgetItem, QMainWindow
from .geter import SettingsWindow, base_dir

class SettingsMainWindow(QMainWindow, SettingsWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.parent = parent
        self.resize(QtCore.QSize(1000, 600))
        self.setWindowIcon(QIcon(base_dir + "icons/logo.png"))
        self.setWindowTitle("The Boss Baby - Settings")

        self.dict = {
            0: ("logo.png", lambda: self.stacked_widget_root.setCurrentIndex(0)),
            1: ("window.png", lambda: self.stacked_widget_root.setCurrentIndex(1)),
            2: ("theme.png", lambda: self.stacked_widget_root.setCurrentIndex(2))
        }

        self.set_root_tabs()
        self.list_widget_root.itemSelectionChanged.connect(self.set_tab)
        self.quitAction = QAction("Quit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.addAction(self.quitAction)

    def set_tab(self):
        item = self.list_widget_root.currentItem()
        index = self.list_widget_root.row(item)

        self.dict.get(index)[1]()

    def set_root_tabs(self):
        for i in self.dict.values():
            att = QListWidgetItem()
            att.setIcon(QIcon(base_dir + "icons/" + i[0]))
            self.list_widget_root.addItem(att)

def main():
    app = QApplication([])
    win = SettingsMainWindow()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
