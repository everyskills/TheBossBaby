import json
import io
import os
import sys
import traceback
import zipfile

from PIL import Image
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

PROGRESS_ON = """
QLabel {
    background-color: rgb(233,30,99);
    border: 2px solid rgb(194,24,91);
    color: rgb(136,14,79);
}
"""

PROGRESS_OFF = """
QLabel {
    color: rgba(0,0,0,0);
}
"""

EXCLUDE_PATHS = [
    '__MACOSX/',
]

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    progress = pyqtSignal(float)


class UnzipWorker(QRunnable):
    '''
    Worker thread for unzipping.
    '''
    signals = WorkerSignals()

    def __init__(self, path):
        super(UnzipWorker, self).__init__()
        os.chdir(os.path.dirname(path))
        self.zipfile = zipfile.ZipFile(path)

    @pyqtSlot()
    def run(self):
        try:
            items = self.zipfile.infolist()
            total_n = len(items)

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in EXCLUDE_PATHS):
                    self.zipfile.extract(item)

                self.signals.progress.emit(n / total_n)

        except Exception as e:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            return

        self.signals.finished.emit()

class ZipInfo:
    def __init__(self, zip_path: str):
        
        self.zip_path = zip_path
        self.mzip = zipfile.ZipFile(zip_path)
        self.zip_files = self.mzip.infolist()

    def set_zip_path(self, zip_path: str):
        self.zip_path = zip_path

    def get_icon(self, save_path: str):
        icon = self.get_file_type("Icon.png")
        if icon:
            dataEnc = io.BytesIO(self.mzip.read(icon))
            img = Image.open(dataEnc)
            img.save(save_path + "Icon.png", "png")
            return img

    def get_screenshot(self, save_path: str):
        image = self.get_file_type("Screenshot.png")
        if image:
            data = self.mzip.read(image)
            dataEnc = io.BytesIO(data)
            img = Image.open(dataEnc)
            img.save(save_path + f"Screenshot.png", "png")
            return img

    @property
    def get_json(self):
        _file = self.get_file_type("info.json")
        if _file:
            data = json.load(self.mzip.open(_file))
            return data

    def get_file_type(self, name: str):
        for f in self.zip_files:
            _file = os.path.split(f.filename)[1]
            if _file.strip() == name.strip():
                return f.filename

