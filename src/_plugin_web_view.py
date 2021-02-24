#!/usr/bin/python3

import os
import sys

from UIBox import pkg, web
# from threading import Thread
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QObject, QSize, QUrl
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWidgets import QAction, QFrame, QGridLayout, QListWidget, QProgressBar, QSizePolicy, QSplitter, QWidget

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

sys.path.insert(0, base_dir + '/modules/jinja2.zip')
from jinja2 import Environment, FileSystemLoader, Template

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
        self.UIB_list_widget.setGridSize(QSize(38, 38))
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
        
        self.UIB_web = QWebView(self.UIB_web_frame)
        self.UIB_web.setObjectName(u"UIB_web")
        self.UIB_web.setUrl(QUrl(u"about:blank"))

        self.UIB_progress_bar = QProgressBar(self.UIB_web_frame)
        self.UIB_progress_bar.setObjectName(u"UIB_progress_bar")
        self.UIB_progress_bar.setMaximumSize(QSize(16777215, 15))
        self.UIB_progress_bar.setValue(24)

        self.UIB_splitter = QSplitter(Form)
        self.UIB_splitter.addWidget(self.UIB_list_widget)
        self.UIB_splitter.addWidget(self.UIB_web)
        self.gridLayout_2.addWidget(self.UIB_splitter)
        
        QWidget.setTabOrder(self.UIB_list_widget, self.UIB_web)
        self.UIB_progress_bar.hide()

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, message, line, source):
        if source:
            print('JS-Error: Line(%s), Source(%s): %s' % (line, source, message))
        else:
            print(message)

class UIBWPlugin(QWidget, UIBUi_web):
    __type__ = "web"

    def __init__(self, window=None) -> None:
        # super().__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)     

        self.window = window

        self.enterAction = QAction(
            "enter", 
            self.UIB_list_widget,
            shortcut="Ctrl+Return", 
            triggered=lambda: self.open_file(self.UIB_list_widget.currentItem(), 
                            pkg.find_in(self.window.input.text().strip(), pkg.user_home_dirs)))

        self.UIB_list_widget.addAction(self.enterAction)

        self.UIB_list_widget.itemDoubleClicked.connect(
            lambda item: self.open_file(item, 
            pkg.find_in(self.window.input.text().strip(), 
            pkg.user_home_dirs)))

        self.UIB_list_widget.itemSelectionChanged.connect(self.get_selected_info)

        self.init_ui()

    def init_ui(self, func=None):
        web.get_settings()

        self.web_page = WebPage(self)
        self.UIB_web.setPage(self.web_page)        
        # self.UIB_web.loadProgress.connect(self.check_progress_bar)

        if not func == None:
            self.run_plugin(func)

    def set_list_items(self):
        self.results = pkg.find_in(self.window.input.text().strip(), pkg.user_home_dirs)

        for k, v in self.results.items():
            icon = pkg.icon_types(v)
            item = pkg.add_item(self.UIB_list_widget, icon, k, v, font_size=9)
            self.UIB_list_widget.addItem(item)

    def get_selected_info(self):
        item = self.UIB_list_widget.currentItem()
        path = self.results.get(item.text())
        keys = {}
        try:
            icon = pkg.icon_types(path, [True, base_dir + "tmp/uibox_icon_type.png"])
            keys["name"] = item.text()
            keys["icon"] = icon

            html = """
                <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title></title>
                    </head>

                    <body>
                        <h3> {{name}} </h3>
                        <img src='file://{{icon}}' />
                    </body>

                </html>
            """

            self.window.btn_ext.show()
            self.window.btn_ext.setIcon(QIcon(icon))

            self.set_html(self.get_jinja_template(html, keys))
        except TypeError:
            pass
        
    def open_file(self, item, results):
        self.window.hide()
        QDesktopServices.openUrl(QUrl.fromUserInput(results.get(item.text())))

    def run_plugin(self, func):
        html = func.get("html")

        if func.get("open_links_in_browser", True):
            self.UIB_web.page().setLinkDelegationPolicy(self.web_page.DelegateAllLinks)
            self.UIB_web.page().linkClicked.connect(self.__link_clicked)

        self.web_frame = self.UIB_web.page().mainFrame()
        self.web_frame.addToJavaScriptWindowObject(func.get("call_name", "").strip(),
                                                    func.get("object", DefaultApp()))

        if func.get("jinja") and not func.get("template_dir"):
            html = self.get_jinja_template(open(html, "r").read() if os.path.exists(html) 
                                            else html, func.get("keywords", {}))

        elif func.get("template_dir"):
            html = self.get_jinja_template_env(func.get("template_dir", "templates"),
                                               func.get("base_file", "index.html"), 
                                               func.get("keywords", {}))
        self.set_html(html)

    # def check_progress_bar(self, value):
    #     if self.UIB_progress_bar.isHidden(): 
    #         self.UIB_progress_bar.show()
    #     self._progress_bar(value)

    # def _progress_bar(self, value: int):
    #     if value == 100:
    #         self.UIB_progress_bar.setValue(0)
    #         self.UIB_progress_bar.hide()
    #     else:
    #         Thread(target=self.UIB_progress_bar.setValue,
    #                args=[value], daemon=True).start()

    def __link_clicked(self, url):
        """Open external links in browser and internal links in the webview"""
        self.UIB_web.setFocus()

        ready_url = url.toEncoded().data().decode()

        if self.root_url not in ready_url:
            QDesktopServices.openUrl(url)
        else:
            self.UIB_web.load(QUrl(ready_url))

        self.UIB_web.setFocus()

    ############ Check HTML return code type
    def set_html(self, html: str):
        try:
            if html.startswith(("http", "ftp", "tcp", "file")):
                self.UIB_web.load(QUrl(html))

            elif os.path.exists(html):
                # self.UIB_web.setUrl(QUrl().fromUserInput(html))
                self.UIB_web.load(QUrl.fromUserInput(html))
                # self.UIB_web.setHtml(str(open(QUrl().fromUserInput(html).toLocalFile(), "r").read()), 
                #                       QUrl.fromUserInput(html))

            else:
                # with open(self.ext.get('path') + ".tmp.html", "w") as _fw:
                #     _fw.write(str(func.get("html")))
                #     _fw.close()
                # self.UIB_web.setUrl(QUrl().fromUserInput(self.ext.get('path') + ".tmp.html"))
                self.UIB_web.setHtml(html)
        except Exception:
            pass

    def get_jinja_template_env(self, tmp_dir: str="templates", base: str="index.html", kwargs: dict={}):
        file_loader = FileSystemLoader(tmp_dir)
        env = Environment(loader=file_loader)

        template = env.get_template(base)
        output = template.render(kwargs)

        return output

    def get_jinja_template(self, html: str, kwargs: dict={}):
        tm = Template(html)
        return tm.render(kwargs)

class DefaultApp(QObject):
    def __init__(self) -> None:
        super().__init__()
