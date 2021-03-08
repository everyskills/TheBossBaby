#!/usr/bin/python3

import os

from UIBox import pkg
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Tray_Icon:
    def __init__(self, parent=None) -> None:
        self.p = parent

        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()

    def createActions(self):
        self.hideAction = QAction(QIcon(base_dir + "icons/logo.png"), "&Toggle Window",
                                self.p, 
                                shortcut="Alt+Space", 
                                triggered=self.p.check_win)
        
        self.preferencesAction = QAction(pkg.get_sys_icon(
            "settings-application"), 
            "&Preferences", 
            self.p, 
            shortcut="F1", 
            triggered=self.p.win_setting.open_setting_window)
        
        self.quitAction = QAction(pkg.get_sys_icon(
            "exit-application"), 
            "&Quit", 
            self.p, 
            shortcut="Ctrl+Q", 
            triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self.p)

        self.trayIconMenu.addAction(self.hideAction)
        self.trayIconMenu.addAction(self.preferencesAction)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(QIcon(base_dir + "icons/logo.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setToolTip(f"The Boss Baby v1.0.0")
        self.trayIcon.activated.connect(self.p.check_win)

    def show_message(self, title: str="", body: str="", icon: str="", timeout: int=5, clicked: object=lambda: ()):
        # self.tray = QSystemTrayIcon(QIcon(base_dir + "icons/logo.png"))
        self.trayIcon.messageClicked.connect(clicked)
        self.trayIcon.showMessage(title, body, QIcon(icon), timeout * 1000)
