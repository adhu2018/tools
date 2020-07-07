# -*- coding: utf-8 -*-
import hashlib
import os
import re
try:
    from requests_html import HTMLSession
    session = HTMLSession()
except ModuleNotFoundError:
    import requests as session


# allow([type, ]_url)
def allow(*_str):
    _url = ""
    type = "*"
    regcom = re.compile(r"https?(://[^/]*)", re.I)
    while _url == "":
        for i in _str:
            if regcom.search(i):
                _url = i
            else:
                type = i.upper()
    _list = _robots(_url)
    b = True  # 默认允许爬取
    if _list:
        for i in _list:
            # 爬虫名称或种类
            if i[0] == type or i[0] == "*":
                i = i[1]
                for j in i:  # j ['Disallow', '.*?/s\\?.*']
                    reg = re.compile(j[1], re.I)
                    if reg.match(_url):  # fix 以第一个匹配到的为准。之前的写法是错的。
                        if j[0].upper() == "DISALLOW":
                            return False
                        else:
                            return True
    return b

# 拼接链接，尝试http和https
def _robots(_url):
    session = HTMLSession()
    url_com = re.search(r"https?(://[^/]*)", _url)[1]
    url1 = "http%s/robots.txt" % str(url_com)
    url2 = "https%s/robots.txt" % str(url_com)
    list1 = robots_(url1)
    if list1:
        return list1
    else:
        list2 = robots_(url2)
        if list2:
            return list2
        else:
            return False

# _
def robots_(url1):
    """
    任何一条Disallow记录为空，说明该网站的所有部分都允许被访问，在"/robots.txt"文件中，至少要有一条Disallow记录。
    如果"/robots.txt"是一个空文件，则对于所有的搜索引擎robot，该网站都是开放的。
    一个网站的所有URL默认是Allow的，所以Allow通常与Disallow搭配使用，实现允许访问一部分网页同时禁止访问其它所有URL的功能。
    需要特别注意的是Disallow与Allow行的顺序是有意义的，robot会根据第一个匹配成功的Allow或Disallow行确定是否访问某个URL。
    robots支持使用通配符"*"和"$"来模糊匹配url：  # 其他的不符合正则语法，需要转义
        "$" 匹配行结束符。
        "*" 匹配0或多个任意字符
    """
    try:
        r = session.get(url1)
    except:  # 尽量验证签名，（使用fiddler等）证书验证有问题时不验证签名。会有一个Warning，这样你就知道当前是没有验证签名的。也可以直接不验证签名，然后把Warning去掉，但不推荐。
        r = session.get(url1, verify=False)
    if r.status_code == 200:
        _list1 = re.split(r"\n", r.text)
        list1 = []
        reg = re.compile(r"^User-agent:\s*(.*)", re.I)
        # reg1 = re.compile(r"^(Disallow):\s*(.*)", re.I)
        # reg2 = re.compile(r"^(Allow):\s*(.*)", re.I)
        reg12 = re.compile(r"^((Dis)?allow):\s*(.*)", re.I)
        reg3 = re.compile(r"^Crawl-delay:\s*(.*)", re.I)
        regz = re.compile(r"([\{\}\[\]\\\^\.\?\+])")  # {}[]\^.?+ 记起了再补充
        reg_ = re.compile(r"(\*)")
        reg__ = re.compile(r"(\$$)")
        for i in _list1:
            if i == "":  # 空行
                pass
            elif reg.search(i):
                list1.append([])  # 爬虫
                list1[-1].append(reg.search(i)[1].upper())  # 爬虫名称，大写 [][0]
                list1[-1].append([])  # (Disallow or Allow):value [][1] 需要特别注意的是Disallow与Allow行的顺序是有意义的
                list1[-1].append([])  # Crawl-delay [][2] 时间间隔
            elif reg12.search(i):
                # [][1][0] ['Disallow', '/baidu']
                # [][1][0][0] 'Disallow'
                if reg__.search(i):  # $标识
                    list1[-1][1].append([reg12.search(i)[1], ".*?"+reg_.sub(r".*", regz.sub(r"\\\1", reg12.search(i)[3]))])
                else:
                    list1[-1][1].append([reg12.search(i)[1], ".*?"+reg_.sub(r".*", regz.sub(r"\\\1", reg12.search(i)[3]))+".*"])
            elif reg3.search(i):
                list1[-1][2].append(reg3.search(i)[1])
        return list1
    else:
        return False

