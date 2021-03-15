#!/usr/bin/python3

import os

from PyQt5.QtWidgets import QApplication, QStyleFactory
from _downloader import Downloader

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Keyowrds:
    def __init__(self, parent=None) -> None:
        self.p = parent

        self.Keys = {
            "@install": (self.key_install, "install.svg"),
            "@settings": (self.key_settings, ""),
            "@dark": (self.key_dark, ""),
            "@light": (self.key_light, ""),
            "@style": (self.key_style, ""),
            "@quit": (self.key_quit, "exit.svg"),
            "@exit": (self.key_quit, "exit.svg"),
            "@hide": (self.key_hide, ""),
            "@small": (self.key_small, ""),
            "@extend": (self.key_extend, ""),
            "@clear-history": (self.key_clear_history, ""),
            "@reload": (self.key_reload, ""),
            "@post-msg": (self.key_post_msg, ""),
            "@larg-txt": (self.key_larg_txt, "")
        }

    def key_larg_txt(self, val):
        self.p.tbb_larg_text.larg_text(val)

    def key_post_msg(self, val):
        self.p.tbb_tray_icon.show_message(
            base_dir + "icons/logo.png", "TheBossBaby", val, 3)

    def key_settings(self, val):
        self.p.win_setting.open_setting_window()
        self.p.input.clear()

    def key_install(self, val):
        self.p.hide()
        Downloader().show()
        self.p.input.clear()

    def key_dark(self, val):
        self.p.win_setting.set_theme("Default Style")
        self.p.win_setting.init_setup()
        self.p.input.clear()

    def key_light(self, val):
        self.p.win_setting.set_theme("Light Style")
        self.p.win_setting.init_setup()
        self.p.input.clear()

    def key_style(self, val):
        def_styles = list(map(lambda x: x.lower(), QStyleFactory.keys()))

        if not val.lower() in def_styles:
            self.p.win_setting.set_theme(val)
        else:
            QApplication.setStyle(QStyleFactory.create(str(val).title()))

        self.p.win_setting.init_setup()
        self.p.input.clear()

    def key_quit(self, val):
        QApplication.instance().quit()

    def key_hide(self, val):
        self.p.hide()
        self.p.input.clear()
        self.p.win_setting.small_mode()

    def key_small(self, val):
        self.p.input.clear()
        self.p.win_setting.small_mode()

    def key_extend(self, val):
        self.p.input.clear()
        self.p.win_setting.extend_mode()

    def key_clear_history(self, val):
        fw = open(base_dir + ".history.kng", "w")
        fw.write("")
        fw.close()
        self.p.input.clear()

    def key_reload(self, val):
        ## reset plugins
        self.p.exts.clear()
        self.p.get_all_plugins()

        ## reset stacked widget
        self.p.stackedWidget.removeWidget(self.p.stackedWidget.widget(0))

        ## reset settings
        self.p.win_setting.init_setup()

        self.p.input.clear()
