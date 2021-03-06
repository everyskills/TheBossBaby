#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os

from glob import glob
from PyQt5.QtGui import QDesktopServices, QIcon, QMovie
from PyQt5.QtCore import QFileInfo, QUrl, QSize
from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.uic import loadUi
from UIBox import pkg, item

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "")

class Results(QWidget):
    def __init__(self, parent):
        super(Results, self).__init__()
        QWidget.__init__(self)

        self.parent = parent

        self.ui = loadUi(base_dir + "files.ui", self)
        self.ui.list_widget.itemDoubleClicked.connect(self.add_click_path)
        self.ui.list_widget.itemSelectionChanged.connect(self.get_path_info)
        # self.ui.btn_video.clicked.connect(self.start_video)
        # self.ui.slide_video.sliderMoved.connect(self.set_video_pos)

        enterAction = QAction("enter", self, shortcut="Return", triggered=self.get_enter_item)
        self.ui.list_widget.addAction(enterAction)

        self.ui.label_12.hide()
        self.ui.lpermissions.hide()

        self.init_ui()
        
    def init_ui(self):
        self.short_title(os.path.split(str(self.parent.get_text()).strip())[1])
        self.query_file()
        self.start_up()
        
    def get_enter_item(self):
        self.add_click_path(self.ui.list_widget.currentItem())
        self.ui.list_widget.setFocus()

    def start_up(self):
        self.ui.slide_video.hide()
        self.ui.label_slide_value.hide()
        self.ui.btn_video.hide()

    def query_file(self):
        self.ui.list_widget.clear()
        self.query = self.parent.get_text()

        _icon = pkg.icon_types(self.query)
        self.ui.image.setPixmap(pkg.set_image(_icon, icon=True, size=300))

        _file_count, _folder_count, _size = 0, 0, 0.00
        _path = os.path.expandvars(os.path.expanduser(self.query))

        if len(self.query) == 1 and self.query.startswith("~"):
            self.parent.insert_text("/")

        try:
            all_path = glob(_path + "*")
            for i in all_path:
                if not os.path.isfile(i):
                    _icon = pkg.icon_types(i)
                    _folder_count += 1
                    _size += os.path.getsize(i)

                elif not os.path.isdir(i):
                    _icon = pkg.icon_types(i)
                    _file_count += 1
                    _size += os.path.getsize(i)

                else:
                    _icon = pkg.icon_types(i)
                    _file_count += 1
                    _size += os.path.getsize(i)
                
                list_item = pkg.add_item(self.ui.list_widget, _icon)
                item_widget = pkg.add_item_widget(
                    list_item, item.UIBUi_Item(), str(os.path.split(i)[1]), i)
                pkg.set_item_widget(self.ui.list_widget, item_widget)
                self.ui.status.setText(f"{_folder_count} {'Folder' if _folder_count <= 1 else 'Folders'}, {_file_count} {'File' if _file_count <= 1 else 'Files'} ({pkg.get_size(_size)})")
                item_widget[1].mouseDoubleClickEvent = (lambda e: self.add_click_path(self.list_widget.currentItem()))
        except Exception:
            pass

    def hide_video(self):
        # try:
        #     if self.video_player.media.is_playing():
        #         self.video_player.media.stop()
        # except AttributeError:
        #     pass
        
        self.ui.btn_video.hide()
        self.ui.slide_video.hide()
        self.ui.label_slide_value.clear()
        self.ui.slide_video.hide()

    def show_video(self):
        self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
        self.ui.slide_video.setValue(0)
        self.ui.btn_video.show()
        self.ui.slide_video.show()
        self.ui.label_slide_value.show()

    def get_path_info(self):
        item = self.ui.list_widget.currentItem()
        litem = item.listWidget().itemWidget(item)

        _file = litem.title.text()
        _path = litem.subtitle.text()

        # self.hide_video()
        self.short_title(_file)
        self.set_data(_path)

        try:
            img = tuple(pkg.api_icons("Image"))
            # video = tuple(pkg.api_icons("Video"))
            # audio = tuple(pkg.api_icons("Audio"))
        except TypeError:
            pass

        if _file.endswith(".gif"):
            self.hide_video()
            movie = QMovie(_path)
            movie.setScaledSize(QSize(350, 300))
            self.ui.image.setMovie(movie)
            movie.start()

        elif _file.endswith(img):
            # self.hide_video()
            self.ui.image.setPixmap(pkg.set_image(item.icon(), size=350))

        # elif _file.endswith(video) or _file.endswith(audio):
        #     self.video_player = pkg.video_player(
        #         self.ui.image, "", self.media_time_changed)
            
        #     self.ui.image.setPixmap(pkg.set_image(item.icon(), size=300))
        #     self.video_player.set_media(_path)
        #     self.show_video()

            # video_screen_img_path = base_dir + "icons/"
            # self.video_player.media.video_take_snapshot(0, 
            #     str(video_screen_img_path + _file),
            #     i_width=self.video_player.media.video_get_width() + 10, 
            #     i_height=self.video_player.media.video_get_height() + 10)

        else:
            self.hide_video()
            self.ui.image.setPixmap(pkg.set_image(item.icon(), size=300))
            
    def set_data(self, _file):
        if not _file.endswith(".fdmdownload"):
            ff = QFileInfo(_file)
            self.short_title(ff.fileName())
            self.ui.lsize.setText(pkg.get_size(ff.size()))

            if ff.isFile():
                try:
                    self.ui.image.setText(str(open(_file, "r").read()))
                except Exception:
                    pass

            if ff.isDir():
                self.ui.litems.show()
                self.ui.label_3.show()
                self.ui.litems.setText(str(len(glob(_file + "/*"))))
            else:
                self.ui.label_3.hide()
                self.ui.litems.hide()

            self.ui.lcreated.setText(ff.created().toString())
            self.ui.lmodified.setText(ff.lastModified().toString())
            self.ui.laccessed.setText(ff.lastRead().toString())
            self.ui.luser.setText(ff.owner())
            self.ui.luid.setText(str(ff.ownerId()))
            self.ui.lgroup.setText(str(ff.group()))
            self.ui.lgid.setText(str(ff.groupId()))
            self.ui.lpath.setText(ff.path())
            # self.lpermissions.setText(str(ff.permissions())

    def add_click_path(self, item):
        item = item.listWidget().itemWidget(item)
        _path = item.subtitle.text()

        self.set_data(_path)

        if not os.path.isfile(_path):
            wh = "" if not os.path.isdir(os.path.expanduser(_path)) else "/"
            self.parent.set_text(_path + wh)
        else:
            QDesktopServices().openUrl(QUrl().fromUserInput(_path))  # from PyQt5
            self.parent.hide_win()

    def short_title(self, item: str):
        if len(item) <= 20:
            self.ui.title.setText(item)
        else:
            self.ui.title.setText(item[0:21] + "...")

    # def start_video(self):
    #     if self.video_player.media.is_playing():
    #         self.video_player.media.pause()
    #         self.ui.btn_video.setIcon(QIcon(base_dir + "icons/play.png"))
    #     else:
    #         self.video_player.media.play()
    #         self.ui.btn_video.setIcon(QIcon(base_dir + "icons/pause.png"))

    # def set_video_pos(self):
    #     pos = self.ui.slide_video.value()
    #     self.video_player.media.set_position(pos / 100)

    # def media_time_changed(self, event):
    #     pos = self.video_player.media.get_position() * 100
    #     self.ui.slide_video.setValue(int(pos))        
    #     self.ui.label_slide_value.setText(str(int(pos)) + "%")

    #     if int(pos) >= 100 or int(pos) >= 99:
    #     	self.ui.slide_video.clear()
    #     	self.video_player.media.set_position(0.00)
    #     	self.ui.slide_video.setValue(0)
    #     	self.video_player.media.pause()
