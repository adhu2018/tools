# -*- coding: utf-8 -*-
import importlib

__temp = ["allow", "chapterNum", "download", "filter", "flashgetLinkGenerator",
        "flashgetLinkRestore", "getClipboardData", "linkConverter", "md5", "meiriyiwen",
        "qqdlLinkGenerator", "qqdlLinkRestore", "reload", "sendmail", "text2Speech",
        "thunderLinkRestore"]
for i in __temp:
    importlib.import_module(".{}".format(i), "tools")
    exec("from .{m} import {m}".format(m=i))
del i, __temp, importlib

def cls():
    exec("__import__('os').system('cls')")
