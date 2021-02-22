#!/usr/bin/python3

import os
import sys

from kangaroo import pkg, web
from threading import Thread
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QObject, QSize, QUrl
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWidgets import QAction, QFrame, QGridLayout, QListWidget, QProgressBar, QSizePolicy, QWidget

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

sys.path.insert(0, base_dir + '/modules/jinja2.zip')
from jinja2 import Environment, FileSystemLoader, Template

class KUi_web(object):
    def setupUi(self, Form):
        # Form.resize(755, 642)
        # self.gridLayout = QGridLayout(Form)
        # self.gridLayout.setObjectName(u"gridLayout")
        # self.gridLayout.setVerticalSpacing(0)
        # self.gridLayout.setContentsMargins(0, 0, 0, 0)
        # self.frame = QFrame(Form)
        # self.frame.setObjectName(u"frame")
        # self.frame.setFrameShape(QFrame.NoFrame)
        # self.frame.setFrameShadow(QFrame.Plain)
        # self.gridLayout_3 = QGridLayout(self.frame)
        # self.gridLayout_3.setObjectName(u"gridLayout_3")
        # self.gridLayout_3.setVerticalSpacing(0)
        # self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        
        # self.KNG_list_widget = QListWidget(self.frame)
        # self.KNG_list_widget.setGridSize(QSize(38, 38))
        # self.KNG_list_widget.setIconSize(QSize(22, 22))
        # self.KNG_list_widget.setObjectName(u"KNG_list_widget")
        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.KNG_list_widget.sizePolicy().hasHeightForWidth())
        # self.KNG_list_widget.setSizePolicy(sizePolicy)
        # self.KNG_list_widget.setFrameShape(QFrame.NoFrame)
        # self.KNG_list_widget.setFrameShadow(QFrame.Plain)

        # self.gridLayout_3.addWidget(self.KNG_list_widget, 0, 0, 1, 1)

        # self.KNG_web_frame = QFrame(self.frame)
        # self.KNG_web_frame.setObjectName(u"KNG_web_frame")
        # sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # sizePolicy1.setHorizontalStretch(0)
        # sizePolicy1.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(
        #     self.KNG_web_frame.sizePolicy().hasHeightForWidth())
        # self.KNG_web_frame.setSizePolicy(sizePolicy1)
        # # self.KNG_web_frame.setFrameShape(QFrame.Panel)

        # self.KNG_web_frame.setFrameShape(QFrame.NoFrame)
        # self.KNG_web_frame.setFrameShadow(QFrame.Plain)
        # self.gridLayout_2 = QGridLayout(self.KNG_web_frame)
        # self.gridLayout_2.setSpacing(0)
        # self.gridLayout_2.setObjectName(u"gridLayout_2")
        # self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        # self.web_view = QWebView(self.KNG_web_frame)
        # self.web_view.setObjectName(u"web_view")
        # sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # sizePolicy2.setHorizontalStretch(0)
        # sizePolicy2.setVerticalStretch(0)
        # sizePolicy2.setHeightForWidth(
        #     self.web_view.sizePolicy().hasHeightForWidth())
        # self.web_view.setSizePolicy(sizePolicy2)
        # self.web_view.setUrl(QUrl(u"about:blank"))

        # self.gridLayout_2.addWidget(self.web_view, 0, 0, 1, 1)

        # self.web_progress_bar = QProgressBar(self.KNG_web_frame)
        # self.web_progress_bar.setObjectName(u"web_progress_bar")
        # self.web_progress_bar.setValue(0)

        # self.gridLayout_2.addWidget(self.web_progress_bar, 1, 0, 1, 1)

        # self.gridLayout_3.addWidget(self.KNG_web_frame, 0, 1, 1, 1)

        # self.gridLayout.addWidget(self.frame, 0, 1, 1, 1)
        





























        Form.resize(729, 535)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 6, 0)
        self.KNG_list_widget = QListWidget(self.frame_2)
        self.KNG_list_widget.setObjectName(u"KNG_list_widget")
        self.KNG_list_widget.setFrameShape(QFrame.NoFrame)
        self.KNG_list_widget.setFrameShadow(QFrame.Plain)
        self.KNG_list_widget.setIconSize(QSize(22, 22))
        self.KNG_list_widget.setGridSize(QSize(38, 38))
        self.KNG_list_widget.setWordWrap(False)
        self.KNG_list_widget.setSortingEnabled(True)

        self.gridLayout_4.addWidget(self.KNG_list_widget, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)

        self.KNG_web_frame = QFrame(Form)
        self.KNG_web_frame.setObjectName(u"KNG_web_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.KNG_web_frame.sizePolicy().hasHeightForWidth())
        self.KNG_web_frame.setSizePolicy(sizePolicy1)
        self.KNG_web_frame.setMaximumSize(QSize(420, 16777215))
        self.KNG_web_frame.setFrameShape(QFrame.NoFrame)
        self.KNG_web_frame.setFrameShadow(QFrame.Plain)
        self.gridLayout_3 = QGridLayout(self.KNG_web_frame)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.web_view = QWebView(self.KNG_web_frame)
        self.web_view.setObjectName(u"web_view")
        self.web_view.setUrl(QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.web_view, 0, 0, 1, 1)

        self.web_progress_bar = QProgressBar(self.KNG_web_frame)
        self.web_progress_bar.setObjectName(u"web_progress_bar")
        self.web_progress_bar.setMaximumSize(QSize(16777215, 15))
        self.web_progress_bar.setValue(24)

        self.gridLayout_3.addWidget(self.web_progress_bar, 1, 0, 1, 1)

        self.gridLayout.addWidget(self.KNG_web_frame, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.KNG_list_widget, self.web_view)
        self.web_progress_bar.hide()
        
class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, message, line, source):
        if source:
            print('JS-Error: Line(%s), Source(%s): %s' % (line, source, message))
        else:
            print(message)

