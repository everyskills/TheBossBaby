#!/usr/bin/python3

import json
import os

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollArea, QSizePolicy, QSpacerItem, QWidget

########### Import Types #############
from .Widgets.tbb_input import UIB_Input_type
from .Widgets.tbb_select import UIB_Select_type
from .Widgets.tbb_check import UIB_Check_type
from .Widgets.tbb_text import UIB_Text_type
from .Widgets.tbb_num import UIB_Num_type
from .Widgets.tbb_dialog import UIB_Dialog_type

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class PluginSettings:
    def __init__(self, parent=None) -> None:
        super(PluginSettings, self).__init__()

        self.p = parent

        self.settings_object = {}
        self.settings_file_location = {}
        self.settings_save_file_location = ""
        self.plugin_scrollArea_deleted = False

        self.dic_types = {
            "input": UIB_Input_type,
            "select": UIB_Select_type,
            "choose": UIB_Select_type,
            "check": UIB_Check_type,
            "text": UIB_Text_type,
            "kw": UIB_Input_type,
            "keyword": UIB_Input_type,
            "num": UIB_Num_type,
            "int": UIB_Num_type,
            "float": UIB_Num_type,
            "double": UIB_Num_type,
            "dialog": UIB_Dialog_type
        }
        
        self.create_scroll_area()

    def create_scroll_area(self):
        self.plugin_scrollArea = QScrollArea(self.p.tab)
        self.plugin_scrollArea.setObjectName(u"plugin_scrollArea")
        self.plugin_scrollArea.setMouseTracking(True)
        self.plugin_scrollArea.setFrameShape(QFrame.NoFrame)
        self.plugin_scrollArea.setFrameShadow(QFrame.Plain)
        self.plugin_scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 718, 584))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plugin_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.p.gridLayout_18.addWidget(self.plugin_scrollArea, 0, 0, 1, 3)

    def set_plugin_settings(self):
        self.create_scroll_area()
        for k, v in self.get_all_json().items():
            if v.get("type", "") and self.dic_types.get(v.get("type", "")):
                self.dic_types.get(v.get("type"))(self, str(k).strip(), v)
            else:
                continue

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer_5)

    def get_all_json(self):
        if not os.path.exists(self.settings_save_file_location):
            return self.settings_object
        else:
            data = self.settings_object
            data.update(json.load(open(self.settings_save_file_location)))
            return data

    def get_json(self, key: str, default: object=None):
        if not os.path.exists(self.settings_save_file_location):
            return self.settings_object.get(key, default)
        else:
            data = self.settings_object
            data.update(json.load(open(self.settings_save_file_location)))
            return data.get(key, default)

    def edit_settings(self, id: str, new_data: dict):
        data = self.get_all_json()
        data.get(id).update(new_data)

        with open(self.settings_save_file_location, "w") as _fw:
            _fw.write(json.dumps(data, indent=4))

    def reset_to_default(self):
        with open(self.settings_save_file_location, "w") as _fw:
            _fw.write(str(json.dumps(self.settings_file_location, indent=4)))

        self.plugin_scrollArea.deleteLater()
        self.set_plugin_settings()
