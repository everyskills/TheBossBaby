import os
import json
import shutil
import markdown

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from UIBox import pkg
from glob import glob
from ._plugin_settings import PluginSettings

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class PluginPage(PluginSettings):
    def __init__(self, parent) -> None:
        super(PluginPage, self).__init__(parent)

        self.p = parent
        self.results = {}

        self.plugins = glob(base_dir + f"../extensions/__{pkg.get_platform()}__/*.ext/")
        self.plugins.extend(glob(base_dir + "../extensions/__all__/*.ext/"))

        self.p.search_plugin.textChanged.connect(self.set_plugins)
        self.p.list_widget_plugin.itemSelectionChanged.connect(self.get_selected_item_data)
        self.p.btn_del.clicked.connect(self.deleting_plugin)
        self.p.check_pluging_is_enabled.stateChanged.connect(lambda: self.update_plugin_file(enabled=True))
        self.p.ps_btn_default.clicked.connect(self.reset_to_default)
    
        # self.p.btn_add.clicked.connect(Downloader().show)

        self.p.note_label.hide()
        self.p.btn_default.hide()
        self.p.btn_delete.hide()
        self.p.frame_9.hide()
        self.p.ps_btn_default.hide()
        self.set_plugins()

    def set_plugins(self, text: str=""):
        self.p.list_widget_plugin.clear()
        self.p.match_plugin.setText("Match (0) Plugins.")
        for p in self.plugins:
            try:
                pp = (p.split("..")[0].rstrip("settings/"))
                ps = pp + p.split("..")[1]
                _file = ps + "info.json"

                item = pkg.add_item(self.p.list_widget_plugin, 
                                    QIcon(self.get_plugin_icon(_file, pp, ps)), 
                                    str(self.get_js(_file, "name", "UnKnow Name")),
                                    str(self.get_js(_file, "description", "UnKnow Description")),
                                    font_size=13)

                if text.strip().lower() in str(self.get_js(_file, "name", "")).lower() or not text.strip():
                    self.p.list_widget_plugin.addItem(item)
                    self.results.update({id(item): _file})
                    self.p.match_plugin.setText("Match (%s) Plugins." % self.p.list_widget_plugin.count())

            except Exception as err:
                print(err)

    def get_plugin_icon(self, _file: str, _path: str, _plug_path: str):
        icon = _plug_path + str(self.get_js(_file, "icon", "Icon.png"))
        if not icon or not os.path.exists(icon):
            icon = _path + "/icons/main/unknow.png"
        return icon

    def get_js(self, _file: str, key: str, value: object=None):
        return json.load(open(_file, "r")).get(key, value)

    def get_url(self, text: str):
        return "<a href='%s'> %s </a>" % (text, text)

    def get_selected_item_data(self):
        item = self.p.list_widget_plugin.currentItem()
        self.p.cr_examples.clear()

        try:
            _file = self.results.get(id(item), "")
            html = """
            <font size='4'>%s</font><br> 
            &nbsp;<font size='2'>Version %s</font><br><br>
            <font size='3'>%s</font><br>
            """ % (
                str(self.get_js(_file, "name", "UnKnow Name")),
                str(self.get_js(_file, "version", "1.0.0")),
                str(self.get_js(_file, "description", "no Description"))
            )

            self._help_file = os.path.split(
                _file)[0] + "/" + str(self.get_js(_file, "help", "README.md"))

            self._setting_save_file = os.path.split(_file)[0] + "/" + ".settings.json"

            self.p.plugin_top_data.setText(html)
            self.p.plugin_icon.setIcon(item.icon())

            self.p.cr_email.setText(self.get_url(str(self.get_js(_file, "creator_email", "no Email"))))
            self.p.cr_url.setText(self.get_url(str(self.get_js(_file, "creator_url", "no URL"))))
            self.p.cr_home_page.setText(self.get_url(str(self.get_js(_file, "home_page", "no Home Page"))))
            self.p.cr_name.setText(str(self.get_js(_file, "creator_name", "no name")))
            self.p.check_pluging_is_enabled.setChecked(self.get_js(_file, "enabled", False))

            for i in list(self.get_js(_file, "examples", [])):
                self.p.cr_examples.insertHtml(str(i) + "<br>" * 1)

            ############# Tab Help ###########
            if os.path.exists(self._help_file):
                if self._help_file.endswith("md"):
                    with open(self._help_file) as _fr:
                        self.p.plugin_help_web.setHtml(markdown.markdown(_fr.read()))
                elif self._help_file.endswith(("html", "htm")):
                    self.p.plugin_help_web.load(self._help_file)
                else:
                    self.p.plugin_help_web.setHtml("")
            else:
                self.p.plugin_help_web.setHtml("")

            ############# Tab Settings ###########            
            if self.get_js(_file, "settings", {}):
                self.settings_object = self.get_js(_file, "settings", {})
                self.settings_file_location = self.get_js(_file, "settings", {})
                self.settings_save_file_location = self._setting_save_file

                self.plugin_scrollArea.show()
                self.plugin_scrollArea.deleteLater()
                self.set_plugin_settings()
                self.p.ps_btn_default.show()

            else:
                self.plugin_scrollArea.hide()
                self.p.ps_btn_default.hide()

        except Exception as err:
            print("Error-settings-item-selected: ", err)

    def update_plugin_file(self, text: str="", enabled: bool=False):
        _file = self.results.get(id(self.p.list_widget_plugin.currentItem()), "")
        if _file:
            data = json.load(open(_file))
            
            if enabled:
                data.update({"enabled": self.p.check_pluging_is_enabled.isChecked()})
            # else:
            #     data.update({"keyword": text.strip().lower()})

            with open(_file, "w") as _fw:
                _fw.write(str(json.dumps(data, indent=4)))


    def deleting_plugin(self):
        item = self.p.list_widget_plugin.currentItem()
        _file = self.results.get(id(self.p.list_widget_plugin.currentItem()), "")
        _path = os.path.split(_file)[0]

        msgBox = QMessageBox(self.p)

        msgBox.setWindowIcon(QIcon(base_dir + "icons/logo.png"))
        msgBox.setIconPixmap(item.icon().pixmap(50, 50))
        msgBox.setWindowTitle(f"Plugin Delete - {str(self.get_js(_file, 'name', ''))}")
        msgBox.setText(f"""\
                        {self.get_js(_file, "name", "")[0:64]}<br>\
                        &nbsp;<font size='1' color='#ffffff'>Version {str(self.get_js(_file, "version", ""))} \
                        </font></sub><br><br>
                        You are sure you wnat to delete this plugin ?
                        """)

        msgBox.addButton(QMessageBox.Cancel)
        msgBox.addButton(QMessageBox.Ok)
        msgBox.show()
        reply = msgBox.exec_()

        if reply == QMessageBox.Ok:
            shutil.rmtree(_path)
            self.set_plugins()
