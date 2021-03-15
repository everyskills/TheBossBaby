#!/usr/bin/python3

import json

class PluginSettings:
    def __init__(self, parent=None) -> None:
        super(PluginSettings, self).__init__()

        self.p = parent

    def set_plugin_setting_form(self):
        
        data = json.load(open(self._setting_file, "r"))

        template = ""

        self.p.plugin_settings_web.setHtml(template)