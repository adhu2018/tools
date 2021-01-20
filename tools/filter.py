# -*- coding: utf-8 -*-
import re

def filter(url, path="blacklist.txt") -> str:
    """filter(url, path="blacklist.txt")  path默认值为blacklist.txt。url在文件(path)里匹配成功则返回值为空，否则原样返回url。"""
    try:
        with open(path, "r", encoding="utf8") as f:
            blacklist = f.readlines()
    except FileNotFoundError: 
        with open(path, "w", encoding="utf8") as f:
            pass
        blacklist = []
    for i in blacklist:
        i = i.strip()
        try:
            j = re.compile(i)
            if j.search(url):
                return ""
        except re.error:
            pass
        finally:
            if url.find(i) > -1:
                return ""
    return url


if __name__ == "__main__":
    pass
