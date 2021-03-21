#!/usr/bin/python3

import os
import json
import shutil

from glob import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

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
        self.p.t_btn_del.clicked.connect(self.deleting_theme)
        self.p.search_theme.textChanged.connect(self.set_theme_items)

    def get_all_themes(self):
        for p in glob(base_dir + "../extensions/__themes__/*.thm/"):
            pp = (p.split("..")[0].rstrip("settings/"))
            ps = pp + p.split("..")[1]

            icon = ps + self.get_info(ps, "icon", "Icon.png")
            if not icon or not os.path.exists(icon) or not os.path.isfile(icon):
                icon = pp + "/icons/logo.png"

            screenshot = ps + "Screenshot.png"
            if not os.path.exists(screenshot):
                screenshot = pp + "/icons/logo.png"

            style = self.get_info(ps, "style", "").strip()

            if style and style.endswith((".qss", ".css")) and self.get_info(ps, "type"):
                self.Styles.update({self.get_info(ps, "name", "No Name"): #os.path.splitext(os.path.split(ps + style)[1])[0] 
                {
                    "path": pp, 
                    "json": json.load(open(ps + "info.json")),
                    "screenshot": screenshot,
                    "style": ps + self.get_info(ps, "style"),
                    "icon": icon,
                    "style_path": ps
                }})

    def get_info(self, _path: str, key: str, default=None):
        return json.load(open(_path + "info.json", "r")).get(key, default)

    def set_theme_items(self, text: str=""):
        self.p.list_widget_theme.clear()
        for _, v in self.Styles.items():
            att = QListWidgetItem()

            if text.strip().lower() in v.get("json").get("name", "").lower() or not text.strip():
                att.setText(v.get("json").get("name", ""))
                att.setIcon(QIcon(v.get("icon")))

                self.p.list_widget_theme.addItem(att)

    def set_theme_info(self):
        item = self.p.list_widget_theme.currentItem()
        data = self.Styles.get(item.text())

        self.p.theme_screenshot.setPixmap(QIcon(data.get("screenshot")).pixmap(630, 320))
        self.p.tcr_name.setText(data.get("json").get("creator_name"))
        self.p.theme_type.setText(data.get("json").get("type"))
        self.p.tcr_url.setText(self.get_url(data.get("json").get("creator_url")))
        self.p.tcr_email.setText(self.get_url(data.get("json").get("creator_email")))
        self.p.tcr_home_page.setText(self.get_url(data.get("json").get("creator_home_page")))

        html = """
        <font size='4'>%s</font><br> 
        &nbsp;<font size='2'>Version %s</font><br><br>
        """ % (
            data.get("json").get("name", "UnKnow Name"),
            data.get("json").get("version", "1.0.0")
        )

        self.p.theme_top_data.setText(html)
        self.p.theme_icon.setIcon(QIcon(data.get("icon")))

    def get_url(self, text: str):
        return "<a href='%s'> %s </a>" % (text, text)

    def applay_theme(self, theme_name: str=""):
        item = self.p.list_widget_theme.currentItem()
        style = self.Styles.get(item.text() if not theme_name else theme_name).get("style")
        self.p.setting.setValue("theme", style)

    def deleting_theme(self):
        item = self.p.list_widget_theme.currentItem()
        data = self.Styles.get(item.text())

        msgBox = QMessageBox(self.p)

        msgBox.setWindowIcon(QIcon(data.get("path") + "/icons/logo.png"))
        msgBox.setIconPixmap(item.icon().pixmap(50, 50))
        msgBox.setWindowTitle(f"Theme Delete - {item.text()}")
        msgBox.setText(f"""\
                        {item.text()[0:64]}<br>\
                        &nbsp;<font size='1' color='#ffffff'>Version {data.get("json").get("version", "1.0.0")} \
                        </font></sub><br><br>
                        You are sure you wnat to delete this theme ?
                        """)

        msgBox.addButton(QMessageBox.Cancel)
        msgBox.addButton(QMessageBox.Ok)
        msgBox.show()
        reply = msgBox.exec_()

        if reply == QMessageBox.Ok:
            shutil.rmtree(data.get("style_path"))
            self.set_theme_items()
