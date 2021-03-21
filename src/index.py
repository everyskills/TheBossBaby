#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import json
import sys

from UIBox import pkg, dialog, item
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QEvent, QObject, QRunnable, QSize, QThreadPool, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QAction, QApplication, QSizeGrip, QStackedWidget, QWidget
from settings.applay import ApplaySettingOnWindow
from ui._window import Ui_Form as app_ui
from _downloader import Downloader

########### TheBossBaby Add One ################
from add_one.larg_text import TBB_Larg_Text

########### TheBossBaby Plugin Modes ################
from _plugin_web_view import UIBWPlugin
from plugin_item.index import UIBIPlugin

########### Index Code Files Import ################
from _methods import Controls
from _keywords import TBB_Keyowrds
from _tray_icon import TBB_Tray_Icon
from _get_all_plugins import TBB_Get_All_Plugins
from _variables import TBB_Variables

from pyqtkeybind import keybinder
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
sys.path.append(base_dir)

class MainWindow(QWidget, app_ui):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        QWidget.__init__(self)
        self.setupUi(self)
        
        ########### window setting
        self.methods = Controls(self)
        self.win_setting = ApplaySettingOnWindow(self)

        self.win_setting.init_setup()
        self.win_setting.small_mode()

        ############ global variables
        self.running_widget_type = ""
        self.exts = {}
        self.user_cmd = json.load(open(base_dir + "Json/user_commands.json", "r"))        
        self.history = []
        self.current = -1
        self._drag_active = False
        self.running = ""
        self.web_running_data = {}
        self.web_item_results = {}
        self.global_hotkeys = {}

        ########## TheBossBaby Modules
        self.tbb_keys = TBB_Keyowrds(self)
        self.tbb_tray_icon = TBB_Tray_Icon(self)
        self.tbb_larg_text = TBB_Larg_Text(self)
        self.tbb_get_all_plugins = TBB_Get_All_Plugins(self)
        self.tbb_vars = TBB_Variables(self)
        self.web = UIBWPlugin(self)
        self.items = UIBIPlugin(self)
        self.threadpool = QThreadPool()

        if self.win_setting.s.value("check_history_storage", False, type=bool):
            self.input.keyReleaseEvent = self.key_get_history

        ############ QLineEdit signal/sloat
        self.input.textChanged.connect(lambda: self.start_tbb_search(self.tbb_vars.get_var_data(self.input.text())))
        self.input.returnPressed.connect(self.built_in_func)
        self.web.UIB_list_widget.itemActivated.connect(self.web.run_clicked_item)
        
        ############ start app and run all functinos
        self.history_append()
        self.init_ui()

        self.set_sys_icon()

    ############################ check if not hor pattern enabled ########################3
        if not self.win_setting.s.value("check_hor_pattern", False, bool):
            self.mousePressEvent = self.mouse_press_event
            self.mouseMoveEvent = self.mouse_move_event
            self.mouseReleaseEvent = self.mouse_Release_event

        self.screen_shot_action = QAction(
            "screenshot", 
            self, 
            shortcut="Meta+Shift+Return", 
            triggered=self.get_screenshot)        
        self.addAction(self.screen_shot_action)

    ############################ Code for Resize window from left and right ###############################3
        self.gripSize = 16
        self.grips = []

        for _ in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

        # storage = QStorageInfo("/media/osama/SanDisk")
        # print(storage.rootPath())

        # if storage.isReadOnly():
        #     print("isReadOnly:", storage.isReadOnly())

        # qDebug("name:" + storage.name())
        # qDebug("fileSystemType:" + str(storage.fileSystemType()))
        # qDebug("size:" + str(storage.bytesTotal()/1000/1000) + " MB")
        # qDebug("availableSize:" + str(storage.bytesAvailable()/1000/1000) + " MB")

    def resizeEvent(self, event):
        QWidget.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)


    ############################ Move Window Event ###############################3
    def mouse_press_event(self, e):
        self.previous_pos = e.globalPos()

    def mouse_move_event(self, e):
        # self.setCursor(QCursor(Qt.CursorShape(9)))
        try:
            delta = e.globalPos() - self.previous_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.previous_pos = e.globalPos()
        except AttributeError:
            pass

        self._drag_active = True

    def mouse_Release_event(self, e):
        self._drag_active = False

    ####################### get all plugin and set stacked widget ##########################
    def init_ui(self):
        self.tbb_get_all_plugins.get_plugins()
        self.set_stacked_widget()

    ####################### Tacke Simple Screen Shot for TheBossBaby window #######################
    def get_screenshot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        dia = dialog.UIBDialog(self)
        path = dia.get_save_dir("TheBossBaby - Save Screenshot")
        if path and os.path.exists(path):
            screenshot.save(f'{path}/Screenshot.png', 'png')

    ###################### Update History File #############################
    def update_history(self, text: str=""):
        text = self.input.text().strip() if not text else text
        history_file = base_dir + ".history.tbb"
        His = list(map(lambda x: x.strip(), open(history_file, "r").readlines()))
        if not text.strip() in His:
            with open(history_file, "a") as _fw:
                if not text.strip() in self.history:
                    _fw.write(f"{text}\n")
                    self.history_append()
                    self.current = len(self.history)
            _fw.close()

    def open_download_window(self):
        Downloader().show()
        
    ##################### Append commands to history ##########################
    def history_append(self):
        self.history.extend(open(base_dir + ".history.tbb", "r").readlines())

    ###################### Get history commands ####################################
    def key_get_history(self, event):
        if event.type() == QEvent.KeyRelease:
            if event.key() == Qt.Key_Up:
                current = max(0, self.current - 1)
                if 0 <= current < len(self.history):
                    self.input.setText(self.history[current])
                    self.current = current

                event.accept()

            elif event.key() == Qt.Key_Down:
                current = min(len(self.history), self.current + 1)
                if 0 <= current < len(self.history):
                    self.input.setText(self.history[current])
                else:
                    self.input.clear()
                self.current = current

                event.accept()

    ####################### Input Auto Copmlete inside line ################################
    def enforce_line_edit_suffix(self, Iterable: list=[]):
        """This method parses the QLineEdit text and makes sure the desired suffix is there."""
        text = self.input.text().lower()
        for i in Iterable:
            if text and text.startswith(i[0].lower()) and text in i:
                self.input.blockSignals(True)
                self.input.setText(text + i[len(text):])
                self.input.setCursorPosition(int(len(text)))
                self.input.cursorForward(True, int(len(text)) + int(len(i)))
                self.input.blockSignals(False)

    @property
    def get_running_plugin(self):
        return self.exts.get(self.get_kv(self.input.text())[0])

    ####################### built in keywords for do some job #######################
    def built_in_func(self):
        try:
            text, val = self.get_kv(self.input.text())

            if text in list(self.tbb_keys.Keys.keys()):
                self.tbb_keys.Keys[text].get("func")(val)

            else:
                key = self.get_kv(self.input.text())[0]
                if key and self.is_key(key) and hasattr(self.exts.get(key).get("script"), "Run"):
                    pp = self.exts.get(key).get("script").Run(self.methods)
                    
                    if pp and isinstance(pp, dict):
                        self.web_running_data.update(pp)
                        self.run_web_plugin(self.exts.get(key).get("icon"), self.web_running_data)

        except AttributeError as err:
            print("Error-return-pressed-plugin: ", err)

            _w = self.stackedWidget.currentWidget()
            if hasattr(_w, "__run__"):
                _w.__run__()

        except Exception as err:
            print("Error-return-pressed: ", err)
            pass

    ####################### get line edit text and process it #######################
    def start_tbb_search(self, text: str):
        key, val = self.get_kv(text)

        self.web.UIB_list_widget.clear()

        if self.win_setting.s.value("check_auto_complete", False, bool):
            List = list(self.exts.keys())
            List.extend(list(self.tbb_keys.Keys.keys()))
            self.enforce_line_edit_suffix(List)

        try:
            key = self.input.text().strip().split(maxsplit=0)[0].strip().lower() if not key else key
        except IndexError:
            pass

        if not self.input.text().strip():
            self.null_mode()
            self.win_setting.small_mode()

        elif key in list(self.exts.keys()) and self.input.selectionLength() <= 0:    
            # thread = Thread(self)
            # thread.signal.return_signal.connect(self.run_plugin)
            # self.threadpool.start(thread)

            self.run_plugin(key)
            # QApplication.processEvents()

            if self.win_setting.s.value("check_history_storage", False, bool):
                self.update_history()

        elif key.startswith("@") and key in list(self.tbb_keys.Keys.keys()):
            data = self.tbb_keys.Keys.get(key, {})

            icon = base_dir + "icons/keywords/" + data.get("icon", f"{key.lstrip('@')}.png")

            if not os.path.exists(icon):
                icon = base_dir + "icons/main/executable.png"

            self.btn_ext.setIcon(QIcon(icon))

            if data.get("changed", False):
                data.get("func", lambda val: ())(val)

        else:
            self.null_mode()
            self.null_html()

            if not self.stackedWidget.currentWidget() == self.web:
                self.stackedWidget.insertWidget(0, self.web)
                self.stackedWidget.setCurrentIndex(0)

            self.web.set_list_items()
            if self.web.UIB_list_widget.count() <= 0:
                self.win_setting.small_mode()
            else:
                self.win_setting.extend_mode()

    def null_html(self):
        color = 'black' if not self.methods.style == 'dark' else 'white'
        bg = self.methods.dark_color if self.methods.style == 'dark' else self.methods.light_color
        style = "style='background-color: %s; color: %s;'" % (bg, color)
        self.web.set_html("<html {0}><body {0}></body></html>".format(style))

    def null_mode(self):
        self.running = ""
        self.set_sys_icon()

    ###################### Get System Icon Linux/MacOS/Windows #############
    def set_sys_icon(self):
        self.btn_ext.setIcon(QIcon(base_dir + "icons/logo.png"))

    ####################### Create new Stacked Widget #######################
    def set_stacked_widget(self):
        self.stackedWidget = QStackedWidget(self)
        self.main_grid_layout.addWidget(self.stackedWidget)

    def reload_web_plugin(self):
        self.stackedWidget.currentWidget().web_veiw.reload()

    ####################### Run/Set Plugin Code #######################
    # def run_plugin(self, kwargs: dict):
    #     key = kwargs.get("key", "")
    #     pp = kwargs.get("pp")
    #     plugin = self.exts.get(key)

    def run_plugin(self, key: str):
        plugin = self.exts.get(key)

        try:
            pp = plugin.get("object")(self.methods)
            self.btn_ext.setIcon(QIcon(plugin.get("icon")))
            _w = self.stackedWidget.currentWidget()

            if not pp:
                self.win_setting.small_mode()

            ## Web View Plugin
            elif pp and isinstance(pp, dict):
                self.web_running_data = pp
                self.run_web_plugin(plugin.get("icon"), pp)
                self.win_setting.extend_mode()

            ## Lists Widget Item
            elif pp and isinstance(pp, list) or isinstance(pp, tuple):
                if _w == None or not getattr(_w, "__type__", "") == "item":
                    # print("added new item widget")
                    self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                    self.stackedWidget.insertWidget(0, UIBIPlugin(self, pp))
                else:
                    # print("run item widget")
                    _w.func = pp
                    _w.init_ui(pp)

            ## Qt Widget
            else:
                if not key == self.running and pp:
                    # print("added new qt widget")
                    self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                    self.stackedWidget.insertWidget(0, pp)
                elif not self.running == "err" and pp:
                    # print("run qt widget")
                    setattr(_w, "parent", self.methods)
                    _w.init_ui()
    
                self.win_setting.extend_mode()

            self.running = key
            self.running_widget_type = getattr(_w, "__type__", "")
            self.stackedWidget.setCurrentIndex(0)

        except Exception as plug_err:
            print("Error-run-plugin: ", plug_err)
            self.win_setting.small_mode()

    def run_web_plugin(self, icon, data, enabled: bool=True):
        self.web.init_ui(data)
        if data.get("items", []) and enabled:
            self.web.UIB_list_widget.clear()

            for i in data.get("items", []):
                uib_item = item.UIBUi_Item()
                tag = str(i.get("subtitle", ""))
                
                ret_color = (
                    self.methods.light_color
                    if self.methods.style == 'dark'
                    else self.methods.dark_color)

                if not tag.strip():
                    gr_size = 37
                    uib_item.subtitle.hide()
                    uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
                else:
                    gr_size = 43
                    uib_item.subtitle.show()
                    uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

                self.web.UIB_list_widget.setGridSize(QSize(gr_size, gr_size))

                list_item = pkg.add_item(self.web.UIB_list_widget,
                                        QIcon(str(i.get("icon", icon)) if str(i.get("icon", icon)) else icon), 
                                        icon_size=(25, 25))

                item_widget = pkg.add_item_widget(list_item, uib_item, 
                    str(i.get("title", "")),
                    tag,
                    "<font size='4' color='%s'>⏎</font>" % ret_color,
                    item_size=(100, 30 if not tag.strip() else 37))

                font = QFont()
                font.setPixelSize(12)
                item_widget[1].title.setFont(font)

                pkg.set_item_widget(self.web.UIB_list_widget, item_widget)
                self.web_item_results.update({id(list_item): i})

    ####################### Static Methods #######################
    @staticmethod
    def get_js_value(_file: str, key: str, value: str=""):
        try:
            return json.load(open(_file, "r")).get(key.lower().strip(), value)
        except Exception:
            return None

    @staticmethod
    def get_json(_file: str):
        try:
            return json.load(open(_file, "r"))
        except Exception:
            return {}

    def get_kv(self, text: str, strip: bool=True):
        try:
            k, v = text.split(maxsplit=1)
            return (self.tbb_vars.get_var_data(k.lower()), self.tbb_vars.get_var_data(v.strip()) 
                    if strip else self.tbb_vars.get_var_data(v))
        except (IndexError, ValueError):
            if text.strip():
                return (self.tbb_vars.get_var_data(text.strip().lower()), "")
            else:
                return ("", "")

    def is_key(self, text: str=""):
        return text if text else self.running in list(self.exts.keys())
        
    ####################### Create System Tray #######################
    def check_win(self):
        if self.isHidden():
            self.show()
            self.setFocus()
            self.input.setFocus()
            if self.input.text().strip():
                self.input.setSelection((len(self.methods.key) + 1), len(self.methods.text))
            else:
                self.input.clear()
        else:
            self.hide()

    def register_hotkey(self, hotkey: str, callback: object):
        # keybinder.register_hotkey(self.winId(), hotkey, callback)
        self.global_hotkeys.update({hotkey: callback})

    def set_global_hotkeys(self):
        startup_hotkey = self.win_setting.s.value("key_toggle_window", "Alt+Space", str)
        self.register_hotkey(startup_hotkey, self.check_win)

        # keybinder.unregister_hotkey(self.p.winId(), hotkey)

        for k, v in self.global_hotkeys.items():
            if str(k).strip() and v:
                keybinder.register_hotkey(self.winId(), k, v)
            

