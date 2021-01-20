# -*- coding: utf-8 -*-
import base64
import chardet
import hashlib
import os
import re
try:
    from requests_html import HTMLSession
    session = HTMLSession()
except ModuleNotFoundError:
    import requests as session

############################################################
# allow

# allow([type, ]_url)
def allow(*_str) -> bool:
    # 需要的模块：re。
    # 不包含调用函数中使用的模块。
    # The required module: re.
    # Does not contain the modules used in the calling function.
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
                        return False if j[0].upper() == "DISALLOW" else True
    return b

# 拼接链接，尝试http和https
def _robots(_url):
    # 需要的模块：re。
    # 不包含调用函数中使用的模块。
    # The required module: re.
    # Does not contain the modules used in the calling function.
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
    # 需要的模块：re, requests_html/requests。
    # The required module: re, requests_html/requests.
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

# allow
############################################################

def chapterNum(aForHtml: str) -> str:
    # 需要的模块：re。
    # The required module: re.
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

# download("http://www.baidu.com"[, path])
def download(*_str):
    # 需要的模块：os, re, requests_html/requests。
    # The required module: os, re, requests_html/requests.
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

def filter(url, path="blacklist.txt") -> str:
    """filter(url, path="blacklist.txt")  path默认值为blacklist.txt。url在文件(path)里匹配成功则返回值为空，否则原样返回url。"""
    # 需要的模块：re。
    # The required module: re.
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

# md5(str[, encoding]) or md5(bytes) or md5(int)
def md5(*_str):
    # 需要的模块：hashlib。
    # The required module: hashlib.
    if len(_str) > 0:
        t = _str[0]
        if type(t) is not str:
            t = str(t)
        encode_type = "utf-8"
        if len(_str) > 1:
            encode_type = _str[1]
        m = hashlib.md5()
        try:
            t = t.encode(encode_type)
        except LookupError:
            t = t.encode("utf-8")
        m.update(t)
        return m.hexdigest()
    else:
        print("缺少参数！")
        return False

# 动态加载模块 相当于在{path}路径下使用`import {_module}`
def reload(_module, path=None, raise_=False):
    """
    试用阶段！！
    
    - 在系统环境路径列表`最前方`插入{path}
    - 使用`importlib.import_module(".", _module)`导入模块
    - 测试中，从`dir({_module})`的结果来看，相关的 类/函数 进行删减的时候是无法同步删减的，会保持原样
    - `在sys.path各路径下存在模块名称冲突`
      * 按照已知的常规导入模块方法，返回的结果是在sys.path中各个路径顺序找到的第一个(第一步的原因)
      * 测试可行，应该也是这样的，不过毕竟样本过少，不能保证稳定性。。
    - `importlib.reload(module_)`语句可以对模块进行热重载(即在代码运行的过程中进行重载，`即时生效`)
    
    - _module   需要导入的模块
    - path      模块所在的路径，可选
    - raise_    导入失败时是否报错，可选
    """
    # 需要的模块：sys, importlib。
    # The required module: sys, importlib.
    if path:
        import sys
        sys_path_temp = list(sys.path)
        sys.path.insert(0, path)
    try:
        import importlib
        module_ = importlib.import_module(".", _module)
        _module_ = importlib.reload(module_)
        return _module_
    except (ImportError, ModuleNotFoundError) as err:
        if path:
            sys.path = sys_path_temp
        if raise_:
            raise err
        return None

# 文本转语音，win10测试可行
def text2Speech(text):
    # 需要的模块：win32com。
    # The required module: win32com.
    try:
        import win32com.client
        # Microsoft Speech API
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
    except (ImportError, ModuleNotFoundError) as err:
        raise err

# 迅雷链接还原
def thunderLinkRestore(thunder_link_: str):
    # 需要的模块：base64, chardet。
    # The required module: base64, chardet.
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

# tools.meiriyiwen().print()
def meiriyiwen(fdir="./cache/", new=False):
    """fdir: 缓存文件夹。new: 重新请求，默认优先使用已有缓存。"""
    # 需要的模块：os, lxml。
    # 不包含调用函数中使用的模块。
    # The required module: os, lxml.
    # Does not contain the modules used in the calling function.
    class SimpleArticle:
        def __init__(self):
            self.title = ""
            self.author = ""
            self.content = ""
        
        def print(self, _print=True):
            result = "标题：{}\n\r作者：{}\n\r\n\r{}".format(self.title, self.author, self.content)
            if _print:
                print(result)
            return result
    
    article = SimpleArticle()
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    fpath = download("https://meiriyiwen.com/", fdir, new)
    with open(fpath, "r", encoding="utf8") as f:
        html_ = f.read()
        from lxml import etree
        html_ = etree.HTML(html_)
    article.title = html_.xpath("//h1")[0].text
    article.author = html_.xpath("//p[@class='article_author']/span")[0].text
    content_ = html_.xpath("//div[@class='article_text']//p")
    for i in content_:
        if i.text.strip():
            article.content += "    " + i.text.strip() + "\n\r"
    return article

############################################################
# sendmail

def _sendmail(account, from_name, to, subject, content) -> bool:
    # 需要的模块：email, smtplib。
    # The required module: email, smtplib.
    from email.mime.text import MIMEText
    from email.utils import parseaddr,formataddr
    from email.header import Header
    
    def _format_addr(s):
        name,addr = parseaddr(s)
        return formataddr((Header(name,"utf-8").encode(), addr if isinstance(addr,str) else addr))
    
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = _format_addr("{} <{}>".format(from_name, account["name"]))
    msg["To"] = to
    msg["Subject"] = subject
    
    import smtplib
    try:
        em = smtplib.SMTP_SSL(account["smtp_host"], account["smtp_port"])
        em.login(account["name"], account["password"])
        em.sendmail(msg["From"], msg["To"], msg.as_string())
        em.quit()
        print("Success!")
        return True
    except Exception as err:
        print("Failed!\n{}".format(err))
        return False

def sendmail(username: str, password: str, smtp_host: str, smtp_port: int,
    from_name: str, send_to: str, subject: str="主题", content="内容") -> bool:
    # 需要的模块：re。
    # 不包含调用函数中使用的模块。
    # The required module: re.
    # Does not contain the modules used in the calling function.
    account = {}
    account["name"] = username.strip()
    account["password"] = password.strip()
    account["smtp_host"] = smtp_host.strip()
    import re
    account["smtp_port"] = smtp_port if re.sub(r"[^\d]", r"", str(smtp_port)) == str(smtp_port) else 0
    
    if account["smtp_port"]==0:
        print("err")
        return False
    else:
        return _sendmail(account, from_name, send_to, subject, content)

# sendmail
############################################################


if __name__ == "__main__":
    pass
