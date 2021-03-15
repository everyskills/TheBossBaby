#!/usr/bin/python3

from UIBox import pkg
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class WorkFlow:
    def __init__(self, parent) -> None:
        super().__init__()

        self.p = parent
