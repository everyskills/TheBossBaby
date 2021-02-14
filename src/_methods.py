#!/usr/bin/python3

import re

class Controls:
    send = ""
    sstart = ""

    def __init__(self, parent=None) -> None:
        self.__parent = parent

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
        self.__parent.def_setup.small_size()
    
    def set_extend_mode(self):
        self.__parent.def_setup.larg_size()

    def get_input(self, text: str):
        patt = re.compile(r"\$\(([a-z-A-Z_0-9]+)\)")
        find = patt.findall(text)

        for i in find:
            text = patt.sub(self.__parent.global_vars.get(i.strip(), ""), text)
        
        print("Your text: ", text)
        return text

    def text_changed(self, func: object):
        self.__parent.input.textChanged.connect(func)
    
    def get_text(self):
        try:
            return self.__parent.get_kv(self.__parent.input.text())[1]
        except IndexError:
            pass

    def set_text(self, text: str):
        self.__parent.input.setText(self.__parent.get_kv(self.__parent.input.text())[0] + " " + text)

    def insert_text(self, text: str):
        self.__parent.input.setText(self.__parent.input.text() + text)

    def insert_in_cursor(self, text: str):
        cur = self.__parent.input.cursorPosition()
        self.__parent.input.setCursorPosition(cur)
        txt = self.__parent.get_kv(self.__parent.input.text())[1]
        txt = txt[0:cur] + text + txt[cur:]
        self.__parent.input.insert(text)
        self.__parent.input.setFocus()

    def return_pressed(self, call: object):
        self.__parent.input.returnPressed.connect(call)

    # def insert_in_selecte(self, text: str=""):
    #     # self.__parent.input.selectedText()

    #     self.send = self.__parent.input.selectionEnd()
    #     self.sstart = self.__parent.input.selectionStart()

    #     print("Start: ", self.sstart, "End: ", self.send)
