#!/usr/bin/python3

import os

from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtGui import QDesktopServices, QFont, QIcon
from UIBox import pkg, item

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class UserCommands:
    def __init__(self) -> None:
        pass

    def add_item(self, icon: str="", title: str="", tag: str="", hotkey: str=""):
        uib_item = item.UIBUi_Item()

        ret_color = (
            self.window.methods.light_color
            if self.window.methods.style == 'dark'
            else self.window.methods.dark_color)

        if not hotkey:
            hotkey = "<font size='4' color='%s'>⏎</font>" % ret_color

        if not tag.strip():
            uib_item.subtitle.hide()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 2, 1)
        else:
            uib_item.subtitle.show()
            uib_item.gridLayout.addWidget(uib_item.title, 0, 1, 1, 1)

        list_item = pkg.add_item(self.UIB_list_widget,
                                QIcon(icon), 
                                icon_size=(27, 27))

        item_widget = pkg.add_item_widget(list_item, uib_item, title, tag, hotkey, item_size=(260, 37))
        
        font = QFont()
        font.setPixelSize(12)
        item_widget[1].title.setFont(font)
        
        pkg.set_item_widget(self.UIB_list_widget, item_widget)

        return item_widget[0]

    def run_clicked_item(self):
        item = self.UIB_list_widget.currentItem()
        dic = {
            "web": self.web_type_code,
            "run": None,
            "app": None,
            "script": None
        }

        if not self.results.get(id(item)):
            self.run_plugin_item(item)
        else:
            data = self.results.get(id(item))
            key, val = self.window.get_kv(self.window.input.text())
            is_args = None

            try:
                if data.get("args", "").strip() == "yes" and val.strip() and key == data.get("keyword", ""):
                    is_args = True
                elif data.get("args", "").strip() == "no":
                    is_args = False
                
                if isinstance(is_args, bool):
                    dic.get(data.get("type", ""))(data, key, val, is_args)
                
                elif not key in list(self.window.exts.keys()):
                    self.window.input.setText(data.get("keyword", "") + " ")
                    self.window.input.setFocus()

            except Exception as err:
                print("USER-CMD-CLICKED: ", err)

    def set_list_items(self, _path: str="exts/__user__/*.wf/"):
        text = self.window.input.text().strip()
        key, _ = self.window.get_kv(self.window.input.text())

        self.UIB_list_widget.setGridSize(QSize(43, 43))

        ###################### Workflow List Item ######################
        # query = ""
        # for p in glob(base_dir + _path):
        #     data = json.load(open(p + "workflow.json"))
        #     wf_data = type("wf_data", (), data)
            
            # print(wf_data.workflow)

            # if data.get("args", "").strip() == "yes" and key == data.get("keyword"):
            #     query = self.window.methods.text

            # elif data.get("args", "").strip() == "no":
            #     query = text

            # icon = data.get("icon", p + "Icon.png")
            # if not os.path.exists(icon):
            #     icon = base_dir + "icons/main/unknow.png"

            # if (text.lower() in data.get("title", "").lower() or
            #     text.lower() in data.get("keyword", "").lower() or
            #     text.lower() in data.get("subtitle", "").lower() or
            #     key == data.get("keyword")):
            #     item = self.add_item(icon,
            #                         data.get("title", "").replace("{query}", query),
            #                         data.get("subtitle", "").replace("{query}", query))
            #     data.update({"icon": icon})
                
            #     self.results.update({id(item): data})


        ###################### Plugins List Item ######################
        for k in (self.window.exts.keys()):
            data = self.window.exts.get(k)

            if (text.lower() in data.get("json").get("name", "") or
                text.lower() in data.get("json").get("description") or
                text.lower() in k or key == k):

                if data.get("key_att", {}):
                    item = self.add_item(
                                        self.window.methods.include_file(data.get("key_att").get("icon")) or data.get("icon"),
                                        data.get("key_att").get("title", ""),
                                        data.get("key_att").get("subtitle", ""))
                else:
                    item = self.add_item(data.get("icon"),
                                        data.get("json").get("name", ""),
                                        data.get("json").get("description", ""))

                self.results.update({id(item): data})

    ######################## WEB Run Code #########################
    def web_type_code(self, data, key, val, is_args: bool):
        browser = data.get("browser", "default")

        def open_browser(url):
            if browser == "TBB-browser":
                pass
            elif browser == "default":
                QDesktopServices.openUrl(QUrl.fromUserInput(url))
            else:
                pkg.run_app(f"{browser} '{url}'")

        if is_args:
            url = data.get("url", "").replace("{query}", val.strip())
        else:
            url = data.get("url", "").replace("{query}", self.window.input.text().strip())

        open_browser(url)

    ######################## SCRIPT Run Code #########################
    def script_type_code(self):
        pass

    ######################## File Run Code #########################
    def run_type_code(self):
        pass

    ######################## APP Run Code #########################
    def app_type_code(self):
        pass
