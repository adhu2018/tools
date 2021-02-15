# -*- coding: utf-8 -*-
from tools import *

print("部分功能测试（false表示存在异常）\n\r")

temp = getClipboardData()
setClipboardData("test")
print("getClipboardData/setClipboardData: ", getClipboardData()=="test")
setClipboardData(temp)

linkList = linkConverter("test")
print("flashgetLinkGenerator: ",
    linkList["flashget"]=="flashget://W0ZMQVNIR0VUXXRlc3RbRkxBU0hHRVRd")
print("flashgetLinkRestore: ",
    flashgetLinkRestore("flashget://W0ZMQVNIR0VUXXRlc3RbRkxBU0hHRVRd")=="test")
print("qqdlLinkGenerator: ", linkList["qqdl"]=="qqdl://dGVzdA==")
print("qqdlLinkRestore: ", qqdlLinkRestore("qqdl://dGVzdA==")=="test")
print("thunderLinkGenerator: ", linkList["thunder"]=="thunder://QUF0ZXN0Wlo=")
print("thunderLinkRestore: ", thunderLinkRestore("thunder://QUF0ZXN0Wlo=")=="test")
