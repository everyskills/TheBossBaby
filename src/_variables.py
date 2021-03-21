#!/usr/bin/python3

import os
import re
import json

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class TBB_Variables:
    def __init__(self, parent=None) -> None:
        self.p = parent
        self.var_file = json.load(open(base_dir + "Json/vars.json"))

    def set_var_data(self):
        query = r"([a-zA-Z0-9_]+)(\s*=\s*|\s+)(.+)"
        if (patt := re.findall(query, self.p.methods.text)):
            for v in patt:
                if len(v) == 3 and str(v[0]).strip() and str(v[2]).strip():
                    val = self.get_var_data(v[2])
                    self.var_file.update({v[0]:{
                        "name": v[0],
                        "type": "str" if not self.is_json(val) else "json",
                        "value": val if not self.is_json(val) else json.loads(val)
                    }})

            with open(base_dir + "Json/vars.json", "w") as _jf:
                _jf.write(json.dumps(self.var_file, indent=4))

    def is_json(self, v):
        return (v.startswith(("{", "[")) and v.endswith(("}", "]")))

    def get_json_value(self, var: str):
        if self.var_file.get(var, ""):
            return self.var_file.get(var)
        else:
            return {}

    def get_split_text(self, split):
        t = ""
        for i in split:
            t += i + " "
        return t.strip()

    def get_var_data(self, text: str=""):
        query = r"\${\s*([a-zA-Z0-9_.\[\]\"']+)\s*}"
        text = self.p.methods.text if not text else text
        patt = re.findall(query, text)

        for v in patt:
            vs = v.strip()
            try:
                if len(vs.split(".")) > 1:
                    var = vs.split(".")
                    results = eval(f"type('{var[0]}', (), {self.get_json_value(var[0]).get('value', {})}).{self.get_split_text(var[1:])}")
                elif len(vs.split("[")) > 1:
                    var = vs.split("[")
                    results = eval(f"{self.get_json_value(var[0]).get('value', [])}[{self.get_split_text(var[1:])}")
                else:
                    results = str(self.get_json_value(v).get("value", ""))

                text = re.sub(r"\${\s*(%s)\s*}" % re.escape(v), str(results), text)

            except Exception as err:
                # print("VAR-error: ", err)
                continue

        return text
