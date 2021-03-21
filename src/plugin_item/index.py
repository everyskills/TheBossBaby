#!/usr/bin/python3

import os
from PyQt5 import QtWidgets
from .list_widget import Ui_List

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UIBIPlugin(QtWidgets.QWidget, Ui_List):
    __type__ = "item"

    def __init__(self, parent=None, func: object=None) -> None:
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.parent = parent
        self.func = func
        self.result = {}
        self.sel_color = ""
        self.ret_color = ""

        enterAction = QtWidgets.QAction(
            "enter",
            self.list_widget,
            shortcut="Return",
            triggered=self.run_plug_func)

        ctrlEnterAction = QtWidgets.QAction(
            "altEnter",
            self.list_widget,
            shortcut="Ctrl+Return",
            triggered=self.Ctrl_Enter_Event)

        self.list_widget.addAction(enterAction)
        self.list_widget.addAction(ctrlEnterAction)

        self.list_widget.itemClicked.connect(lambda: self.item_event(False))
        self.list_widget.itemSelectionChanged.connect(lambda: self.item_event(True))

        if self.parent.methods.style == 'dark':
            self.ret_color = self.parent.methods.light_color
            self.sel_color = "#bbbbbb"
        else:
            self.ret_color = self.parent.methods.dark_color
            self.sel_color = "#6e6e6e"

        self.init_ui(self.func)

    def init_ui(self, func):
        if (self.parent.methods.text or func) and (isinstance(func, list) or isinstance(func, tuple)):
            self.set_widget_items(func)
            count = self.list_widget.count()
            if count >= 12:
                self.parent.win_setting.extend_mode()
            else:
                self.parent.win_setting.custom_extend((count * 44) + (90 if not count == 1 else 60))
        else:
            self.parent.win_setting.small_mode()
            self.list_widget.clear()

    def get_search(self, index: int=1):
        split = self.parent.methods.text.split()
        text = ""
        for i in split[index - 1:]:
            text += i + " "
        return text.strip().lower()

    def set_widget_items(self, func):
        self.list_widget.clear()
        self.result.clear()
        black_list = ["\b", "\n", "\v", "\f", "\r", "\a"]

        for item in func:
            try:
                title = str(item.get("title", ""))
                text = self.parent.methods.text

                if (text.lower() in title.strip().lower() or self.list_widget.count() <= 0 or not item.get("filter", True)):
                    if not item.get("icon_theme", False):
                        def_icon = self.parent.get_running_plugin
                        icon = item.get("icon", def_icon.get("icon", "") if def_icon else "").strip()
                        is_icon_theme = False
                    else:
                        icon = item.get("icon", "")
                        is_icon_theme = True

                    if item.get("highlightable", True):
                        title = title.replace(
                        text,
                        f"<font color='{self.sel_color}'>{text}</font>")

                    is_ctrl_enter = item.get("ctrl_enter", hasattr(self.parent.exts.get(self.parent.methods.key, {}).get("script", ""), "ItemCtrlEnter"))
                    is_enter = item.get("func", hasattr(self.parent.exts.get(self.parent.methods.key, {}).get("script", ""), "Run"))

                    item_widget = self.add_item(
                        icon,
                        # title,
                        # str(item.get("subtitle", "")),
                        self.no_space(title, black_list),
                        self.no_space(str(item.get("subtitle", "")), black_list),
                        f"<font size='5' color='{self.ret_color}'>{'⌘' if is_ctrl_enter else ''}{'⏎' if is_enter else ''}</font>",
                        icon_from_theme=is_icon_theme,
                        null_icon=item.get('null_icon'),
                        item_size=(0, 43),
                        icon_provider=item.get("icon_provider", False)
                    )

                    self.result.update({id(item_widget): item})

            except Exception as err:
                print("Error-Add-Item: ", err)
                continue

            self.list_widget.blockSignals(True)
            self.list_widget.setCurrentRow(0)
            self.list_widget.blockSignals(False)

    def no_space(self, text: str, black_list: list):
        if text:
            for i in black_list:
                text = text.replace(i, "")
        return text.strip()

    def run_plug_func(self):
        try:
            data = self.result.get(id(self.list_widget.currentItem()))
            item_index = self.list_widget.currentRow()
            plugin_code = self.parent.exts.get(self.parent.methods.key, {}).get("script", "")
            pp = {}

            if data.get("func", ""):
                pp = data.get("func")(self.parent.methods, type("item", (), data))
            
            elif hasattr(plugin_code, "Run"):
                pp = plugin_code.Run(self.parent.methods, type("item", (), data))

            if not data.get("keep_app_open", False):
                self.parent.hide()

            if pp:
                self.init_ui(pp)
                self.list_widget.setCurrentRow(item_index)
        except Exception as err:
            print("Error-item-return-pressed-run: ", str(err))
            pass

    def item_event(self, selected: bool=False):
        try:
            data = self.result.get(id(self.list_widget.currentItem()))
            item_index = self.list_widget.currentRow()
            item = type("item", (), data)
            plugin_code = self.parent.exts.get(self.parent.methods.key, {}).get("script", "")
            pp = {}

            if not selected:
                if data.get("item_clicked", ""):
                    pp = data.get("item_clicked")(self.parent.methods, item)
                elif hasattr(plugin_code, "ItemClicked"):
                    pp = plugin_code.ItemClicked(self.parent.methods, item)

                if not data.get("keep_app_open", False) == True:
                    self.parent.hide()
            else:
                if data.get("item_selected", ""):
                    pp = data.get("item_selected")(self.parent.methods, item)
                elif hasattr(plugin_code, "ItemSelected"):
                    pp = plugin_code.ItemSelected(self.parent.methods, item)

            if pp:
                self.init_ui(pp)
                self.list_widget.setCurrentRow(item_index)
        except Exception as err:
            print("Error-item-clicked-and-selected: ", str(err))
            pass

    def Ctrl_Enter_Event(self):
        try:
            data = self.result.get(id(self.list_widget.currentItem()))
            item_index = self.list_widget.currentRow()
            plugin_code = self.parent.exts.get(self.parent.methods.key, {}).get("script", "")
            pp = {}

            if data.get("ctrl_enter", ""):
                pp = data.get("ctrl_enter")(self.parent.methods, type("item", (), data))
            elif hasattr(plugin_code, "ItemCtrlEnter"):
                pp = plugin_code.ItemCtrlEnter(self.parent.methods, type("item", (), data))

            if not data.get("keep_app_open", False):
                self.parent.hide()

            if pp:
                self.init_ui(pp)
                self.list_widget.setCurrentRow(item_index)
        except Exception as err:
            print("Error-Alt-Enter: ", err)
            pass
