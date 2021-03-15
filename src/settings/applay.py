#!/usr/bin/python3

import json
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QAction, QApplication
from UIBox.pkg import set_box_shadow
from .main_window import SettingsMainWindow
from . import methods as mt

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class ApplaySettingOnWindow:
    def __init__(self, parent=None) -> None:
        super().__init__()

        self.p = parent
        self.s = mt.setting
        self.mode_style = "light"

        ############## QLineEdit
        self.p.input.setText(self.s.value("start_up_text", ""))
        self.p.input.setPlaceholderText(self.s.value("placeholder_text"))

        ############## QKeysequence Setattr
        self.set_key_action(
            self.p.input, "key_clear_line_text", 
            self.clear_input)

        self.set_key_action(
            self.p.input, "key_clear_split_line_text", 
            self.clear_plugin_value)

        self.set_key_action(
            self.p.input, "key_focus_line_search", 
            self.p.input.setFocus)

        self.set_key_action(
            self.p.input, "key_select_split_line_text", 
            self.select_plugin_value)

        self.set_key_action(self.p, "key_quit_app", QApplication.instance().quit)
        self.set_key_action(self.p, "key_open_settings", self.open_setting_window)
        
        self.set_key_action(self.p, "key_resize_to_larg", self.extend_mode)
        self.set_key_action(self.p, "key_resize_to_small", self.small_mode)

        ############## CHeck Box
        self.check_do("check_round", self.set_round_window)
        self.check_do("check_frameless", lambda: self.p.setWindowFlags(self.p.windowFlags()| Qt.FramelessWindowHint))
        self.check_do("check_shadow", lambda: self.p.setGraphicsEffect(set_box_shadow(30, (20, 20), "black")))
        self.check_do("check_hor_pattern", lambda: self.p.setWindowFlags(self.p.windowFlags() | Qt.HorPattern))

        if not mt.setting.value("check_show_left_icon", True, bool):
            self.p.btn_setting.hide()

        if not mt.setting.value("check_show_right_icon", True, bool):
            self.p.btn_ext.hide()

    def init_setup(self):
        try:
            width = self.p.screen().size().width()
            height = self.p.screen().size().height()
            self.p.move(width - width + 350, height - height + 80)
        except AttributeError:
            pass
        
        self.p.resize(QSize(
            mt.setting.value("window_width", type=int),
            mt.setting.value("window_height", type=int)))
        
        self.p.setWindowTitle("TheBossBaby")
        self.p.setWindowFlags(self.p.windowFlags() | Qt.WindowStaysOnTopHint)
        self.p.setWindowOpacity(mt.setting.value("window_opacity", type=float))
        self.p.setWindowIcon(QIcon(base_dir + "icons/logo.png"))
        self.p.btn_setting.setIcon(QIcon(base_dir + "icons/search.svg"))
        self.p.btn_ext.setIcon(QIcon(base_dir + "icons/logo.png"))

        try:
            style = mt.setting.value("theme", type=str)
            self.mode_style = json.load(open(os.path.split(style)[0] + "/info.json")).get("type", "light")
        except Exception:
            pass

        if os.path.exists(style):
            self.p.setStyleSheet(open(style, "r").read())

        self.p.input.setFocus()

    def open_setting_window(self):
        self.p.hide()
        SettingsMainWindow().show()

    def open_downloader_window(self):
        self.p.hide()
        self.p.open_download_window()
        
    def set_key_action(self, obj, key, func):
        obj.addAction(QAction(key.replace("_", " "), obj,
                              shortcut=mt.setting.value(key), 
                              triggered=func))

    def check_do(self, key, func):
        if mt.setting.value(key, type=bool):
            func()

    def get_val(self, key):
        return mt.setting.value(key)

        # check_auto_launche
        # check_auto_update
        # 
        # key_extend_height
        # key_extend_width
        # 
        # key_open_settings
        # 
        # key_resize_to_larg
        # key_resize_to_small
        # 
        # key_toggle_window
        # key_zoomout_height
        # key_zoomout_width
        # left_icon
        # line_font_style
        # placeholder_text
        # rigth_icon
        # start_up_text
        # window_opacity

    def clear_input(self):
        self.p.input.clear()
        self.p.input.setFocus()

    def select_plugin_value(self):
        k, v = self.p.get_kv(self.p.input.text())
        self.p.input.setSelection(len(k) + 1 if v else 0, len(self.p.input.text()))
        self.p.input.setFocus()

    def clear_plugin_value(self):
        k, v = self.p.get_kv(self.p.input.text())
        self.p.input.setText(k + " " if v else "")
        self.p.input.setFocus()

    def small_mode(self):
        self.set_line_style(False)
        height = mt.setting.value("window_min_extend", type=int)
        if not self.p.UIB_main_frame.isHidden() and self.p.height() != height:
            self.p.UIB_main_frame.hide()
            self.p.setFixedHeight(height)

        # self.p.resize(QSize(mt.setting.value("window_width", type=int), mt.setting.value("window_min_extend", type=int)))

    def extend_mode(self):
        self.set_line_style(True)
        height = mt.setting.value("window_max_extend", type=int)
        if self.p.UIB_main_frame.isHidden() and self.p.height() != height:
            self.p.UIB_main_frame.show()
            self.p.setFixedHeight(height)

        # self.p.resize(QSize(mt.setting.value("window_width", type=int), mt.setting.value("window_max_extend", type=int)))

    def custom_extend(self, value: int):
        self.set_line_style(True)
        if self.p.UIB_main_frame.isHidden():
            self.p.UIB_main_frame.show()
        self.p.setFixedHeight(value)

        # self.p.resize(QSize(self.p.width(), value))


    # def default_mode(self):
    #     self.set_line_style(True)
    #     self.p.UIB_main_frame.show()
    #     self.p.setFixedHeight(180)
    #     # self.p.resize(QSize(self.p.width(), 180))

    def for_ward_cursor(self):
        self.p.input.setCursorPosition(len(self.p.input.text()))

    def set_line_style(self, show: bool = False):
        color = '777d7f' if not self.mode_style == 'light' else 'c8c8c8'  # 'e6e6e6'
        size = '2' if show else '0'
        frsize = '2' if show else '0'

        self.p.setStyleSheet(self.p.styleSheet() +
            """
            /*
            #UIB_input_frame {
                border-bottom-color: #%s;
                border-bottom-width: %spx;
                border-bottom-style: solid;
                padding-bottom: 0px;
                margin-bottom: 0px;
                padding-bottom: %spx;
            }
            */

            #UIB_list_widget {
                border-right-color: #%s;
                border-right-width: %spx;
                border-right-style: solid;
                padding-top: 0px;
                margin-top: 0px;
            }
            """ % (color, size, frsize, color, size))

    def set_round_window(self):
        self.p.setAttribute(Qt.WA_TranslucentBackground, True)
        self.p.setStyleSheet(self.p.styleSheet() + "border-radius: 8px;")

    def set_theme(self, theme_name: str):
        SettingsMainWindow().thm.applay_theme(theme_name)
