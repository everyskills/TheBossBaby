import os
import json
from glob import glob
from UIBox import pkg

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Get_All_Plugins:
    def __init__(self, parent=None) -> None:
        self.Plugins = glob(base_dir + f"exts/__{pkg.get_platform()}__/*.ext/")
        self.Plugins.extend(glob(base_dir + "exts/__all__/*.ext/"))
        self.count = 0
        self.p = parent
    
    def get_icon(self, _path: str, _json: dict):
        icon = _path + _json.get("icon", "Icon.png")
        if not icon or not os.path.exists(icon):
            icon = base_dir + "icons/main/unknow.png"
        return icon

    def get_data(self, _path: str, _json: dict):
        return {
            "path": _path,
            "json": _json,
            "icon": self.get_icon(_path, _json),
            "count": self.count,
            "script": pkg.Import(_path + _json.get("script", "plugin.py")),
            "object": pkg.Import(_path + _json.get("script", "plugin.py")).Results,
        }

    def get_keys(self, _path: str, _json: dict):
        for k in _json.get("keywords"):
            data = self.get_data(_path, _json)
            data.update({
                "keyword": k.get("key"),
                "key_att": k
            })
            self.p.exts.update({str(k.get("key")).strip().lower(): data})
            self.count += 1

    def get_key(self, _path: str, _json: dict):
        data = self.get_data(_path, _json)
        data.update({
            "keyword": str(_json.get("keyword")).strip().lower()
        })

        self.p.exts.update({
            str(_json.get("keyword")).strip().lower(): data
        })

        self.count += 1

    def get_plugins(self):
        for rd in self.Plugins:
            try:
                dic = json.load(open(rd + "info.json"))
                if dic.get("enabled", False):
                    
                    if dic.get("keywords", []) and isinstance(dic.get("keywords"), list):
                        self.get_keys(rd, dic)

                    elif dic.get("keyword", "") and isinstance(dic.get("keyword"), str):
                        self.get_key(rd, dic)

            except Exception as plug_err:
                print(f"Error-add: ({rd}): ", plug_err)
                continue