def chapterNum(aForHtml):
    num = 0
    temp = str(aForHtml)
    tempNum = re.search(r"第([^0-9章节回(部分)]+)([章节回(部分)])", temp)
    if tempNum:
        b = tempNum[2]
        tempNum = tempNum[1]
        tempNum = re.sub(r"[一壹Ⅰ]",r"1", tempNum)
        tempNum = re.sub(r"[二贰Ⅱ]",r"2", tempNum)
        tempNum = re.sub(r"[三叁Ⅲ]",r"3", tempNum)
        tempNum = re.sub(r"[四肆Ⅳ]",r"4", tempNum)
        tempNum = re.sub(r"[五伍Ⅴ]",r"5", tempNum)
        tempNum = re.sub(r"[六陆Ⅵ]",r"6", tempNum)
        tempNum = re.sub(r"[七柒Ⅶ]",r"7", tempNum)
        tempNum = re.sub(r"[八捌Ⅷ]",r"8", tempNum)
        tempNum = re.sub(r"[九玖Ⅸ]",r"9", tempNum)
        tempNum = re.sub(r"[零〇]",r"0", tempNum)
        if re.search(r"^\d+$", tempNum):
            aForHtml = re.sub(r"第[^0-9章节回(部分)]+([章节回(部分)])", "第"+tempNum+b, aForHtml)
        else:
            numList = re.findall(r"[1-9][^\d]|[^\d]|\d", tempNum)
            for i in numList:
                if re.search(r"亿", i):
                    if re.search(r"\d", i):
                        num = (num + int(re.search(r"\d", i)[0])) * 100000000
                    else:
                        num *= 100000000
                elif re.search(r"[万萬]", i):
                    if re.search(r"\d", i):
                        num = (num + int(re.search(r"\d", i)[0])) * 10000
                    else:
                        num *= 10000
                elif re.search(r"[千仟]", i):
                    num += int(re.search(r"\d", i)[0]) * 1000
                elif re.search(r"[百佰]", i):
                    num += int(re.search(r"\d", i)[0]) * 100
                elif re.search(r"[十什拾Ⅹ]", i):
                    if re.search(r"\d", i):
                        num += int(re.search(r"\d", i)[0]) * 10
                    else:
                        num += 10
                elif re.search(r"^\d$", i):
                    if re.search(r"0", tempNum):
                        num += int(re.search(r"\d", i)[0])
                    else:
                        temp = len(str(re.sub(r"[\s\S]*?(0+$)", r"\1", str(num)))) - 1
                        num += int(re.search(r"\d", i)[0]) * (10**temp)
            aForHtml = re.sub(r"第[^0-9章节回(部分)]+([章节回(部分)])", "第"+str(num)+b, aForHtml)
    return aForHtml

# download_("http://www.baidu.com"[, path])
def download_(*_str):
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
    r = session.get(url)
    if r.status_code == 200:
        if not os.path.exists(fpath):
            with open(fpath, "wb+") as f:
                f.write(r.content)
    del r
    return os.path.abspath(fpath)

def filter_(url):
    fpath = "blacklist.txt"  # 改成你的blacklist.txt的路径
    try:
        with open(fpath, "r", encoding="utf8") as f:
            blacklist = f.readlines()
    except FileNotFoundError: 
        with open(fpath, "w", encoding="utf8") as f:
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
            # if i.index(url):
            if i.find(url) > -1:
                return ""
    return url

# md5(str[, encoding]) or md5(bytes)
def md5(*_str):
    if len(_str) > 0:
        t = _str[0]
        encode_type = "utf-8"
        if len(_str) > 1:
            encode_type = _str[1]
        m = hashlib.md5()
        if type(t) == str:
            try:
                t = t.encode(encode_type)
            except LookupError:
                t = t.encode("utf-8")
        m.update(t)
        return m.hexdigest()
    else:
        print("缺少参数！")
        return False

if __name__ == "__main__":
    pass
