import os
import json
from glob import glob
from UIBox import pkg

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Get_All_Plugins:
    def __init__(self, parent=None) -> None:
        self.Plugins = glob(base_dir + f"extensions/__{pkg.get_platform()}__/*.ext/")
        self.Plugins.extend(glob(base_dir + "extensions/__all__/*.ext/"))
        self.count = 0
        self.p = parent

    def get_icon(self, _path: str, _json: dict):
        icon = _path + _json.get("icon", "Icon.png")
        if not icon or not os.path.exists(icon):
            icon = base_dir + "icons/main/unknow.png"
        return icon

    def get_data(self, _path: str, _json: dict):
        obj = pkg.Import(_path + _json.get("script", "plugin.py"))
        return {
            "path": _path,
            "json": _json,
            "icon": self.get_icon(_path, _json),
            "count": self.count,
            "script": obj,
            "object": obj.Results
        }

    def get_keys(self, _path: str, _json: dict):
        _file = _path + ".settings.json"
        if os.path.exists(_file):
            settings = json.load(open(_file))
        else:
            settings = _json.get("settings", {})

        for sv in settings.values():
            if sv.get('type', '') in ("kw", "keyword"):
                data = self.get_data(_path, _json)
                data.update({
                    "keyword": sv.get("value", ""),
                    "key_att": sv
                })

                self.p.exts.update({str(sv.get("value", "")).strip().lower(): data})
                self.count += 1

    def get_plugins(self):
        for rd in self.Plugins:
            try:
                dic = json.load(open(rd + "info.json"))
                if dic.get("enabled", False):
                    self.get_keys(rd, dic)
    
            except Exception as plug_err:
                print(f"Error-add: ({rd}): ", plug_err)
                continue
