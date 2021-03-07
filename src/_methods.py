#!/usr/bin/python3

import re
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Controls:
    def __init__(self, parent=None) -> None:
        self.__parent = parent
        self.cb = QtWidgets.QApplication.clipboard()

        ## Whenever clipboard data changes
        # self.cb.dataChanged.connec()

    def close_win(self):
        self.__parent.close()

    def hide_win(self):
        self.__parent.hide()

    def show_win(self):
        self.__parent.show()

    def set_win_height(self, h: int):
        if not h < 70:
            self.__parent.setFixedHeight(h)
        
    def set_win_width(self, w: int):
        if not w > 700:
            self.__parent.setFixedWidth(w)

    def set_win_size(self, w: int, h: int):
        self.__parent.setFixedSize(w, h)

    def set_small_mode(self):
        self.__parent.win_setting.small_mode()
    
    def set_extend_mode(self):
        self.__parent.win_setting.extend_mode()

    @property
    def is_dark(self):
        return self.mode_style == 'dark'

    @property
    def is_light(self):
        return self.mode_style == 'light'

    @property
    def mode_style(self):
        return 'dark' if 'dark' in self.__parent.win_setting.mode_style else 'light'

    @property
    def style_mode(self):
        return self.mode_style

    @property
    def style(self):
        return self.mode_style

    @property
    def text(self):
        return self.get_text()

    @property
    def value(self):
        return self.get_text()
        
    @property
    def result(self):
        return self.get_text()

    @property
    def dark_color(self):
        return "#393D40"

    @property
    def light_color(self):
        return "#f6f6f6"

    def post_message(self, title: str="", body: str="", icon: str="", timeout: int=5, clicked: object=lambda: ()):
        self.__parent.tbb_tray_icon.show_message(title, body, icon, timeout, clicked)

    def larg_text(self, text: str="", font_size: int=50, timeout: int=5000):
        self.__parent.tbb_larg_text.larg_text(text, font_size, timeout)


    def text_changed(self, func: object):
        self.__parent.input.textChanged.connect(func)


    def text_copy(self, text: str=""):
        if not text:
            self.__parent.input.copy()
        else:
            self.cb.setText(text)

    def text_cut(self):
        self.__parent.input.cut()

    def set_text(self, text: str):
        self.__parent.input.setText(self.__parent.get_kv(
            self.__parent.input.text())[0] + " " + text)

    def insert_text(self, text: str):
        self.__parent.input.setText(self.__parent.input.text() + text)

    def text_paste(self, get: bool=False):
        if not get:
            self.__parent.input.paste()
        else:
            return self.cb.text()

    def by_key(self, key: str, default=None, index=None) -> dict:
        _dict = {}
        args = self.text.split()

        for i in range(len(args)):
            if i == index or index == None:
                try:
                    _dict.update({args[i]: args[i + 1]})
                except IndexError:
                    _dict.update({args[i]: ""})
        
        return _dict.get(key, default)

    def reload_page(self, count: int=1):
        for _ in range(count):
            self.__parent.web.run_plugin(self.__parent.web_running_data)

    def include_file(self, _file: str):
        key = self.__parent.get_kv(self.__parent.input.text())[0]
        return QUrl.fromUserInput(self.__parent.exts.get(key, {}).get("path") + _file).toLocalFile()

    def get_input(self, text: str):
        patt = re.compile(r"\$\(([a-z-A-Z_0-9]+)\)")
        find = patt.findall(text)
        for i in find:
            text = patt.sub(self.__parent.global_vars.get(i.strip(), ""), text)
        return text

    def get_text(self, exception: str=""):
        try:
            text = self.__parent.get_kv(self.__parent.input.text())[1].strip()
            if exception:
                return re.sub(r"%s" % exception, "", text)
            else:
                return text
        except IndexError:
            return ""

    def insert_in_cursor(self, text: str):
        cur = self.__parent.input.cursorPosition()
        self.__parent.input.setCursorPosition(cur)
        txt = self.__parent.get_kv(self.__parent.input.text())[1]
        txt = txt[0:cur] + text + txt[cur:]
        self.__parent.input.insert(text)
        self.__parent.input.setFocus()

    def set_auto_complete(self, Iterable: list=[]):
        text = self.get_text()
        for i in Iterable:
            if text and text.startswith(i[0].lower()) and text in i:
                self.__parent.input.blockSignals(True)
                ######### auto type 1
                self.set_text(text + i[len(text):] + " ")
                self.__parent.input.setCursorPosition(
                    int(len(text)) + len(self.__parent.get_kv(self.__parent.input.text())[0]) + 1)
                self.__parent.input.cursorForward(True, int(len(text)) + int(len(i)))
                self.__parent.input.blockSignals(False)
