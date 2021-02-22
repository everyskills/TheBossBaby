#!/usr/bin/python3

from PyQt5.QtWebKit import QWebSettings

def get_settings():
    settings = QWebSettings.globalSettings()
    settings.setDefaultTextEncoding("utf-8")
    settings.setAttribute(QWebSettings.JavascriptEnabled, True)
    settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
    settings.setAttribute(QWebSettings.WebAudioEnabled, True)
    settings.setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled, True)
    settings.setAttribute(QWebSettings.PluginsEnabled, True)
    settings.setAttribute(QWebSettings.CSSGridLayoutEnabled, True)
    settings.setAttribute(QWebSettings.CSSRegionsEnabled, True)
    settings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)
    settings.setAttribute(QWebSettings.JavaEnabled, True)
    settings.setAttribute(QWebSettings.PrivateBrowsingEnabled, True)
    settings.setAttribute(QWebSettings.PrintElementBackgrounds, True)
    settings.setAttribute(QWebSettings.NotificationsEnabled, True)
    settings.setAttribute(QWebSettings.JavascriptCanCloseWindows, True)
    settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
    settings.setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
    settings.setAttribute(QWebSettings.LocalStorageDatabaseEnabled, True)
    settings.setAttribute(QWebSettings.LocalStorageEnabled, True)
    settings.setAttribute(QWebSettings.WebGLEnabled, True)
    settings.setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled, True)
    settings.setAttribute(QWebSettings.FrameFlatteningEnabled, True)
    settings.setAttribute(QWebSettings.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebSettings.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebSettings.PrivateBrowsingEnabled, True)
    settings.setAttribute(QWebSettings.NotificationsEnabled, True)
    settings.setAttribute(QWebSettings.HyperlinkAuditingEnabled, True)

    return settings