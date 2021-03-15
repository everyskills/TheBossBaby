#!/usr/bin/python3

import os
from UIBox import pkg
from PyQt5 import QtCore, QtGui, QtWidgets

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UIBUi_Item(QtWidgets.QWidget):
    def __init__(self):
        super(UIBUi_Item, self).__init__()

        self.setObjectName("Form")
        self.setMouseTracking(True)

        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, -2, 0)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setVerticalSpacing(0)

        self.title = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.title.setFont(font)
        self.title.setText("")
        self.title.setObjectName("title")
        # self.title.setWordWrap(True)

        # self.gridLayout.addWidget(self.title, 0, 1, 2, 1)
        self.subtitle = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.subtitle.setFont(font)
        self.subtitle.setText("")
        self.subtitle.setObjectName("subtitle")

        self.subtitle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.subtitle.setAlignment(QtCore.Qt.AlignLeft)
        # self.subtitle.setWordWrap(True)

        self.gridLayout.addWidget(self.subtitle, 1, 1, 1, 1)
        self.image = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setText("")
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 2, 1)
        self.hotkey = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hotkey.sizePolicy().hasHeightForWidth())
        self.hotkey.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.hotkey.setFont(font)
        self.hotkey.setText("")
        # self.hotkey.setWordWrap(True)
        self.hotkey.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.hotkey.setObjectName("hotkey")
        self.gridLayout.addWidget(self.hotkey, 0, 2, 2, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.setStyleSheet("""
        /* color: #898b8c; */
        #subtitle {
            padding-left: 4px;
            font-size: 12px;
            color: #929a90;
            padding-top: 2px;
            padding-bottom: 2px;
        }

        #title {
            padding-left: 2px;
        }

        #hotkey {
        	padding-left: 5px;
        }
        """)

class Ui_List(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.list_widget = QtWidgets.QListWidget(Form)
        self.list_widget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.list_widget.setStyleSheet("QListWidget {\n"
        "    padding: 0;\n"
        "    margin: 0;\n"
        "    background: transparent;\n"
        "    padding-left: 5px;"
        "    padding-right: 5px;"
        "}")

        self.list_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_widget.setFrameShadow(QtWidgets.QFrame.Plain)
        
        # self.list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.list_widget.setAutoScroll(True)

        self.list_widget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list_widget.setGridSize(QtCore.QSize(0, 45))
        self.list_widget.setObjectName("list_widget")
        self.gridLayout.addWidget(self.list_widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def add_item(self, icon: str="", title: str="", tag: str="", 
    			hotkey: str="", icon_from_theme: bool=False, 
                null_icon: str='', item_size=(0, 40)):

        uib_item = UIBUi_Item()

        if not tag.strip():
            uib_item.subtitle.hide()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
        else:
            uib_item.subtitle.show()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

        if icon_from_theme:
            icon = QtGui.QIcon.fromTheme(icon)
        else:
            icon = QtGui.QIcon(icon)
        
        if icon.isNull():
            icon = QtGui.QIcon(null_icon)

        uib_item.title.setText(title)
        uib_item.subtitle.setText(tag)
        uib_item.hotkey.setText(hotkey)

        list_item = pkg.add_item(self.list_widget, icon, icon_size=(30, 30))
        list_item.setSizeHint(QtCore.QSize(item_size[0], item_size[1]))
        pkg.set_item_widget(self.list_widget, (list_item, uib_item))
        
        return list_item

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.list_widget.setSortingEnabled(True)

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
        if self.parent.methods.text:            
            self.set_widget_items(func)
            count = self.list_widget.count()
            if count >= 13:
                self.parent.win_setting.extend_mode()
            else:
                self.parent.win_setting.custom_extend((count * 42) + (90 if not count == 1 else 60))
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

        if isinstance(func, list) or isinstance(func, tuple):
            for item in func:
                title = str(item.get("title", ""))
                text = self.parent.methods.text.strip()

                if (text.lower() in title.strip().lower() or self.list_widget.count() <= 0 or not item.get("filter", True)):

                    if not item.get("icon_theme", False):
                        def_icon = self.parent.get_running_plugin
                        icon = item.get("icon", def_icon.get("icon")).strip()
                        is_icon_theme = False
                    else:
                        icon = item.get("icon", "")
                        is_icon_theme = True

                    if item.get("highlightable", True):
                        title = title.replace(
                        text,
                        f"<font color='{self.sel_color}'>{text}</font>")

                    is_ctrl_enter = item.get("ctrl_enter", hasattr(self.parent.exts.get(self.parent.running).get("script"), "ItemCtrlEnter"))

                    item_widget = self.add_item(
                        icon,
                        self.no_space(title, black_list),
                        self.no_space(str(item.get("subtitle", "")), black_list),
                        f"<font size='5' color='{self.ret_color}'>{'⌘' if is_ctrl_enter else ''}⏎</font>",
                        icon_from_theme=is_icon_theme,
                        null_icon=item.get('null_icon'),
                        item_size=(0, 40)
                    )

                    self.result.update({id(item_widget): item})

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
            plugin_code = self.parent.exts.get(self.parent.running).get("script")
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
            plugin_code = self.parent.exts.get(self.parent.running).get("script")
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
            plugin_code = self.parent.exts.get(self.parent.running).get("script")
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