#!/usr/bin/python3

def get_webkit_settings():
    from PyQt5.QtWebKit import QWebSettings

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
    settings.setAttribute(QWebSettings.FrameFlatteningEnabled, True)
    settings.setAttribute(QWebSettings.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebSettings.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebSettings.HyperlinkAuditingEnabled, True)

    return settings

def get_webengine_settings():
    from PyQt5.QtWebEngineWidgets import QWebEngineSettings

    settings = QWebEngineSettings.globalSettings()
    settings.setDefaultTextEncoding("utf-8")
    settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
    settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebEngineSettings.AllowWindowActivationFromJavaScript, True)
    settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
    settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
    settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
    settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, True)
    settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
    settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
    settings.setAttribute(QWebEngineSettings.JavascriptCanPaste, True)
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
    settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
    settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.PrintElementBackgrounds, True)
    settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
    settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebEngineSettings.SpatialNavigationEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)
    settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
    settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)

    return settings