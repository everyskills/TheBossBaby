#!/usr/bin/python3

from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from pyqtkeybind import keybinder

class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

class TBB_Key_Bind(object):
    def __init__(self, parent=None) -> None:
        self.p = parent
        keybinder.init()

        win_event_filter = WinEventFilter(keybinder)
        event_dispatcher = QAbstractEventDispatcher.instance()
        event_dispatcher.installNativeEventFilter(win_event_filter)

    def register(self, hotkey: str, callback: object):
        keybinder.register_hotkey(self.p.winId(), hotkey, callback)

    def unregister(self, hotkey: str):
        keybinder.unregister_hotkey(self.p.winId(), hotkey)