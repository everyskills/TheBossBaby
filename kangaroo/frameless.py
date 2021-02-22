#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QEnterEvent
from PyQt5.QtWidgets import QWidget, QDialog


LEFT = 1
TOP = 2
RIGHT = 4
BOTTOM = 8
LEFTTOP = LEFT | TOP
RIGHTTOP = RIGHT | TOP
LEFTBOTTOM = LEFT | BOTTOM
RIGHTBOTTOM = RIGHT | BOTTOM

class KFramelessBase:

    Margins = 4
    BaseClass = QWidget

    def __init__(self, *args, **kwargs):
        super(KFramelessBase, self).__init__(*args, **kwargs)
        self.dragParams = {'type': 0, 'x': 0,
                           'y': 0, 'margin': 0, 'draging': False}
        self.originalCusor = None
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def isResizable(self):
        return self.minimumSize() != self.maximumSize()

    def getEdge(self, pos):
        rect = self.rect()
        edge = 0
        if not self.isResizable():
            return edge
        if pos.x() <= rect.left() + self.Margins:
            edge |= LEFT
        elif pos.x() >= rect.right() - self.Margins:
            edge |= RIGHT
        if pos.y() <= rect.top() + self.Margins:
            edge |= TOP
        elif pos.y() >= rect.bottom() - self.Margins:
            edge |= BOTTOM
        return edge

    def adjustCursor(self, edge):
        cursor = None
        if edge in (TOP, BOTTOM):
            cursor = Qt.SizeVerCursor
        elif edge in (LEFT, RIGHT):
            cursor = Qt.SizeHorCursor
        elif edge in (LEFT | TOP, RIGHT | BOTTOM):
            cursor = Qt.SizeFDiagCursor
        elif edge in (TOP | RIGHT, BOTTOM | LEFT):
            cursor = Qt.SizeBDiagCursor
        if cursor and cursor != self.cursor():
            self.setCursor(cursor)

    def eventFilter(self, obj, event):
        if isinstance(event, QEnterEvent):
            self.setCursor(self.originalCusor or Qt.ArrowCursor)
        return self.BaseClass.eventFilter(self, obj, event)

    def paintEvent(self, event):
        self.BaseClass.paintEvent(self, event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def showEvent(self, event):
        layout = self.layout()
        if self.originalCusor == None and layout:
            self.originalCusor = self.cursor()
            layout.setContentsMargins(
                self.Margins, self.Margins, self.Margins, self.Margins)

            for w in self.children():
                if isinstance(w, QWidget):
                    w.installEventFilter(self)
        self.BaseClass.showEvent(self, event)

    def mousePressEvent(self, event):
        if not self.isResizable() or self.childAt(event.pos()):
            return
        self.dragParams['x'] = event.x()
        self.dragParams['y'] = event.y()
        self.dragParams['globalX'] = event.globalX()
        self.dragParams['globalY'] = event.globalY()
        self.dragParams['width'] = self.width()
        self.dragParams['height'] = self.height()
        if event.button() == Qt.LeftButton and self.dragParams['type'] != 0 \
                and not self.isMaximized() and not self.isFullScreen():
            self.dragParams['draging'] = True

    def mouseReleaseEvent(self, event):
        self.dragParams['draging'] = False
        self.dragParams['type'] = 0

    def mouseMoveEvent(self, event):
        if self.isMaximized() or self.isFullScreen() or not self.isResizable():
            return

        cursorType = self.dragParams['type']
        if not self.dragParams['draging']:
            cursorType = self.dragParams['type'] = self.getEdge(event.pos())
            self.adjustCursor(cursorType)

        if self.dragParams['draging']:
            x = self.x()
            y = self.y()
            width = self.width()
            height = self.height()

            if cursorType & TOP == TOP:
                y = event.globalY() - self.dragParams['margin']
                height = self.dragParams['height'] + \
                    self.dragParams['globalY'] - event.globalY()
            if cursorType & BOTTOM == BOTTOM:
                height = self.dragParams['height'] - \
                    self.dragParams['globalY'] + event.globalY()
            if cursorType & LEFT == LEFT:
                x = event.globalX() - self.dragParams['margin']
                width = self.dragParams['width'] + \
                    self.dragParams['globalX'] - event.globalX()
            if cursorType & RIGHT == RIGHT:
                width = self.dragParams['width'] - \
                    self.dragParams['globalX'] + event.globalX()

            minw = self.minimumWidth()
            maxw = self.maximumWidth()
            minh = self.minimumHeight()
            maxh = self.maximumHeight()
            if width < minw or width > maxw or height < minh or height > maxh:
                return

            self.setGeometry(x, y, width, height)


class KFramelessWidget(QWidget, KFramelessBase):
    BaseClass = QWidget

class KFramelessDialog(QDialog, KFramelessBase):
    BaseClass = QDialog
