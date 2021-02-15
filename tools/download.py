# -*- coding: utf-8 -*-
import os
import re
try:
    from requests_html import HTMLSession
    session = HTMLSession()
except ModuleNotFoundError:
    import requests as session
try:
    from .md5 import md5
except ImportError:
    from md5 import md5

# download("http://www.baidu.com"[, path])
def download(*_str):
    if len(_str) > 0:
        url = _str[0]
        type = re.sub(r".*//[^/]*", r"", url)
        type = re.sub(r"[@\?].*", r"", type)
        type = re.sub(r".*/", r"", type)
        try:
            type = re.match(r".*?(\.[^\.]*)$",type)[1]
        except:
            type = ""
    else:
        return False
    if len(_str) > 1:
        fpath = _str[1] + md5(url) + type
    else:
        fpath = md5(url) + type
    if len(_str) > 2:
        new = _str[2]
    else:
        new = False
    if new or not os.path.exists(fpath):
        r = session.get(url)
        if r.status_code == 200:
            with open(fpath, "wb+") as f:
                f.write(r.content)
        del r
    return os.path.abspath(fpath)


if __name__ == "__main__":
    pass
