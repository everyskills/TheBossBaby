#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import json
import sys

from threading import Thread
from glob import glob
from UIBox import pkg, list_item, dialog
from PyQt5.QtCore import QEvent, QSize, QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSizeGrip, QStackedWidget, QSystemTrayIcon, QWidget
from plugin_settings import PluginSettings
from _methods import  Controls
from ui._window import Ui_Form as app_ui
from _user_commands import UserCommandCreator
from _plugin_web_view import UIBWPlugin
from _plugin_items import UIBIPlugin
from settings.applay import ApplaySettingOnWindow

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

__keywords__ = ["small", "install", "download", 
                "about", "exit", "quit", "resize",
                "killme", "close-uibox", "quit-uibox",
                "update", "refresh", "clone", "add-cmd",
                "add-shortcut", "test", "kng", "uibox",
                "create", "create-plugin", "clear-history",
                "reload"]

__keywords__ = list(map(lambda x: "@" + x, __keywords__))

types = json.load(open(base_dir + "Json/types.json"))

def get_type(_path):
    ty = os.path.splitext(os.path.split(_path)[1])[1].lstrip(".").lower()
    for k, v in types.items():
        if ty in v:
            return k

class MainWindow(QWidget, app_ui):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        QWidget.__init__(self)
        self.setupUi(self)
        
        ########## create system tray
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()

        self.running_widget_type = ""

        ########### window setting
        self.methods = Controls(self)

        self.win_setting = ApplaySettingOnWindow(self)
        self.win_setting.init_setup()
        self.win_setting.small_mode()

        self.web = UIBWPlugin(self)

        ############ global variables
        self.exts = {}         # {key: {count, object, path, icon}}
        self.user_cmd = json.load(open(base_dir + "Json/user_commands.json", "r"))        
        self.history = []
        self.current = -1
        self._drag_active = False
        self.running = ""
        self.web_running_data = {}

        if self.win_setting.s.value("check_history_storage", False, type=bool):
            self.input.keyReleaseEvent = self.key_get_history

        ############ QLineEdit signal/sloat
        self.input.textChanged.connect(self.split_check)
        # self.input.textEdited.connect(self.split_check)
        self.input.returnPressed.connect(self.built_in_func)

        ############ start app and run all functinos
        self.history_append()
        self.init_ui()
        # self.set_sys_icon()

    ############################ check if not hor pattern enabled ########################3
        if not self.win_setting.s.value("check_hor_pattern", False, bool):
            self.mousePressEvent = self.mouse_press_event
            self.mouseMoveEvent = self.mouse_move_event
            self.mouseReleaseEvent = self.mouse_Release_event

        self.screen_shot_action = QAction("screenshot", self, shortcut="Meta+Shift+Return", triggered=self.get_screen_shot)
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
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
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

    def get_screen_shot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        dia = dialog.UIBDialog(self)
        path = dia.get_save_dir("Save ScreenShot Directory path")
        if path and os.path.exists(path):
            screenshot.save(f'{path}/Screenshot.png', 'png')

    ###################### Update History File #############################
    def update_history(self, text: str=""):
        text = self.input.text().strip() if not text else text
        history_file = base_dir + ".history.kng"
        His = list(map(lambda x: x.strip(), open(history_file, "r").readlines()))
        if not text.strip() in His:
            with open(history_file, "a") as _fw:
                if not text.strip() in self.history:
                    _fw.write(f"{text}\n")
                    self.history_append()
                    self.current = len(self.history)

            _fw.close()

    ##################### Append commands to history ##########################
    def history_append(self):
        self.history.extend(open(base_dir + ".history.kng", "r").readlines())

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
                
                ######### auto type 1
                self.input.setText(text + i[len(text):])
                self.input.setCursorPosition(int(len(text)))
                self.input.cursorForward(True, int(len(text)) + int(len(i)))
                
                ######## auto type 2
                # self.input.setText(text + " - " + i)
                # self.input.setCursorPosition(int(len(text)))
                # self.input.cursorForward(True, int(len(text)) + int(len(i)) + 3)

                self.input.blockSignals(False)

    ####################### get all plugins and set them to self.exts var #######################
    def get_all_plugins(self):
        Plugins = glob(base_dir + f"exts/__{self.get_platform}__/*.ext/")
        Plugins.extend(glob(base_dir + f"exts/__all__/*.ext/"))
        count = 0

        for rd in Plugins:
            try:
                dic = self.get_json(rd + "package.json")
                obj = pkg.Import(rd + dic.get("script")).Results
                icon = rd + dic.get("icon", "")
                
                if not os.path.exists(icon):
                    icon = rd + "Icon.png"

                self.exts.update(
                    {
                        str(dic.get("key")).strip(): 
                            {
                                "script": pkg.Import(rd + dic.get("script")),
                                "count": count, 
                                "object": obj,
                                "path": rd, 
                                "icon": icon,
                                "json": dic
                            }
                        }
                    )
                count += 1
            except Exception as plug_err:
                print(f"Error-add: ({rd}): ", plug_err)
                continue

    @property
    def get_running_plugin(self):
        print(self.get_kv(self.input.text())[0])
        return self.exts.get(self.get_kv(self.input.text())[0])

    ####################### Get System type Name ################################
    @property
    def get_platform(self):
        platform = ""
        if sys.platform.startswith(("linux")):
            platform = "linux"
        elif sys.platform.startswith("win"):
            platform = "windows"
        elif sys.platform.startswith("darw"):
            platform = "macos"
        else:
            platform = "all"

        return platform

    ####################### built in keywords for do some job #######################
    def built_in_func(self):
        text = ""

        try:
            text, val = self.get_kv(self.input.text())

            if text in ("@exit", "@quit"):
                self.hide()
                self.input.clear()
                self.win_setting.small_mode()

            elif text in ("@small", "@resize"):
                self.win_setting.small_mode()

            elif text in ("@killme", "@close-uibox", "@quit-uibox"):
                QApplication.instance().quit()

            elif text in ("@download", "@install", "@clone"):
                PluginSettings(win=self).install_url()

            elif text in ("@add-cmd", "@add-shortcut"):
                self.hide()
                UserCommandCreator(self, keywords=__keywords__).show()

            elif text in ("@create", "@create-plugin"):
                self.create_plugin()

            elif text in ("@clear-history"):
                fw = open(base_dir + ".history.kng", "w")
                fw.write("")
                fw.close()
                self.input.clear()

            elif text in ("@reload"):
                ## reset plugins
                self.exts.clear()
                self.get_all_plugins()

                ## reset stacked widget
                self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
                
                ## reset settings
                self.win_setting.init_setup()

                self.input.clear()
                
            elif text in list(self.user_cmd.keys()):
                pkg.run_app(self.user_cmd.get(text.strip()).get("cmd"))
            
            else:
                key = self.get_kv(self.input.text())[0]
                try:
                    pp = self.exts.get(key).get("script").Run(self.methods)
                    if isinstance(pp, dict):
                        self.web_running_data.update(pp)
                        self.run_web_plugin(key, self.web_running_data)
                except:
                    self.stackedWidget.currentWidget().__run__()
        except Exception:
            pass

    ####################### get line edit text and process it #######################
    def split_check(self, text: str):
        key, _ = self.get_kv(text)
        exts_keys = list(self.exts.keys())

        self.web.UIB_list_widget.clear()
        
        if self.win_setting.s.value("check_auto_complete", False, bool):
            List = list(self.exts.keys())
            List.extend(__keywords__)
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
            self.btn_ext.show()
            self.run_plugin(key)
            self.win_setting.extend_mode()

            if self.win_setting.s.value("check_history_storage", False, bool):
                self.update_history()

        else:
            self.running = ""
            self.set_sys_icon()
            self.web.set_html(f"<center><h3> {self.input.text()} </h3></center>")
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



            # results = pkg.find_in(self.input.text().strip(), pkg.user_home_dirs)
            # for k, v in results.items():
            #     icon = pkg.icon_types(v)
            #     item = pkg.add_item(self.web.UIB_list_widget, icon, k, v, font_size=9)
            #     self.web.UIB_list_widget.addItem(item)

            # def open_file(item):
            #     self.hide()
            #     QDesktopServices.openUrl(QUrl.fromUserInput(results.get(item.text())))

            # self.web.UIB_list_widget.blockSignals(True) 
            # self.web.UIB_list_widget.itemDoubleClicked.connect(open_file)
            # self.web.UIB_list_widget.blockSignals(False)

            # for i in exts_keys:
            #     try:
            #         if self.input.text().strip().lower() in i:
            #             icon = self.exts.get(i).get("icon")
            #             name = self.exts.get(i).get("json").get("name")
            #             item = pkg.add_item(self.web.UIB_list_widget, icon, name, "", font_size=9)
            #             self.web.UIB_list_widget.addItem(item)
            #     except Exception:
            #         pass
            
        # result = {}
        # for i in pkg.user_home_dirs:
        #     for j in glob(os.path.expanduser(os.path.expandvars(i)) + "*"):
        #         if self.input.text().strip().lower() in j.strip().lower():
        #             ty = get_type(j)
        #             try:
        #                 if not ty == None or ty:
        #                     # result[ty].append({os.path.splitext(os.path.split(j)[1])[0]: j})
        #                     result[ty]
        #                     item = pkg.add_item(self.web.UIB_list_widget, "", os.path.splitext(
        #                         os.path.split(j)[1])[0], j, font_size=9, enabled=True)
        #                     self.web.UIB_list_widget.addItem(item)

        #             except KeyError:
        #                 result[ty] = []
        #                 item = pkg.add_item(self.web.UIB_list_widget, "", ty, j, font_size=10, enabled=False, alignment=4)
        #                 self.web.UIB_list_widget.addItem(item)


    ###################### Get System Icon Linux/MacOS/Windows #############
    def set_sys_icon(self):
        # def_icon = base_dir + "icons/systems/" + self.get_platform + ".png"
        # self.btn_ext.setIcon(QIcon(def_icon))
        self.btn_ext.hide()

    ####################### Create new Stacked Widget #######################
    def set_stacked_widget(self):
        self.stackedWidget = QStackedWidget(self)
        self.main_grid_layout.addWidget(self.stackedWidget)

    def reload_web_plugin(self):
        self.stackedWidget.currentWidget().web_veiw.reload()

    ####################### Run/Set Plugin Code #######################
    def run_plugin(self, key: str):
        plugin = self.exts.get(key)
        def_icon = plugin.get("icon")
        try:
            pp = plugin.get("object")(self.methods)

            ############ Fast Code ############
            self.btn_ext.setIcon(QIcon(def_icon if os.path.exists(
                def_icon) else base_dir + "icons/main/unknow.png"))

            _w = self.stackedWidget.currentWidget()

            if isinstance(pp, dict):
                ## Qt Web View
                self.web_running_data = pp
                self.run_web_plugin(key, pp)

            elif isinstance(pp, list) or isinstance(pp, tuple):
                ## Qt List Widget Item
                if _w == None or not getattr(_w, "__type__", "") == "item":
                    self.stackedWidget.insertWidget(
                        0, UIBIPlugin(self, pp))
                else:
                    _w.func = pp
                    _w.init_ui(pp)
            else:
                ## Qt Widget
                if not key == self.running:
                    self.stackedWidget.insertWidget(0, pp)
                else:
                    if not self.running == "err":
                        setattr(_w, "parent", self.methods)
                        _w.init_ui()

            self.stackedWidget.setCurrentIndex(0)
            self.running = key
            self.running_widget_type = getattr(_w, "__type__", "")

            ############ Slow Code ############
            # if isinstance(pp, dict):
            #     self.stackedWidget.insertWidget(0, KWPlugin(self, pp, plugin))
            # else:
            #     self.stackedWidget.insertWidget(0, pp)
            # self.stackedWidget.setCurrentIndex(0)

        except Exception as plug_err:
            print(plug_err)
            # widget = PluginException()
            # widget.add_item(base_dir + "icons/main/delete.png",
            #                 f"{key} was Crashed!", 
            #                 str(plug_err), key)

            # self.stackedWidget.insertWidget(0, widget)
            # self.stackedWidget.setCurrentIndex(0)
            # self.running = "err"


    def run_web_plugin(self, key, data):
        # self.web.run_plugin(data)
        self.web.UIB_list_widget.clear()
        self.web.init_ui(data)

        icon = self.exts.get(key).get("icon")
        if not os.path.exists(icon):
            icon = base_dir + "icons/main/unknow.png"

        item = pkg.add_item(self.web.UIB_list_widget, 
            QIcon(icon),
            data.get("title", ""),
            enabled=True, 
            font_size=9)

        self.web.UIB_list_widget.addItem(item)
        self.web.UIB_list_widget.setCurrentItem(item)

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

    ####################### Create System Tray #######################
    def createActions(self):
        self.hideAction = QAction("Toggle Window", self, shortcut="Alt+Space", triggered=self.check_win)
        self.quitAction = QAction(pkg.get_sys_icon("application-exit"), "&Quit", self, triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)

        self.trayIconMenu.addAction(self.hideAction)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(QIcon(base_dir + "icons/logo.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)

        self.trayIcon.activated.connect(self.check_win)

    def showMessage(self, title: str, body: str, icon: int=1, limit: int=5):
        tray = QSystemTrayIcon(QIcon(base_dir + "icons/logo.png"))
        icon_ = tray.MessageIcon(icon)
        tray.showMessage(title, body, icon_, limit * 2000)
        tray.show()

    def check_win(self):
        if self.isHidden():
            self.show()
            self.setFocus()
            self.input.setFocus()
            self.input.selectAll()
        else:
            self.hide()

    ######################### Creaet Plugin for User ################################3
    def create_plugin(self):
        import shutil
        
        _, v = self.get_kv(self.input.text())
        dic = {
            "items": "plugin_items",
            "witems": "plugin_widget_items",
            "widget": "plugin",
            "web": "plugin_web_view",
            "browser": "plugin_web_browser"
        }

        open_file = dialog.UIBDialog(self)
        dir_name = open_file.get_save_dir("UIBox - Create Plugin save path", os.path.expanduser("~"))
        
        try:
            if dir_name and os.path.exists(dir_name):
                save_plugin = dir_name.rstrip("/") + "/" + dic.get(v) + ".ext"
                shutil.copytree(f"create_plugin/{dic.get(v)}", save_plugin)
                # self.input.setText(f"@test {save_plugin}/main.py ")
                QDesktopServices.openUrl(QUrl().fromUserInput(save_plugin))
        except (FileExistsError, KeyError):
            pass
            
################## List Item Widget ######################
class PluginException(QWidget, list_item.UIBUi_List):
    __type__ = "err"

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)


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









"""
@Alfred
@Ulauncher
@Albert
@Spolight
@Flashlight
"""

"""
@UIBox Requirements:
########### Hardware ###########
Memory: >= 6GB
CPU   : >= Core i3
GPU   : >= 

########### Software ###########
Python: >= v3.7
PyQt5 : >= 15.12
psutil: >= 5.7.2

########### System Support ###########
Linux: 
    - Ubuntu : >= 19.4
    - Windows:
    - MacOS  :

@Questions:
    Why do we need UIBox?
    How I can use UIBox?
    What the UIBox Plugins?
    Get Start with UIBox?
    How to create UIBox Plugin?
    What rules for creating UIBox plugins?
"""
