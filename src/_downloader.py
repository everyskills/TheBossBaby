#!/usr/bin/python3

import os
import shutil

from glob import glob
from PyQt5.QtGui import QDragEnterEvent, QIcon
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from _unzip import UnzipWorker, ZipInfo
from ui.down import Ui_Form

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Downloader(QWidget, Ui_Form):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setAcceptDrops(True)        

        self.threadpool = QThreadPool()
        self.dragEnterEvent = self.drag_plugin
        self.screenshot.dragEnterEvent = self.drag_plugin
        self.plugin_file = ""

        self.screenshot.setStyleSheet("border: 1px dotted white; border-radius: 5px;")
        self.screenshot.setText("Drag Plugin Zip file here")

        self.btn_install.clicked.connect(self.start_unzip)
        self.btn_install.hide()
        self.progress_bar.hide()

    def unzip_file(self, url: str):
        # Load the zipfile and pass to the worker which will extract.
        self.progress_bar.show()

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
        self.progress_bar.setValue(current_n // 10 * 100)

    def unzip_finished(self):
        self.start_install()

    def unzip_error(self, err):
        _, _, traceback = err
        self.update_progress(1)  #  Reset the Pez bar.
        dlg = QMessageBox(self)
        dlg.setText(traceback)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def drag_plugin(self, event: QDragEnterEvent):
        data = event.mimeData()
        try:
            path = data.urls()[0].toLocalFile()
            if os.path.exists(path) and path.endswith(".zip"):
                event.setAccepted(True)
                self.btn_install.show()
                self.plugin_file = path
                self.set_plugin_info(path)
            else:
                event.setAccepted(False)
                self.btn_install.hide()
        except IndexError:
            pass

    def start_install(self):
        try:
            _down_path = base_dir + "extensions/__download__/" # exts -> extensions

            for i in glob(_down_path + "*"):
                if not os.path.isfile(i) and not i.endswith(".zip"):

                    if not self.info.get("style", ""):
                        _path = base_dir + \
                            f"extensions/__{self.info.get('system')}__/" + \
                            os.path.split(i)[1] + ".ext"

                        if os.path.exists(_path):
                            shutil.rmtree(_path)
                        shutil.move(i, _path)

                    else:
                        _path = base_dir + f"extensions/__themes__/" + os.path.split(i)[1] + ".thm"
                        if os.path.exists(_path):
                            shutil.rmtree(_path)
                        shutil.move(i, _path)

            os.remove(_down_path + os.path.split(self.plugin_file)[1])
            os.remove(base_dir + "tmp/Icon.png")
            os.remove(base_dir + "tmp/Screenshot.png")

        except Exception as err:
            print("Copy Error: ", err)

    def start_unzip(self):
        _down_path = base_dir + "extensions/__download__/"
        zip_down = _down_path + os.path.split(self.plugin_file)[1]
        if (
            self.info.get("settings") and
            self.info.get("script") and
            self.info.get("system")) or (
                self.info.get("type", "") and 
                self.info.get("style")):

            shutil.copy2(self.plugin_file, _down_path)
            self.unzip_file(zip_down)

    def set_plugin_info(self, url: str):
        self.zip_file = ZipInfo(url)

        icon = self.zip_file.get_icon(base_dir + "tmp/")
        screen = self.zip_file.get_screenshot(base_dir + "tmp/")

        self.info = self.zip_file.get_json
        html = """
        <font size='4'>%s</font><br> 
        &nbsp;<font size='2'>Version: %s</font><br><br>
        <font size='3'>%s</font>
        """ % (
            self.info.get("name", "UnKnow Name"),
            self.info.get("version", "1.0.0"),
            self.info.get("description", "")
        )

        if screen:
            self.screenshot.setPixmap(QIcon(base_dir + "tmp/Screenshot.png").pixmap(640, 400))            
        if icon:
            self.icon.setIcon(QIcon(base_dir + "tmp/Icon.png"))

        self.data.setText(html)

def main():
    app = QApplication([])
    win = Downloader()
    win.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
