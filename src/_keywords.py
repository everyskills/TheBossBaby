#!/usr/bin/python3

import os
import json

from PyQt5.QtWidgets import QApplication, QStyleFactory
from _downloader import Downloader
from _variables import TBB_Variables
from plugin_item.index import UIBIPlugin

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Keyowrds:
    def __init__(self, parent=None) -> None:
        self.p = parent

        self.Keys = {
            "@install": {"func": self.key_install, "icon": "install.svg", "changed": True},
            "@installer": {"func": self.key_installer, "icon": "install.svg"},
            "@settings": {"func": self.key_settings},
            "@dark": {"func": self.key_dark},
            "@light": {"func": self.key_light},
            "@style": {"func": self.key_style},
            "@quit": {"func": self.key_quit, "icon": "exit.svg"},
            "@exit": {"func": self.key_quit, "icon": "exit.svg"},
            "@hide": {"func": self.key_hide, "icon": "hide.svg"},
            "@small": {"func": self.key_small, "icon": "small.svg"},
            "@extend": {"func": self.key_extend, "icon": "extend.svg"},
            "@reload": {"func": self.key_reload},
            "@post-msg": {"func": self.key_post_msg, "icon": "post-msg.svg"},
            "@larg-txt": {"func": self.key_larg_txt},   
            "@var": {"func": self.key_var, "icon": "var.svg"},
            # "@var": {"func": self.key_list_var, "icon": "var.svg", "changed": True},
            "@var-del": {"func": self.key_var_del, "icon": "var-del.svg"},
            "@clear-history": {"func": self.key_clear_history}
        }

    def key_larg_txt(self, val):
        self.p.tbb_larg_text.larg_text(val)

    def key_post_msg(self, val):
        self.p.tbb_tray_icon.show_message(0, "TheBossBaby", val, 3000)

    def key_settings(self, val):
        self.p.win_setting.open_setting_window()
        self.p.input.clear()

    def key_installer(self, val):
        self.p.hide()
        Downloader().show()
        self.p.input.clear()

    def key_install(self, val):
        tbb_downloader = Downloader()
        val = os.path.expandvars(os.path.expanduser(val))
        if os.path.exists(val) and val.endswith(".zip"):
            tbb_downloader.plugin_file = val
            tbb_downloader.set_plugin_info(val)

        self.p.stackedWidget.insertWidget(0, tbb_downloader)
        self.p.stackedWidget.setCurrentIndex(0)
        self.p.win_setting.extend_mode()

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
        self.p.tbb_get_all_plugins.get_plugins()

        ## reset stacked widget
        self.p.stackedWidget.removeWidget(self.p.stackedWidget.widget(0))

        ## reset settings
        self.p.win_setting.init_setup()

        self.p.input.clear()

    # def key_list_var(self, val):
    #     _w = self.p.stackedWidget.currentWidget()
    #     if not len(val.split("=")) > 1 or not len(val.split()) > 1:
    #         pp = []
    #         for k, v in self.p.tbb_vars.var_file.items():
    #             pp.append(
    #                 {
    #                     "icon": base_dir + "icons/keywords/var.svg",
    #                     "title": k,
    #                     "subtitle": f"Type: {v.get('type', '')}   Value: {v.get('value', '')}",
    #                     "key": v.get('value', ''),
    #                     "func": lambda p, i: self.p.input.setText(f"@var {i.title} = {i.key}"),
    #                     "ctrl_enter": lambda p, i: self.key_var_del(i.title),
    #                     "filter": True,
    #                     "highlightable": False,
    #                     "keep_app_open": True
    #                 }
    #             )

    #         if _w == None or not getattr(_w, "__type__", "") == "item":
    #             # print("added new item widget")
    #             self.p.stackedWidget.removeWidget(self.p.stackedWidget.widget(0))
    #             self.p.stackedWidget.insertWidget(0, UIBIPlugin(self.p, pp))
    #         else:
    #             # print("run item widget")
    #             _w.func = pp
    #             _w.init_ui(pp)
    #     else:
    #         self.p.stackedWidget.removeWidget(self.p.stackedWidget.widget(0))

    def key_var(self, val):
        tbb_vars = TBB_Variables(self.p)
        tbb_vars.set_var_data()
        self.p.tbb_vars.var_file = json.load(open(base_dir + "Json/vars.json"))

    def key_var_del(self, val):
        data = json.load(open(base_dir + "Json/vars.json"))
        data.pop(val, "")
        
        with open(base_dir + "Json/vars.json", "w") as _jf:
            _jf.write(json.dumps(data, indent=4))
        
        self.p.tbb_vars.var_file = json.load(open(base_dir + "Json/vars.json"))
