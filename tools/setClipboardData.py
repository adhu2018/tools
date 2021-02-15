# -*- coding: utf-8 -*-
try:
    import win32clipboard
    _win32clipboard = True
except ModuleNotFoundError:
    _win32clipboard = False

def setClipboardData(data: str=""):
    if not _win32clipboard:
        raise Exception("Please install the `win32clipboard` module.")
    try:
        win32clipboard.CloseClipboard()  # 解决进程异常结束时可能存在的问题
    except:
        pass
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()


if __name__ == "__main__":
    pass