class KWPlugin(QWidget, KUi_web):
    __type__ = "web"

    def __init__(self, window=None) -> None:
        # super().__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)     

        self.window = window
        
        self.enterAction = QAction(
            "enter", 
            self.KNG_list_widget,
            shortcut="Ctrl+Return", 
            triggered=lambda: self.open_file(self.KNG_list_widget.currentItem(), 
                            pkg.find_in(self.window.input.text().strip(), pkg.user_home_dirs)))

        self.KNG_list_widget.addAction(self.enterAction)

        self.KNG_list_widget.itemDoubleClicked.connect(
            lambda item: self.open_file(item, 
            pkg.find_in(self.window.input.text().strip(), 
            pkg.user_home_dirs)))

        self.init_ui()

    def init_ui(self, func=None):
        web.get_settings()

        self.web_page = WebPage(self)
        self.web_view.setPage(self.web_page)        
        self.web_view.loadProgress.connect(self.check_progress_bar)

        if not func == None:
            self.run_plugin(func)

    def set_list_items(self):
        results = pkg.find_in(self.window.input.text().strip(), pkg.user_home_dirs)
        for k, v in results.items():
            icon = pkg.icon_types(v)
            item = pkg.add_item(self.KNG_list_widget, icon, k, v, font_size=9)
            self.KNG_list_widget.addItem(item)

    def open_file(self, item, results):
        self.window.hide()
        QDesktopServices.openUrl(QUrl.fromUserInput(results.get(item.text())))

    def run_plugin(self, func):
        html = func.get("html")

        if func.get("open_url_in_browser", True):
            self.web_view.page().setLinkDelegationPolicy(self.web_page.DelegateAllLinks)
            self.web_view.page().linkClicked.connect(self.__link_clicked)

        self.web_frame = self.web_view.page().mainFrame()
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

    def check_progress_bar(self, value):
        if self.web_progress_bar.isHidden(): 
            self.web_progress_bar.show()
        self._progress_bar(value)

    def _progress_bar(self, value: int):
        if value == 100:
            self.web_progress_bar.setValue(0)
            self.web_progress_bar.hide()
        else:
            Thread(target=self.web_progress_bar.setValue,
                   args=[value], daemon=True).start()

    def __link_clicked(self, url):
        """Open external links in browser and internal links in the webview"""
        self.web_view.setFocus()

        ready_url = url.toEncoded().data().decode()

        if self.root_url not in ready_url:
            QDesktopServices.openUrl(url)
        else:
            self.web_view.load(QUrl(ready_url))

        self.web_view.setFocus()

    # def get_item_dbclicked(self, item):
    #     try:
    #         data = self.Dict.get(id(item))
    #         data.get("cfunc")(data.get("icon"), data.get("title"))
    #     except Exception as item_err:
    #         # print("Error-ItemDoubleClicked: " + str(item_err))
    #         pass
        
    #     self.KNG_list_widget.setCurrentRow(-1)

    # def get_item_selected(self, item=None):
    #     item = self.KNG_list_widget.currentItem()
    #     try:
    #         data = self.Dict.get(id(item))
    #         data.get("sfunc")(data.get("icon"), data.get("title"))
    #     except Exception as item_err:
    #         # print("Error-ItemSelected: " + str(item_err))
    #         pass

    ############ Check HTML return code type
    def set_html(self, html: str):
        if html.startswith(("http", "ftp", "tcp")):
            self.web_view.load(QUrl(html))

        elif os.path.exists(html):
            # self.web_view.setUrl(QUrl().fromUserInput(html))
            self.web_view.load(QUrl.fromUserInput(html))
            # self.web_view.setHtml(str(open(QUrl().fromUserInput(html).toLocalFile(), "r").read()), 
            #                       QUrl.fromUserInput(html))

        else:
            # with open(self.ext.get('path') + ".tmp.html", "w") as _fw:
            #     _fw.write(str(func.get("html")))
            #     _fw.close()
            # self.web_view.setUrl(QUrl().fromUserInput(self.ext.get('path') + ".tmp.html"))
            self.web_view.setHtml(html)


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