class Signals(QObject):
    return_signal = pyqtSignal(dict)

class Thread(QRunnable):
    def __init__(self, main_window=None):
        super(Thread, self).__init__()
        self.signal = Signals()
        self.p = main_window
        self.key = self.p.get_kv(self.p.input.text())[0]

    @pyqtSlot()
    def run(self):
        self.pp = self.p.exts.get(self.key).get("object")(self.p.methods)
        if self.key and self.pp:
            self.signal.return_signal.emit({"key": self.key, "pp": self.pp})






















# class Worker(QRunnable):
#     '''
#     Worker thread

#     Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

#     :param callback: The function callback to run on this worker thread. Supplied args and
#                      kwargs will be passed through to the runner.
#     :type callback: function
#     :param args: Arguments to pass to the callback function
#     :param kwargs: Keywords to pass to the callback function
#     '''

#     def __init__(self, fn):
#         super(Worker, self).__init__()
#         self.fn = fn

#     @pyqtSlot()
#     def run(self):
#         '''
#         Initialise the runner function with passed args, kwargs.
#         '''
#         # self.fn(*self.args, **self.kwargs)
#         self.fn()

        # self.threadpool = QThreadPool()
        # self.threadpool.start(Worker())


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

################# main function for run app ##########################
def main():
    app = QApplication(sys.argv)
    window =  MainWindow()

    keybinder.init()
    
    window.set_global_hotkeys()

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    try:
        if ('--hide') in sys.argv[1:]:
            window.hide()
        else:
            window.show()
    except IndexError:
        window.show()
    
    app.setQuitOnLastWindowClosed(False)
    exit(app.exec_())

if __name__ == "__main__":
    main()
