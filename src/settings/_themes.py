#!/usr/bin/python3

import os
import json

from glob import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class ThemePage:
    def __init__(self, parent) -> None:
        super().__init__()

        self.p = parent
        self.Styles = {}
        self.get_all_themes()
        self.set_theme_items()

        self.p.list_widget_theme.itemSelectionChanged.connect(self.set_theme_info)
        self.p.btn_use_theme.clicked.connect(self.applay_theme)

    def get_all_themes(self):
        for p in glob(base_dir + "../styles/*.thm/"):
            pp = (p.split("..")[0].rstrip("settings/"))
            ps = pp + p.split("..")[1]

            style = self.get_info(ps, "style", "").strip()

            if style and style.endswith((".qss", ".css")) and self.get_info(ps, "type"):
                self.Styles.update({self.get_info(ps, "name", "No Name"): #os.path.splitext(os.path.split(ps + style)[1])[0] 
                {
                    "path": pp, 
                    "json": json.load(open(ps + "package.json")),
                    "image": self.get_info(ps, "image"),
                    "style": ps + self.get_info(ps, "style")
                }})

    def get_info(self, _path: str, key: str, default=None):
        return json.load(open(_path + "package.json", "r")).get(key, default)

    def set_theme_items(self):
        for _, v in self.Styles.items():
            att = QListWidgetItem()

            att.setText(v.get("json").get("name", ""))
            att.setIcon(QIcon(v.get("path") + "/icons/logo.png"))

            self.p.list_widget_theme.addItem(att)

    def set_theme_info(self):
        item = self.p.list_widget_theme.currentItem()
        data = self.Styles.get(item.text())

        self.p.image_theme.setPixmap(
            QIcon(data.get("image", data.get("path") + "/icons/logo.png")).pixmap(400, 300))

        self.p.tcr_name.setText(data.get("json").get("creator_name"))
        self.p.theme_type.setText(data.get("json").get("type"))
        self.p.tcr_url.setText(data.get("json").get("creator_url"))
        self.p.tcr_email.setText(data.get("json").get("creator_email"))
        self.p.tcr_home_page.setText(data.get("json").get("creator_home_page"))
    
    def applay_theme(self):
        item = self.p.list_widget_theme.currentItem()
        style = self.Styles.get(item.text()).get("style")
        self.p.setting.setValue("theme", style)
