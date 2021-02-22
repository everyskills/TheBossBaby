#!/usr/bin/python3

import os
import shutil
import json

from kangaroo import pkg, item
from glob import glob
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtCore import QProcess, QSize, QThreadPool, QUrl, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, 
                            QFrame, QGridLayout, QLabel, QLineEdit, 
                            QMessageBox, QProgressBar, QSizePolicy, 
                            QStyleFactory, QTextEdit, QWidget)
from _downloader import UnzipWorker
from ui.setting_ui import Ui_Form

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")
setting_file = base_dir + "Json/settings.json"

class PluginSettings(QWidget, Ui_Form):
    def __init__(self, parent=None, win: object=None) -> None:
        super().__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)

        self.win = win
        self.bef_key = self.key.text().strip().lower()
        self.threadpool = QThreadPool()
        self.p = None
        self.get_plugin_name = ""

        self.btn_delete.setIcon(QIcon(base_dir + "icons/main/delete.png"))
        # self.btn_update.setIcon(QIcon())

        self.list_widget.itemSelectionChanged.connect(self.set_info)
        self.btn_delete.clicked.connect(self.remove_plugin)
        self.btn_update.clicked.connect(self.update_plugin)
        self.btn_help.clicked.connect(self.plugin_help_page)
        self.btn_plugin_page.clicked.connect(self.plugin_page)
        self.btn_down.clicked.connect(self.install_url)

        self.btn_save.clicked.connect(self.set_settings)
        self.btn_default.clicked.connect(self.set_default_settings)
        self.btn_apply.clicked.connect(lambda: self.set_settings(True))

        # self.win.input.textChanged.connect(self.query_exts)
        self.win.input.returnPressed.connect(self.check_page)

        _, self.val = self.win.get_kv(self.win.input.text().strip())
        self.val = self.val.strip().lower()

        if not len(self.val) > 1:
            self.query_exts()
        else:
            self.start_up()

    def query_exts(self):
        for k, v in self.win.exts.items():
            if ((self.val in k.lower() or 
                self.val in v.get("json").get("name", "").lower())
                or not self.val):
                
                self.set_info(k)
                icon = base_dir + "icons/unknow_plugin.png"
                list_item = pkg.add_item(self.list_widget, 
                QIcon(v.get('icon', '') if os.path.exists(v.get('icon')) else icon))
                
                item_widget = pkg.add_item_widget(
                    list_item, 
                    item.KUi_Item,
                    v.get("json").get("name", "")[0:64], 
                    v.get("json").get("description", "")[0:64],
                    k)
                pkg.set_item_widget(self.list_widget, item_widget)

    def check_download(self):
        url = self.url_path.text().strip().replace("file://", "")
        down_path = "exts/__download__/"

        if os.path.exists(url) and url.endswith(".zip"):
            self.load_progress_down.show()
            shutil.copy2(url, base_dir + down_path)
            self.unzip_file(base_dir + f"{down_path}{os.path.split(url)[1]}")

        elif url.endswith(".git"):
            self.load_progress_down.hide()
            self.get_plugin_name = url.split("/")[-1].rstrip(".git")
            self.start_process("git clone " + url + " " + base_dir +
                               f"{down_path}{self.get_plugin_name}.ext")

        elif os.path.exists(url) and not os.path.isfile(url):
            dirn = url.rstrip("/").split("/")[-1]
            shutil.copytree(url, (base_dir + down_path + dirn) + ".ext" if not dirn.endswith(".ext") else "")
            self.setup_downloaded_plugin()
        
        elif (os.path.exists(url) and not 
            os.path.isdir(url) and 
            url.endswith(".qss")):
            
            try:
                shutil.copy2(url, base_dir + "styles/")
            except shutil.Error:
                pass
            
            self.message(f"<font size='4' color='white'>Theme {os.path.splitext(os.path.split(url)[1])[0]}:\
                </font> <font size='4' color='green'>Fininshed Installed.</font>")

    def setup_downloaded_plugin(self):
        for i in glob(base_dir + "exts/__download__/*.ext/"):
            try:
                with open(i + "package.json", "r") as _f:
                    data = json.load(_f)
                    if (os.path.exists(i + data.get("script")) and
                        data.get("key").strip() and not 
                        data.get("key") in list(self.win.exts.keys()) and
                        data.get("system").strip()):

                        shutil.move(i.rstrip("/"), base_dir + f"exts/__{data.get('system')}__/")
                        
                        list(map(lambda x: os.remove(x), glob(base_dir + "exts/__download__/*")))
                        self.message(f"<font size='4' color='white'>{data.get('name')}:\
                            </font> <font size='4' color='green'>Install is Finished.</font><br>\
                            Press 'Ctrl+Q' for Exit")
            except shutil.Error:
                self.message(f"{data.get('name')}: is Already exists !")
            except (FileExistsError, TypeError, AttributeError):
                self.del_perr(i)

    def del_perr(self, _path):
        self.message(f"<font size='4' color='white'>Error:\
                        </font> <font size='4' color='red'>This not Kangaroo Plugin</font><br>\
                        Press 'Ctrl+Q' for Exit")
        shutil.rmtree(_path)

    def unzip_file(self, url: str):
        # Load the zipfile and pass to the worker which will extract.
        self.get_plugin_name = url.split("/")[-1].rstrip(".ext")
        self.worker = UnzipWorker(os.path.expanduser(os.path.expandvars(url)))
        self.worker.signals.progress.connect(self.update_progress)
        self.worker.signals.finished.connect(self.unzip_finished)
        self.worker.signals.error.connect(self.unzip_error)
        self.update_progress(0)

        self.threadpool.start(self.worker)
        self.worker = None  # Remove the worker so it is not double-triggered.

    def update_progress(self, pc):
        """
        Accepts progress as float in
        :param pc: float 0-1 of completion.
        :return:
        """
        current_n = int(pc * 10)
        self.load_progress_down.setValue(current_n // 10 * 100)
        
    def unzip_finished(self):
        self.setup_downloaded_plugin()

    def unzip_error(self, err):
        exctype, value, traceback = err
        self.update_progress(1)  #  Reset the Pez bar.
        dlg = QMessageBox(self)
        dlg.setText(traceback)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def check_page(self):
        if self.val in ("about", "kangaroo"):
            self.about_page()

        elif self.val in ("setting", "custom", "settings", "customs"):
            self.get_settings()
            self.settings_page()
        
        elif self.val in ("help", "helpme", "readme"):
            self.help_page()

    def install_url(self):
        self.Dialog = QDialog(self)
        self.Dialog.resize(432, 234)
        self.gridLayout = QGridLayout(self.Dialog)
        self.label_27 = QLabel(self.Dialog)
        self.label_27.setText("Plugin URL: ")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.label_27, 0, 0, 1, 1)

        self.load_progress_down = QProgressBar(self.Dialog)
        self.gridLayout.addWidget(self.load_progress_down, 2, 0, 1, 2)

        self.url_path = QLineEdit(self.Dialog)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.url_path.sizePolicy().hasHeightForWidth())
        self.url_path.setSizePolicy(sizePolicy1)
        self.url_path.setPlaceholderText("https://www.github.com....git or *.zip")
        self.url_path.setFrame(False)
        self.url_path.setStyleSheet("padding: 5px;")
        self.url_path.paste()
        self.url_path.returnPressed.connect(self.check_download)

        self.gridLayout.addWidget(self.url_path, 0, 1, 1, 1)

        self.output_text_edit = QTextEdit(self.Dialog)
        self.output_text_edit.setFrameShape(QFrame.NoFrame)
        self.output_text_edit.setFrameShadow(QFrame.Plain)
        self.output_text_edit.setReadOnly(True)

        self.gridLayout.addWidget(self.output_text_edit, 1, 0, 1, 2)
    
        self.Dialog.setWindowFlags(
            self.Dialog.windowFlags() 
            | Qt.FramelessWindowHint)
        
        self.Dialog.addAction(
            QAction("Q&uit", self.Dialog, shortcut="Ctrl+Q", triggered=self.close_dialgo))
        
        self.Dialog.show()
        self.win.hide()

    def close_dialgo(self):
        self.Dialog.close()
        self.win.show()

    def set_info(self, key: str=""):
        try:
            item = self.list_widget.currentItem()
            l_item = item.listWidget().itemWidget(item)
            plugin = l_item.shortcut.text()
        except AttributeError:
            plugin = key

        plug = self.win.exts.get(plugin).get("json")
        icon = self.win.exts.get(plugin).get("icon")
        
        if not os.path.exists(icon):
            icon = base_dir + "icons/unknow_plugin.png"

        self.plug_image.setPixmap(QIcon(icon).pixmap(QSize(60, 60)))
        self.plug_name.setText(f"""\
                                {plug.get("name", "")[0:64]} \
                                <sub><font size='2' \
                                color='#ffffff'>v{plug.get("version", "")} \
                                </font></sub>""")
        
        self.plug_desc.setText(plug.get("description", "")[0:120]) # limit 120 chrs
        self.key.setText(plug.get("key", ""))
        self.name.setText(plug.get("author_name", ""))
        self.email.setText(plug.get("author_email"))
        self.github.setText(f"https://www.github.com/{plug.get('github_user', '')}")
        self.home_page.setText(plug.get("home_page", ""))
        self.system.setText(plug.get("system", ""))
        self.sys_img.setPixmap(QIcon(base_dir + f"icons/systems/{plug.get('system')}.png").pixmap(QSize(30, 30)))
        
    def start_up(self):
        self.plug_image.setPixmap(QIcon(base_dir + "icons/logo.png").pixmap(QSize(60, 60)))
        self.plug_name.setText("Kangaroo  <sub><font size='2' color='#ffffff'>v1.0.0</font></sub>")
        # self.plug_name.setText("Kangaroo  <sub><font size='2' color='#000'>v1.0.0</font></sub>")
        self.plug_desc.setText("simple system lanuchers") # limit 120 chrs
        self.key.setText("kangaroo, kng")
        self.name.setText("Osama Muhammed Alzabidi")
        self.email.setText("everyskils@gmail.com")
        self.github.setText("https://www.github.com/everyskills")
        self.home_page.setText("https://www.everyskills.com")
        self.system.setText("Cross Platform")
        self.sys_img.setPixmap(QIcon(base_dir + "icons/logo.png").pixmap(QSize(30, 30)))

    def remove_plugin(self):
        msgBox = QMessageBox(self)
        
        icon = self.win.exts.get(self.key.text()).get('icon')
        plug = self.win.exts.get(self.key.text()).get('json')
        
        msgBox.setWindowIcon(QIcon(base_dir + "icons/logo.png"))
        msgBox.setIconPixmap(QIcon(icon if os.path.exists(
            icon) else base_dir + "icons/unknow_plugin.png").pixmap(QSize(50, 50)))
        msgBox.setWindowTitle(f"Plugin Delete - {plug.get('name', '')}")
        msgBox.setText(f"""\
                        {plug.get("name", "")[0:64]} \
                        <sub><font size='2' \
                        color='#ffffff'>v{plug.get("version", "")} \
                        </font></sub><br><br>
                        You are sure you wnat to delete this plugin ?
                        """)

        # msgBox.setWindowFlags(msgBox.windowFlags() | Qt.FramelessWindowHint)
        msgBox.addButton(QMessageBox.Cancel)
        msgBox.addButton(QMessageBox.Ok)
        # msgBox.setText(msgBox.text() + "<br>" + text)
        msgBox.show()
        reply = msgBox.exec_()

        if reply == QMessageBox.Ok:
            path = self.win.exts.get(self.key.text()).get("path")
            shutil.rmtree(path)
            self.parent.get_all_plugins()
            self.query_exts()
            
        elif reply == QMessageBox.Cancel:
            self.win.show()
        
    def update_plugin(self):
        pass

    def plugin_help_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def plugin_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def help_page(self):
        self.stackedWidget.setCurrentIndex(4)
        self.web_page.load(QUrl("https://www.google.com"))
        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)
        
        self.web_page.loadProgress.connect(self.change_progress)
        self.web_page.loadFinished.connect(self.load_progress.hide)

    def change_progress(self, value: int):
        if self.load_progress.isHidden():
            self.load_progress.show()
        self.load_progress.setValue(value)

    def about_page(self):
        icon = QIcon(base_dir + "icons/logo.png")

        self.about_title.setText("""\
        Kangaroo<br> <font size='2' color='#727272'>V1.3.6</font>\
        """)
        self.win.btn_ext.setIcon(icon)
        self.about_image.setPixmap(icon.pixmap(QSize(200, 200)))
        self.stackedWidget.setCurrentIndex(3)

    def settings_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def set_settings(self, apply: bool=False):
        dic = {}

        dic["key_start_up"] = self.get_key(self.key_start_up)
        dic["key_clear_input"] = self.get_key(self.key_clear_input)
        dic["key_remove_split"] = self.get_key(self.key_rm_split)
        dic["key_quit"] = self.get_key(self.key_quit_app)
        dic["key_hide"] = self.get_key(self.key_hide)
        dic["key_line_focus"] = self.get_key(self.key_line_focus)
        dic["key_select_split"] = self.get_key(self.key_select_split)
        dic["key_go_to_end"] = self.get_key(self.key_go_to_end)

        dic["theme"] = self.combo_themes.currentText().strip()
        dic["opacity"] = float(f'0.{self.slide_opacity.value()}' if not self.slide_opacity.value() == 10 else 1.0)
        dic["max_ext"] = self.max_ext.value()
        dic["min_ext"] = self.min_ext.value()
        dic["window_width"] = self.win_width.value()

        dic["is_launch_at_login"] = self.check_launche.isChecked()
        dic["is_auto_check_update"] = self.check_auto.isChecked()
        dic["is_rounded"] = self.check_round.isChecked()
        dic["is_frame_less"] = self.check_frame.isChecked()
        dic["is_shadow"] = self.check_shadow.isChecked()
        dic["is_hor_pattern"] = self.check_hor_pattern.isChecked()
        dic["is_auto_complete"] = self.check_auto_comp.isChecked()

        if not apply:
            with open(setting_file, "w") as _fsw:
                _fsw.write(str(json.dumps(dic, indent=4)))
                _fsw.close()
                self.win.win_setting.set_window_settings(dic)
        else:
            self.win.win_setting.set_window_settings(dic)

    def get_settings(self):
        with open(setting_file, "r") as _fs:
            data = json.load(_fs)

            self.set_key(self.key_start_up, data.get("key_start_up", ""))
            self.set_key(self.key_clear_input, data.get("key_clear_input", ""))
            self.set_key(self.key_rm_split, data.get("key_remove_split", ""))
            self.set_key(self.key_quit_app, data.get("key_quit", ""))
            self.set_key(self.key_hide, data.get("key_hide", ""))
            self.set_key(self.key_line_focus, data.get("key_line_focus", ""))
            self.set_key(self.key_select_split, data.get("key_select_split", ""))
            self.set_key(self.key_go_to_end, data.get("key_go_to_end", ""))

            for i in glob(base_dir + "styles/*.qss"):
                self.combo_themes.addItem(os.path.splitext(os.path.split(i)[1])[0])
            
            self.combo_themes.addItems(QStyleFactory.keys())
            self.combo_themes.setCurrentText(data.get("theme"))

            self.slide_opacity.setValue(data.get("opacity") * 10 if not int(data.get("opacity")) == 1 else 10)
            self.max_ext.setValue(data.get("max_ext"))
            self.min_ext.setValue(data.get("min_ext"))
            self.win_width.setValue(data.get("window_width"))

            self.check_launche.setChecked(data.get("is_launch_at_login"))
            self.check_auto.setChecked(data.get("is_auto_check_update"))
            self.check_round.setChecked(data.get("is_rounded"))
            self.check_frame.setChecked(data.get("is_frame_less"))
            self.check_shadow.setChecked(data.get("is_shadow"))
            self.check_hor_pattern.setChecked(data.get("is_hor_pattern"))
            self.check_auto_comp.setChecked(data.get("is_auto_complete"))
            
            _fs.close()

    def set_default_settings(self):
        _fr = open(base_dir + "Json/default_settings.json", "r")
        _fw = open(setting_file, "w")
        _fw.write(str(json.dumps(json.load(_fr))))

        _fr.close()
        _fw.close()

        self.set_settings(True)
        
    def get_key(self, obj):
        return obj.keySequence().toString()
    
    def set_key(self, obj, key: str):
        obj.setKeySequence(QKeySequence(key.strip()))  # set

    ############################ Github Downloader Methods ###############################
    def message(self, s):
        self.output_text_edit.insertHtml("<br>"*2 + s)

    def start_process(self, cmd: str):
        if self.p is None:  # No process running.
            self.message(
                "<font color='white' size='5'>Downloading Start</font>")
            # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            # Clean up once complete.
            self.p.finished.connect(self.process_finished)
            self.p.start(cmd)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: "<font color'red'>Not running",
            QProcess.Starting: "<font color='green'>Starting",
            QProcess.Running: "<font color='white'>Running",
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}</font>")

    def process_finished(self):
        self.setup_downloaded_plugin()
        self.message("<font color='white' size='5'>Download finished.</font><br>You can press 'Ctrl+Q' to close window now !")
        self.p = None

def main():
    app = QApplication([])
    win = PluginSettings()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
