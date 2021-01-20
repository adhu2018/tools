# -*- coding: utf-8 -*-
import base64
import chardet

# 迅雷链接还原
def thunderLinkRestore(thunder_link_: str):
    thunder_link = thunder_link_[10:]
    if len(thunder_link) == 0 or not thunder_link_.startswith("thunder_link"):
        print("`{}`不是迅雷链接！".format(thunder_link_))
        return None
    bytes_ = base64.b64decode(thunder_link)
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
