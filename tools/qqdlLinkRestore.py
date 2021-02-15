# -*- coding: utf-8 -*-
import base64
import chardet

def qqdlLinkRestore(link_: str):
    link = link_[7:]
    if len(link) == 0 or not link_.startswith("qqdl://"):
        print("`{}`不是QQ旋风链接！".format(link_))
        return None
    bytes_ = base64.b64decode(link)
    try:
        str_ = bytes_.decode(chardet.detect(bytes_)['encoding'])
    except TypeError:
        try:
            str_ = bytes_.decode("utf8")
        except UnicodeDecodeError:
            str_ = bytes_.decode("gbk")
    return str_


if __name__ == "__main__":
    pass
