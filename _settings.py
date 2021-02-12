#!/usr/bin/python3

import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QStyleFactory

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

__app_name__ = "Kangaroo"
__version__ = "1.3.6"
__author__ = "Osama Muhammed Alzabidi"

class MainWindowSettings:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        
        self.max_ext = 670
        self.min_ext = 70
        self.win_width = 700

    def init_setup(self):
        self.set_window_settings()

        quitAction = QAction("Quit", self.parent, shortcut=self.kquit,
                            triggered=QApplication.instance().quit)

        closeeAction = QAction("Hide", self.parent, shortcut=self.khide,
                            triggered=self.parent.hide)

        focusAction = QAction("setFocus", self.parent, shortcut=self.klfocus,
                            triggered=self.parent.input.setFocus)

        clearAction = QAction("clearText", self.parent, shortcut=self.kclear,
                            triggered=self.clear_input)

        clearValueAction = QAction("clearPluginValue", self.parent, shortcut=self.krmsp,
                                triggered=self.clear_plugin_value)
                                
        self.parent.input.addAction(clearValueAction)
        self.parent.input.addAction(clearAction)
        self.parent.input.addAction(focusAction)
        self.parent.addAction(closeeAction)
        self.parent.addAction(quitAction)
    
        self.parent.move(360, 60)
        self.parent.setFixedSize(self.win_width, 320)
        self.parent.setWindowFlags(self.parent.windowFlags()
                                    | Qt.WindowStaysOnTopHint)

        QApplication.instance().setApplicationName("Kangaroo")
        QApplication.instance().setApplicationVersion("1.3.6")
        QApplication.instance().setQuitLockEnabled(True)
        
        self.parent.setWindowTitle("Kangaroo")
        self.parent.input.setPlaceholderText("Kangaroo - search...")
        self.parent.btn_setting.setIcon(QIcon(base_dir + "icons/main/search.svg"))
        self.parent.input.setFocus()


    def set_window_settings(self, data: str=""):
        with open(base_dir + "settings.json", "r") as _fs:
            data = json.load(_fs) if not data else data

            style = base_dir + "styles/" + data.get("theme") + ".qss"

            # self.set_key(self.key_start_up, data.get("key_start_up", ""))
            self.kquit = data.get("key_quit")
            self.kclear = data.get("key_clear_input")
            self.krmsp = data.get("key_remove_split")
            self.khide = data.get("key_hide")
            self.klfocus = data.get("key_line_focus")

            if os.path.exists(style):
                self.parent.setStyleSheet(open(style).read())
            else:
                self.parent.setStyleSheet("")
                QApplication.setStyle(QStyleFactory.create(data.get("theme")))

            self.parent.setWindowOpacity(data.get("opacity"))

            self.max_ext = data.get("max_ext")
            self.min_ext= data.get("min_ext")
            self.win_width = data.get("window_width")
            
            self.parent.setFixedSize(self.win_width, 320)
            # self.check_launche.setChecked(data.get("is_launch_at_login"))
            # self.check_auto.setChecked(data.get("is_auto_check_update"))

            if data.get("is_rounded"):
                self.parent.setAttribute(Qt.WA_TranslucentBackground, True)

            if data.get("is_frame_less"):
                self.parent.setWindowFlags(
                    self.parent.windowFlags() 
                    | Qt.FramelessWindowHint)
            
            if data.get("is_shadow"):
                self.parent.setGraphicsEffect(self.parent.set_shadow(3, (2, 2), "black"))

            if data.get("is_hor_pattern"):
                self.parent.setWindowFlags(
                    self.parent.windowFlags() 
                    | Qt.HorPattern)

            _fs.close()
            self.extend_mode()

    def clear_input(self):
        self.parent.input.clear()
        self.parent.input.setFocus()

    def clear_plugin_value(self):
        k = self.parent.get_kv(self.parent.input.text())[0]
        self.parent.input.setText(k + " " if k else "")

    def small_mode(self):
        self.parent.setFixedHeight(self.min_ext)
        self.parent.main_frame.hide()

    def extend_mode(self):
        self.parent.setFixedHeight(self.max_ext)
        self.parent.main_frame.show()

    def default_mode(self):        
        self.parent.setFixedHeight(180)
        self.parent.main_frame.show()
