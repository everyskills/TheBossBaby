#!/usr/bin/python3

import os
import sys
import traceback
import zipfile

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


# class UrlDownloader:
    # def __init__(self, parent):
    #     super().__init__()

    #     self.parent = parent
    #     self.p = None

    # def message(self, s):
    #     self.parent.output_text_edit.setHtml(s)

    # def start_process(self, cmd: str):
    #     if self.p is None:  # No process running.
    #         self.message("<font color='white' size='5'>Executing process</font>")
    #         # Keep a reference to the QProcess (e.g. on self) while it's running.
    #         self.p = QProcess()
    #         self.p.readyReadStandardOutput.connect(self.handle_stdout)
    #         self.p.readyReadStandardError.connect(self.handle_stderr)
    #         self.p.stateChanged.connect(self.handle_state)
    #         # Clean up once complete.
    #         self.p.finished.connect(self.process_finished)
        
            # self.p.start(cmd)
            # self.p.start("git clone https://www.github.com/everyskills/Kangaroo.git /home/o_o/Projects/Ready/kangaroo-app/exts/__download__/Kangaroo")
        
    # def handle_stderr(self):
    #     data = self.p.readAllStandardError()
    #     stderr = bytes(data).decode("utf8")
    #     self.message(stderr)

    # def handle_stdout(self):
    #     data = self.p.readAllStandardOutput()
    #     stdout = bytes(data).decode("utf8")
    #     self.message(stdout)

    # def handle_state(self, state):
    #     states = {
    #         QProcess.NotRunning: "<font color'red'>Not running",
    #         QProcess.Starting: "<font color='green'>Starting",
    #         QProcess.Running: "<font color='>white'Running<",
    #     }
    #     state_name = states[state]
    #     self.message(f"State changed: {state_name}</font>")

    # def process_finished(self):
    #     self.message("<font color='white' size='5'>Process finished.</font>")
    #     self.p = None
