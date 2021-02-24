#!/usr/bin/python3

# import os
# import json

# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QAction, QApplication, QStyleFactory

# base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

# __app_name__ = "UIBox"
# __version__ = "1.3.6"
# __author__ = "Osama Muhammed Alzabidi"

# class MainWindowSettings:
#     def __init__(self, parent=None) -> None:
#         self.parent = parent
        
#         self.max_ext = 670
#         self.min_ext = 60
#         self.win_width = 720
#         self.is_auto_comp = False

    # def init_setup(self):
        # self.set_window_settings()

        # quitAction = QAction("Quit", self.parent, shortcut=self.kquit,
        #                     triggered=QApplication.instance().quit)

        # closeeAction = QAction("Hide", self.parent, shortcut=self.khide,
        #                     triggered=self.parent.hide)

        # focusAction = QAction("setFocus", self.parent, shortcut=self.klfocus,
        #                     triggered=self.parent.input.setFocus)

        # clearAction = QAction("clearText", self.parent.input, shortcut=self.kclear,
        #                     triggered=self.clear_input)

        # selectValueAction = QAction("selectPluginValue", self.parent.input, shortcut=self.kssp,
        #                         triggered=self.select_plugin_value)

        # clearValueAction = QAction("clearPluginValue", self.parent.input, shortcut=self.krmsp,
        #                             triggered=self.clear_plugin_value)

        # forwardCursor = QAction("ForewardCurosr", self.parent.input, shortcut=self.gte,
        #                            triggered=self.for_ward_cursor)

        # self.parent.input.addAction(forwardCursor)
        # self.parent.input.addAction(clearValueAction)
        # self.parent.input.addAction(selectValueAction)
        # self.parent.input.addAction(clearAction)
        # self.parent.input.addAction(focusAction)
        # self.parent.addAction(closeeAction)
        # self.parent.addAction(quitAction)
    
        # try:
        #     width = self.parent.screen().size().width()
        #     height = self.parent.screen().size().height()
        #     self.parent.move(width - width + 350, height - height + 80)
        # except AttributeError:
        #     pass

        # # self.parent.move(360, 60)
        # self.parent.setFixedSize(self.win_width, 320)
        # self.parent.setWindowFlags(self.parent.windowFlags()
        #                             | Qt.WindowStaysOnTopHint)

        # QApplication.instance().setApplicationName("Kangaroo")
        # QApplication.instance().setApplicationVersion("1.3.6")
        # QApplication.instance().setQuitLockEnabled(True)
        
        # self.parent.setWindowTitle("Kangaroo")
        # self.parent.setWindowIcon(QIcon(base_dir + "icons/logo.png"))
        # self.parent.input.setPlaceholderText("Kangaroo - search...")
        # self.parent.btn_setting.setIcon(QIcon(base_dir + "icons/main/search.svg"))
        # self.parent.input.setFocus()

    # def set_window_settings(self, data: str=""):
    #     with open(base_dir + "Json/settings.json", "r") as _fs:
    #         data = json.load(_fs) if not data else data

    #         self.style = base_dir + "styles/" + data.get("theme") + ".qss"

    #         # self.set_key(self.key_start_up, data.get("key_start_up", ""))
    #         self.kquit = data.get("key_quit")
    #         self.kclear = data.get("key_clear_input")
    #         self.krmsp = data.get("key_remove_split")
    #         self.khide = data.get("key_hide")
    #         self.klfocus = data.get("key_line_focus")
    #         self.kssp = data.get("key_select_split")
    #         self.gte = data.get("key_go_to_end")
            
    #         if os.path.exists(self.style):
    #             self.parent.setStyleSheet(open(self.style).read())
    #         else:
    #             self.parent.setStyleSheet("")
    #             QApplication.setStyle(QStyleFactory.create(data.get("theme")))

            # self.parent.setWindowOpacity(data.get("opacity"))

    #         self.max_ext = data.get("max_ext")
    #         self.min_ext= data.get("min_ext")
    #         self.win_width = data.get("window_width")
            
    #         self.parent.setFixedSize(self.win_width, 320)
    #         # self.check_launche.setChecked(data.get("is_launch_at_login"))
    #         # self.check_auto.setChecked(data.get("is_auto_check_update"))

    #         if data.get("is_rounded"):
    #             self.parent.setAttribute(Qt.WA_TranslucentBackground, True)

    #         if data.get("is_frame_less"):
    #             self.parent.setWindowFlags(
    #                 self.parent.windowFlags() 
    #                 | Qt.FramelessWindowHint)

    #         if data.get("is_shadow"):
    #             self.parent.setGraphicsEffect(self.parent.set_shadow(3, (2, 2), "black"))

    #         if data.get("is_hor_pattern"):
    #             self.parent.setWindowFlags(
    #                 self.parent.windowFlags() 
    #                 | Qt.HorPattern)

    #         if data.get("is_auto_complete"):
    #             self.is_auto_comp = True

    #         _fs.close()
    #         self.extend_mode()

    # def get_setting(self, key: str, value: str=""):
    #     return json.load(open(base_dir + "Json/settings.json", "r")).get(key, value)

    # def clear_input(self):
    #     self.parent.input.clear()
    #     self.parent.input.setFocus()

    # def select_plugin_value(self):
    #     k, v = self.parent.get_kv(self.parent.input.text())
    #     self.parent.input.setSelection(len(k) + 1 if v else 0, len(self.parent.input.text()))

    # def clear_plugin_value(self):
    #     k, v = self.parent.get_kv(self.parent.input.text())
    #     self.parent.input.setText(k + " " if v else "")

    # def small_mode(self):
    #     self.set_line_style(False)
    #     self.parent.setFixedHeight(self.min_ext)
    #     # self.parent.resize(QSize(self.parent.width(), self.min_ext))
    #     self.parent.KNG_main_frame.hide()

    # def extend_mode(self):
    #     self.set_line_style(True)
    #     self.parent.setFixedHeight(self.max_ext)
    #     # self.parent.resize(QSize(self.parent.width(), self.max_ext))
    #     self.parent.KNG_main_frame.show()

    # def default_mode(self):
    #     self.set_line_style(True)
    #     self.parent.setFixedHeight(180)
    #     # self.parent.resize(QSize(self.parent.width(), 180))
    #     self.parent.KNG_main_frame.show()

    # def extend_custom(self, value: int):
    #     self.set_line_style(True)
    #     self.parent.setFixedHeight(value)
    #     # self.parent.resize(QSize(self.parent.width(), value))
    #     self.parent.KNG_main_frame.show()
    
    # def for_ward_cursor(self):
    #     self.parent.input.setCursorPosition(len(self.parent.input.text()))

    # def set_line_style(self, show: bool=False):
    #     pass
        # style = os.path.splitext(os.path.split(self.style)[1])[0].strip().lower()
        # color = '777d7f' if 'dart' in style or style == 'default' else 'e6e6e6'
        # size = '2' if show else '0'
        # frsize = '10' if show else '0'

        # if not self.parent.running_widget_type == "item":
        #     self.parent.setStyleSheet(self.parent.styleSheet() +
        #         """ 
        #         #KNG_input_frame {
        #             border-bottom-color: #%s;
        #             border-bottom-width: %spx;
        #             border-bottom-style: solid;
        #             padding-bottom: 0px;
        #             margin-bottom: 0px;
        #         }
                
        #         #KNG_list_widget {
        #             border-right-color: #%s;
        #             border-right-width: %spx;
        #             border-right-style: solid;
        #             padding-top: 0px;
        #             margin-top: 0px;
        #         }

        #         #KNG_input_frame {
        #             padding-bottom: %spx;
        #         }
        #         """ % (color, size, color, size, frsize))

    # @property
    # def get_theme_name(self):
    #     return os.path.splitext(os.path.split(self.style)[1])[0].strip().lower()
