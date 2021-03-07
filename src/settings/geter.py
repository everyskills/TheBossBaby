#!/usr/bin/python3

import os

from . import methods as mt
from PyQt5.QtCore import QSize
from UIBox import dialog, pkg
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.uic import loadUi
from ._themes import ThemePage
from ._plugins import PluginPage
from .path_item_ui import KUi_Form

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class SettingsWindow:
    def __init__(self) -> None:
        super().__init__()
    
        # self.parent = parent
        self.ui = loadUi(base_dir + "../ui/extend_setting.ui", self)
        self.dialog = dialog.UIBDialog()
        self.setting = mt.setting

        ################# Include Classes
        self.thm = ThemePage(self)
        self.plug = PluginPage(self)

        ################# get all value from setting file and put them in formas
        self.get_settings_value()

        ################## Events
        self.ui.window_opacity.sliderMoved.connect(self.set_window_opacity)

        ################# Clicked
        # self.ui.btn_color.clicked.connect(self.dialog_color)
        # self.ui.btn_font.clicked.connect(self.dialog_font)

        ############# QLineEdit TExt Changed
        mt.L_changed(self.ui.placeholder_text)
        mt.L_changed(self.ui.start_up_text)

        ############# QKeySequenceEdit TExt Changed
        ## Line page
        mt.K_changed(self.ui.key_focus_line_search)
        mt.K_changed(self.ui.key_clear_split_line_text)
        mt.K_changed(self.ui.key_select_split_line_text)
        mt.K_changed(self.ui.key_clear_line_text)

        ## Window page
        mt.K_changed(self.ui.key_toggle_window)
        mt.K_changed(self.ui.key_quit_app)
        mt.K_changed(self.ui.key_resize_to_small)
        mt.K_changed(self.ui.key_resize_to_larg)
        mt.K_changed(self.ui.key_extend_width)
        mt.K_changed(self.ui.key_zoomout_width)
        mt.K_changed(self.ui.key_extend_height)
        mt.K_changed(self.ui.key_zoomout_height)
        mt.K_changed(self.ui.key_open_settings)

        ############# QCheckBox Status Changed
        ## Line Page
        mt.C_changed(self.ui.check_history_storage)
        # mt.C_changed(self.ui.check_show_left_icon)
        # mt.C_changed(self.ui.check_show_right_icon)
        mt.C_changed(self.ui.check_auto_complete)

        ## Window page
        mt.C_changed(self.ui.check_auto_update)
        mt.C_changed(self.ui.check_auto_launche)
        mt.C_changed(self.ui.check_hor_pattern)
        mt.C_changed(self.ui.check_frameless)
        mt.C_changed(self.ui.check_round)
        mt.C_changed(self.ui.check_shadow)
        mt.C_changed(self.ui.check_show_left_icon)
        mt.C_changed(self.ui.check_show_right_icon)

        ############# QSpinBox Value Changed
        mt.S_changed(self.ui.window_width)
        mt.S_changed(self.ui.window_height)
        mt.S_changed(self.ui.window_max_extend)
        mt.S_changed(self.ui.window_min_extend)

        ############# QComboBox Value Changed
        mt.CB_changed(self.ui.window_style)

        # self.add_list_paths()

    ###################### Set Line Style 
    # def dialog_font(self):
    #     font = self.dialog.get_font()
    #     if not font == None:
    #         mt.setting.setValue("line_font_style", font)
    #         self.ui.btn_font.setFont(font)

    # def dialog_color(self):
    #     color = self.dialog.get_color()
    #     if not color == None:
    #         mt.setting.setValue("line_color_style", color.name())
    #         self.ui.btn_color.setStyleSheet("background: %s" % color.name())
    #         self.ui.btn_color.clearFocus()

    ###################### Drop & Drag Events
    # def drag_icon(self, e, obj):
    #     data = e.mimeData()
    #     path = data.urls()[0].toLocalFile()
        
    #     try:
    #         if os.path.exists(path) and path.endswith((".png", ".svg")):
    #             e.setAccepted(True)

    #             obj.setPixmap(QIcon(path).pixmap(150, 100))

    #             mt.setting.setValue(obj.objectName(), QIcon(path))

    #             obj.setStyleSheet("")

    #             shutil.copyfile(path, base_dir + f"icons/{obj.objectName()}{os.path.splitext(os.path.split(path)[1])[1]}")
    #         else:
    #             e.setAccepted(False)

    #     except shutil.SameFileError:
    #         pass

    # def clear_icon(self, e, obj):
    #     if obj == "l":
    #         self.set_default_left_icon()
    #         # self.ui.left_icon.setStyleSheet("border: 1px dashed white;")
    #         # self.ui.left_icon.setText("Drag Image")

    #     elif obj == "r":
    #         icon = QIcon("")

    #         self.ui.right_icon.setPixmap(icon.pixmap(0, 0))

    #         self.ui.right_icon.setStyleSheet("border: 1px dashed white;")

    #         mt.setting.setValue("rigth_icon", icon)

    #         self.ui.right_icon.setText("Drag Image")

    def get_settings_value(self):
        ########## Shortcutss
        mt.set_key_sequence(self.ui.key_focus_line_search, "Ctrl+F")
        mt.set_key_sequence(self.ui.key_clear_split_line_text, "Ctrl+B")
        mt.set_key_sequence(self.ui.key_select_split_line_text, "Ctrl+L")
        mt.set_key_sequence(self.ui.key_clear_line_text, "Ctrl+W")
        mt.set_key_sequence(self.ui.key_toggle_window, "Alt+Space")
        mt.set_key_sequence(self.ui.key_quit_app, "Ctrl+Q")
        mt.set_key_sequence(self.ui.key_resize_to_small, "Ctrl+Alt+-")
        mt.set_key_sequence(self.ui.key_resize_to_larg, "Ctrl+Alt+=")
        mt.set_key_sequence(self.ui.key_extend_width, "Ctrl+W+=")
        mt.set_key_sequence(self.ui.key_zoomout_width, "Ctrl+W+-")
        mt.set_key_sequence(self.ui.key_extend_height, "Ctrl+H+=")
        mt.set_key_sequence(self.ui.key_zoomout_height, "Ctrl+H+-")
        mt.set_key_sequence(self.ui.key_open_settings, "F1")

        ########## Text
        mt.set_text(self.ui.placeholder_text, "The Boss Baby - Go...")
        mt.set_text(self.ui.start_up_text, "")

        ########## SpinBoxs
        mt.set_spin_value(self.ui.window_width, 710)
        mt.set_spin_value(self.ui.window_height, 320)
        mt.set_spin_value(self.ui.window_max_extend, 670)
        mt.set_spin_value(self.ui.window_min_extend, 60)

        self.ui.window_opacity.setValue(mt.setting.value("window_opacity", type=float) * 10)

        ########### Check box
        mt.set_check(self.ui.check_history_storage, False)
        mt.set_check(self.ui.check_show_left_icon, True)
        mt.set_check(self.ui.check_show_right_icon, True)
        mt.set_check(self.ui.check_auto_complete, False)
        mt.set_check(self.ui.check_auto_update, True)
        mt.set_check(self.ui.check_auto_launche, True)
        mt.set_check(self.ui.check_hor_pattern, False)
        mt.set_check(self.ui.check_frameless, True)
        mt.set_check(self.ui.check_round, False)
        mt.set_check(self.ui.check_shadow, False)

        self.ui.window_style.addItems(QStyleFactory.keys())
        self.ui.window_style.setCurrentText(mt.setting.value(self.ui.window_style.objectName()))

    def set_window_opacity(self, value: int):
        mt.setting.setValue("window_opacity", float(
            f'0.{value}' if not value == 10 else 1.0))

    # def set_default_left_icon(self, key: str, path=""):
    #     icon = QIcon(base_dir + "icons/search.svg" if not path else path)
    #     self.ui.left_icon.setPixmap(icon.pixmap(150, 100))
    #     mt.setting.setValue(key, path)
    #     self.ui.left_icon.setStyleSheet("")


    # def add_list_paths(self):
    #     for i in range(10):
    #         item_widget = KUi_Form()
    #         item = pkg.add_item(self.list_widget_path, "")

    #         item.setSizeHint(QSize(60, 60))

    #         item_widget.btn_icon.setIcon(pkg.icon_types(item_widget.line_path.text().strip()))
    #         item_widget.line_path.setText(str(i))
    #         item_widget.setObjectName("line_path_%d" % i)

    #         self.list_widget_path.addItem(item)
    #         self.list_widget_path.setItemWidget(item, item_widget)

    #         item_widget.line_path.textChanged.connect(self.edited_path)

    # def edited_path(self, text):
    #     item = self.list_widget_path.currentItem()
    #     print(item)

def main():
    app = QApplication([])
    win = SettingsWindow()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()

