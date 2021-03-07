#!/usr/bin/python3

import os
import sys

from UIBox import web
from _user_commands import UserCommands
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, QSize, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QFrame, QGridLayout, QListWidget, QProgressBar, QSizePolicy, QSplitter, QWidget

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ModuleNotFoundError:
    sys.path.insert(0, base_dir + '/modules/jinja2.zip')
    from jinja2 import Environment, FileSystemLoader, Template

"""
return: ⏎
shift: ⇧
ctrl: ⌘
alt: ⌥
"""

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-web-security"
                                            # "--blink-settings=darkMode=4"

class UIBUi_web(object):
    def setupUi(self, Form):
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        
        self.UIB_list_widget = QListWidget(self.frame_2)
        self.UIB_list_widget.setObjectName(u"UIB_list_widget")
        self.UIB_list_widget.setFrameShape(QFrame.NoFrame)
        self.UIB_list_widget.setFrameShadow(QFrame.Plain)
        self.UIB_list_widget.setIconSize(QSize(22, 22))
        self.UIB_list_widget.setGridSize(QSize(50, 50))
        self.UIB_list_widget.setWordWrap(False)
        self.UIB_list_widget.setSortingEnabled(True)

        self.UIB_web_frame = QFrame(Form)
        self.UIB_web_frame.setObjectName(u"UIB_web_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.UIB_web_frame.sizePolicy().hasHeightForWidth())
        self.UIB_web_frame.setSizePolicy(sizePolicy1)
        self.UIB_web_frame.setFrameShape(QFrame.NoFrame)
        self.UIB_web_frame.setFrameShadow(QFrame.Plain)

        self.UIB_web = QWebEngineView(self.UIB_web_frame)
        self.UIB_web.setObjectName(u"UIB_web")
        self.UIB_web.setUrl(QUrl(u"about:blank"))
        self.UIB_web.resize(300, 0)
        
        self.UIB_progress_bar = QProgressBar(self.UIB_web_frame)
        self.UIB_progress_bar.setObjectName(u"UIB_progress_bar")
        self.UIB_progress_bar.setMaximumSize(QSize(16777215, 15))
        self.UIB_progress_bar.setValue(24)

        self.UIB_splitter = QSplitter(Form)
        self.UIB_splitter.setHandleWidth(5)

        self.UIB_splitter.addWidget(self.UIB_list_widget)
        self.UIB_splitter.addWidget(self.UIB_web)

        self.gridLayout_2.addWidget(self.UIB_splitter)
        
        QWidget.setTabOrder(self.UIB_list_widget, self.UIB_web)
        self.UIB_progress_bar.hide()

class WebPage(QWebEnginePage):
    def __init__(self, table):
        QWebEnginePage.__init__(self)

        self._USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
        self.open_links_in_browser = False

    def javaScriptConsoleMessage(self, level: 'QWebEnginePage.JavaScriptConsoleMessageLevel', message: str, lineNumber: int, sourceID: str) -> None:
        # print(f"JS-Error: Line(%s), Source(%s): %s" % (lineNumber, sourceID, message))
        return super().javaScriptConsoleMessage(level, message, lineNumber, sourceID)

    def set_user_agent(self, agent: str):
        if agent.strip():
            self.profile().setHttpUserAgent(agent if agent.strip() else self._USER_AGENT)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if (_type == QWebEnginePage.NavigationTypeLinkClicked and self.open_links_in_browser):
            # and not url.toString() in url.toEncoded().data().decode()):
            QDesktopServices.openUrl(url)
            return False

        return super().acceptNavigationRequest(url,  _type, isMainFrame)

    # def javaScriptAlert(self, securityOrigin: QUrl, msg: str) -> None:
    #     # return super().javaScriptAlert(securityOrigin, msg)
    #     print("JS-Alert: Url(%s), Message(%s)" % (securityOrigin, msg))

class UIBWPlugin(QWidget, UIBUi_web, UserCommands):
    __type__ = "web"

    def __init__(self, window=None, func=None) -> None:
        QWidget.__init__(self)
        self.setupUi(self)     

        self.window = window
        self.func = func
        self.results = {}
        self.registeredObjects = {}
        
        self.default_jinja_vars = {
            "include_file": self.window.methods.include_file,
            "parent": self.window.methods
        }

        self.UIB_list_widget.itemSelectionChanged.connect(self.get_selected_info)

        web.get_webengine_settings()
        self.web_page = WebPage(self)
        self.channel = QWebChannel()

        self.UIB_web.page().setDevToolsPage(self.web_page)
        self.UIB_web.setPage(self.web_page)
        self.UIB_web.page().setWebChannel(self.channel)

        self.init_ui(self.func)

    def init_ui(self, func=None):
        if not func == None:
            if func.get("object", {}):
                objects = func.get("object", {"": DefaultApp()})
                self.web_page.open_links_in_browser = func.get("open_links_in_browser", True)

                if (not list(self.registeredObjects.keys()) == list(objects.keys()) or not self.registeredObjects):
                    self.channel.registeredObjects().clear()
                    self.channel.registerObjects(objects)
                    self.registeredObjects.update(objects)

            if func.get("web_args", ""):
            	os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] += " " + func.get("web_flags", "")
            
            self.run_plugin(func)

    def run_plugin_item(self, item, selected: bool=False):
        try:
            data = type("item", (), self.window.web_item_results.get(id(item), {}))
            key = self.window.running

            if not selected:
            	pp = self.window.exts.get(key).get("script").ItemClicked(self.window.methods, data)
            else:
            	pp = self.window.exts.get(key).get("script").ItemSelected(self.window.methods, data)

            if isinstance(pp, dict):
                pp.get("keywords", {}).update(self.window.web_running_data.get("keywords", {}))
                self.window.web_running_data.update(pp)
                self.window.run_web_plugin(self.window.exts.get(key).get(
                    "icon"), self.window.web_running_data, False if selected else True)

        except AttributeError:
            self.window.built_in_func()

    def get_selected_info(self):
        item = self.UIB_list_widget.currentItem()
        data = self.results.get(id(item))

        try:
            is_run = self.window.get_kv(self.window.input.text())[0]
            if not is_run in list(self.window.exts.keys()):
                # path = self.results.get(item.text())
                # icon = pkg.icon_types(path, [True, base_dir + "tmp/uibox_icon_type.png"])
                # keys = {}
                # if path.endswith((".pdf", ".mp4", ".mp3", ".jpg", ".png", ".jpeg", ".gif")):
                #     self.UIB_web.load(QUrl.fromUserInput(path))
                # else:
                #     keys["name"] = item.text()
                #     keys["icon"] = icon

                #     html = """
                #         <!DOCTYPE html>
                #         <html>
                #             <head>
                #                 <meta charset="utf-8">
                #                 <title></title>
                #             </head>

                #             <body>
                #                 <iframe src="{{file}}"> </iframe>
                #                 <h3> {{name}} </h3>
                #                 <img src='file://{{icon}}' />
                #             </body>

                #         </html>
                #     """
                #     self.set_html(self.get_jinja_template(html, keys))
                # self.window.btn_ext.setIcon(QIcon(icon))
                # pass

                desc = data.get("json", {}).get("description", "")
                name = data.get("json", {}).get("name", "")
                version = data.get("json", {}).get("version")
                key = data.get("json", {}).get("keyword", "")

                keys = {
                    "name": name if name else data.get("title"),
                    "icon": data.get("icon"),
                    "tag":  desc if desc else data.get("description"),
                    "version": version,
                    "style": "file://" + base_dir + "default_view/plugin.css",
                    "key": key if key else data.get("keyword"),
                    'color': 'black' if not self.window.methods.style == 'dark' else 'white',
                    'bg': self.window.methods.dark_color if self.window.methods.style == 'dark' else self.window.methods.light_color
                }

                html = self.get_jinja_template(open(base_dir + "default_view/plugin.html", "r").read(), keys)
                self.window.btn_ext.setIcon(QIcon(data.get("icon")))
                self.set_html(html)

            else:
                self.run_plugin_item(item, selected=True)

        except Exception as err:
            print(err)
            self.run_plugin_item(item, selected=True)

    def open_file(self, item, results):
        self.window.hide()
        QDesktopServices.openUrl(QUrl.fromUserInput(results.get(item.text())))

    def run_plugin(self, func):
        html = str(func.get("html"))
        if html.strip():
            self.web_page.set_user_agent(str(func.get("user_agent", "")))

            if func.get("jinja", False) and not func.get("template_dir", ""):
                html = self.get_jinja_template(open(html, "r").read() if os.path.exists(html) 
                                                else html, func.get("keywords", {}))
            elif func.get("template_dir", ""):
                html = self.get_jinja_template_env(func.get("template_dir", "templates"),
                                                   func.get("base_file", "index.html"), 
                                                   func.get("keywords", {}))
            self.set_html(html)

    ############ Check HTML return code type
    def set_html(self, html: str):
        try:
            if html.startswith(("http", "ftp", "tcp", "file")) or os.path.exists(html):
                self.UIB_web.load(QUrl.fromUserInput(html))
            else:
                tmp_path = base_dir + "tmp/plugin.html"
                with open(tmp_path, "w", encoding="utf-8") as _fw:
                    _fw.write(str(html))
                self.UIB_web.load(QUrl.fromUserInput(tmp_path))
        except Exception:
            pass

    def get_jinja_template_env(self, tmp_dir: str="templates", base: str="index.html", kwargs: dict={}):
        file_loader = FileSystemLoader(tmp_dir)
        env = Environment(loader=file_loader)
        template = env.get_template(base)
        kwargs.update(self.default_jinja_vars)
        output = template.render(kwargs)

        return output

    def get_jinja_template(self, html: str, kwargs: dict={}):
        tm = Template(html)
        kwargs.update(self.default_jinja_vars)
        return tm.render(kwargs)

class DefaultApp(QObject):
    def __init__(self) -> None:
        super().__init__()
