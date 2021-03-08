#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import json
import sys

from glob import glob
from _methods import Controls
from PyQt5.QtGui import QFont, QIcon
from _plugin_items import UIBIPlugin
from _plugin_web_view import UIBWPlugin
from ui._window import Ui_Form as app_ui
from UIBox import pkg, dialog, item
from PyQt5.QtCore import QEvent, QRunnable, QSize, QThread, QThreadPool, Qt, pyqtSlot
from PyQt5.QtWidgets import QAction, QApplication, QSizeGrip, QStackedWidget, QWidget
from settings.applay import ApplaySettingOnWindow
from _downloader import Downloader
from _keywords import TBB_Keyowrds
from _tray_icon import TBB_Tray_Icon
from _larg_text import TBB_Larg_Text
from threading import Thread

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

try:
    import keyboard
except ModuleNotFoundError:
    sys.path.insert(0, base_dir + '/modules/keyboard.zip')
    import keyboard

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

        ########## TheBossBaby Modules
        self.tbb_keys = TBB_Keyowrds(self)
        self.tbb_tray_icon = TBB_Tray_Icon(self)
        self.tbb_larg_text = TBB_Larg_Text(self)

        self.web = UIBWPlugin(self)
        self.items = UIBIPlugin(self)

        if self.win_setting.s.value("check_history_storage", False, type=bool):
            self.input.keyReleaseEvent = self.key_get_history

        ############ QLineEdit signal/sloat
        self.input.textChanged.connect(self.start_tbb_search)
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
        self.get_all_plugins()
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

    ####################### get all plugins and set them to self.exts var #######################
    def get_all_plugins(self):
        Plugins = glob(base_dir + f"exts/__{pkg.get_platform()}__/*.ext/")
        Plugins.extend(glob(base_dir + "exts/__all__/*.ext/"))
        count = 0
        for rd in Plugins:
            try:
                dic = json.load(open(rd + "info.json")) # info.json
                if dic.get("enabled", False):

                    icon = rd + dic.get("icon", "Icon.png")
                    if not icon or not os.path.exists(icon):
                        icon = base_dir + "icons/main/unknow.png"

                    self.exts.update({str(dic.get("keyword")).strip().lower():
                        {
                            "script": pkg.Import(rd + dic.get("script", "plugin.py")),
                            "object": pkg.Import(rd + dic.get("script", "plugin.py")).Results,
                            "count": count, 
                            "icon": icon,
                            "json": dic,
                            "path": rd
                        }
                    })
                    count += 1
            except Exception as plug_err:
                print(f"Error-add: ({rd}): ", plug_err)
                continue

    @property
    def get_running_plugin(self):
        return self.exts.get(self.get_kv(self.input.text())[0])

    ####################### built in keywords for do some job #######################
    def built_in_func(self):
        try:
            text, val = self.get_kv(self.input.text())
            
            if text in list(self.tbb_keys.Keys.keys()):
                self.tbb_keys.Keys[text](val)
            else:
                key = self.get_kv(self.input.text())[0]

                if key and self.is_key(key):
                    
                    pp = self.exts.get(key).get("script").Run(self.methods)

                    if isinstance(pp, dict):
                        pp.get("keywords", {}).update(self.web_running_data.get("keywords", {}))
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
        exts_keys = list(self.exts.keys())

        self.web.UIB_list_widget.clear()
        
        if self.win_setting.s.value("check_auto_complete", False, bool):
            List = list(self.exts.keys())
            List.extend(list(self.tbb_keys.Keys.keys()))
            self.enforce_line_edit_suffix(List)

        try:
            key = self.input.text().strip().split(
                maxsplit=0)[0].strip().lower() if not key else key
        except IndexError:
            pass

        if not self.input.text().strip():
            self.running = ""
            self.set_sys_icon()
            self.win_setting.small_mode()
        
        elif key in exts_keys and self.input.selectionLength() <= 0:
            self.run_plugin(key)
            
            if self.win_setting.s.value("check_history_storage", False, bool):
                self.update_history()

            self.win_setting.extend_mode()

        elif key.startswith("@"):
            if key in ("@download", "@install", "@downloader", "@installer"):
                self.btn_ext.setIcon(QIcon(base_dir + "icons/main/downloader.png"))

                tbb_downloader = Downloader()
                val = os.path.expandvars(os.path.expanduser(val))

                if os.path.exists(val) and val.endswith(".zip"):
                    tbb_downloader.plugin_file = val
                    tbb_downloader.set_plugin_info(val)

                self.stackedWidget.insertWidget(0, tbb_downloader)

                self.stackedWidget.setCurrentIndex(0)
                self.win_setting.extend_mode()
            else:
                self.btn_ext.setIcon(QIcon(base_dir + "icons/main/executable.png"))
                self.win_setting.small_mode()
        else:
            self.running = ""
            self.set_sys_icon()
            # 
            color = 'black' if not self.methods.style == 'dark' else 'white'
            bg = self.methods.dark_color if self.methods.style == 'dark' else self.methods.light_color
            style = "style='background-color: %s; color: %s;'" % (bg, color)
            self.web.set_html(
                "<html {0}><body {0}>\
                <center><h3> {1} </h3>\
                </center></body></html>".format(style, self.input.text()))
            
            self.web.set_list_items()
            if not self.stackedWidget.currentWidget() == self.web:
                self.stackedWidget.insertWidget(0, self.web)
                self.stackedWidget.setCurrentIndex(0)

            if self.web.UIB_list_widget.count() <= 0:
                self.running = ""
                self.set_sys_icon()
                self.win_setting.small_mode()
            else:
                self.win_setting.extend_mode()

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
    def run_plugin(self, key: str):
        plugin = self.exts.get(key)
        try:
            os.chdir(plugin.get("path"))
            pp = plugin.get("object")(self.methods)
            ############ Fast Code ############
            self.btn_ext.setIcon(QIcon(plugin.get("icon")))
            _w = self.stackedWidget.currentWidget()
            
            if pp and isinstance(pp, dict):
                # print("run web widget")
                ## Qt Web View
                # if _w == None or not getattr(_w, "__type__", "") == "web":
                #     self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                #     self.stackedWidget.insertWidget(0, UIBWPlugin(self, pp))
                # else:
                self.web_running_data = pp
                self.run_web_plugin(plugin.get("icon"), pp)

            elif pp and isinstance(pp, list) or isinstance(pp, tuple):
                ## Qt List Widget Item
                if _w == None or not getattr(_w, "__type__", "") == "item":
                    # print("added new item widget")
                    self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                    self.stackedWidget.insertWidget(0, UIBIPlugin(self, pp))
                else:
                    # print("run item widget")
                    _w.func = pp
                    _w.init_ui(pp)
            else:
                ## Qt Widget
                if not key == self.running and pp:
                    # print("added new qt widget")
                    self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                    self.stackedWidget.insertWidget(0, pp)
                else:
                    if not self.running == "err" and pp:
                        # print("run qt widget")
                        setattr(_w, "parent", self.methods)
                        _w.init_ui()

            self.running = key
            self.running_widget_type = getattr(_w, "__type__", "")
            self.stackedWidget.setCurrentIndex(0)

        except Exception as plug_err:
            print("Error-run-plugin: ", plug_err)

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

                hotkey = "<font size='4' color='%s'>⏎</font>" % ret_color

                if not tag.strip():
                    gr_size = 37
                    uib_item.desc.hide()
                    uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
                else:
                    gr_size = 43
                    uib_item.desc.show()
                    uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

                self.web.UIB_list_widget.setGridSize(QSize(gr_size, gr_size))

                list_item = pkg.add_item(self.web.UIB_list_widget,
                                        QIcon(str(i.get("icon", icon)) if str(i.get("icon", icon)) else icon), 
                                        icon_size=(25, 25))

                item_widget = pkg.add_item_widget(list_item, uib_item, 
                    str(i.get("title", "")),
                    tag, str(hotkey),
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

    @staticmethod
    def get_kv(text: str):
        try:
            k, v = text.split(maxsplit=1)
            return (k.strip().lower(), v.strip())
        except (IndexError, ValueError):
            if text.strip():
                return (text.strip().lower(), "")
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
                self.input.selectAll()
            else:
                self.input.clear()
        else:
            self.hide()

################# main function for run app ##########################
def main():
    app = QApplication(sys.argv)
    win =  MainWindow()

    try:
        if ('--hide') in sys.argv[1:]:
            win.hide()
        else:
            win.show()
    except IndexError:
        win.show()
    
    app.setQuitOnLastWindowClosed(False)
    exit(app.exec_())

if __name__ == "__main__":
    main()


#303136
