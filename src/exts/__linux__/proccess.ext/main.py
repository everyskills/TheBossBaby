#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon
import psutil

from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.QtCore import QSize
from PyQt5.uic import loadUi

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def get_processes():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = {}
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
            # Fetch process details as dict
            svmem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe'])
            pinfo["vms"] = float(get_size(proc.memory_info().vms)[:-2]) / float(get_size(svmem.total)[:-2]) * 100
            pinfo["swap"] = float(get_size(proc.memory_info().shared)[:-2]) / float(get_size(swap.total)[:-2]) * 100
            pinfo["event"] = proc

            listOfProcObjects.update({pinfo.get("pid"): pinfo})
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    return listOfProcObjects


class Plugin(QWidget):
    def __init__(self, pkg, parent):
        super(Plugin, self).__init__()
        QWidget.__init__(self)

        self.pkg = pkg
        self.parent = parent

        self.ui = loadUi(base_dir + "UI.ui", self)

        self.ui.list_widget.itemSelectionChanged.connect(self.get_path_info)
        enterAction = QAction("enter", self, shortcut="Return", triggered=self.get_enter_item)
        
        self.btn_kill_proc.clicked.connect(self.kill_processe)
        self.btn_kill_proc.setIcon(QIcon(base_dir + "icons/dead.png"))

        self.ui.list_widget.addAction(enterAction)
        self.short_title(os.path.split(str(self.parent.get_text()).strip())[1])
        self.query_processes()

    def get_enter_item(self):
        self.add_click_path(self.ui.list_widget.currentItem())
        self.ui.list_widget.setFocus()

    def query_processes(self):
        self.ui.list_widget.clear()
        self.query = self.parent.get_text()

        for _, v in get_processes().items():
            name = v.get("name", "")
            _icon = self.pkg.get_sys_icon(name)
            if not _icon:
                _icon = QIcon(base_dir + "icons/executable.png")

            if (self.list_widget.count() <= 9 and self.query in name):
                frame = self.pkg.Import(base_dir + "item.py").Ui_Item
                item = self.pkg.add_item_widget(self.ui.list_widget, frame, _icon, name, '', str(v.get("pid")))
                self.pkg.set_item_widget(self.ui.list_widget, item)
            
            self.ui.status.setText(f"{self.list_widget.count()} Proccess")

    def get_path_info(self):

        self.prog_mem.setValue(0)
        self.prog_swap.setValue(0)

        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        # title = litem.title.text()
        # desc = litem.desc.text()
        pid = litem.shortcut.text()
        proc = get_processes()[int(pid)]

        self.title.setText(proc.get("name", ""))
        self.prog_mem.setValue(proc.get("vms"))
        self.prog_swap.setValue(proc.get("swap"))
        self.prog_cpu.setValue(proc.get("cpu_percent"))

        self.luser.setText(proc.get("username"))
        self.lpath.setText(proc.get("exe"))
        self.image.setPixmap( QIcon().fromTheme(proc.get("name")).pixmap(QSize(170, 170)) )

    def short_title(self, item: str):
        if len(item) <= 20:
            self.ui.title.setText(item)
        else:
            self.ui.title.setText(item[0:21] + "...")
    
    def kill_processe(self):
        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        pid = litem.shortcut.text()
        get_processes()[int(pid)].get("event").kill()
        self.query_processes()