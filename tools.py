# -*- coding: utf-8 -*-
import base64
try:
    import chardet
except ImportError:
    chardet = None
import hashlib
import importlib
import os
import re
import smtplib
try:
    import subprocess
except ImportError:
    subprocess = None
import sys
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.header import Header
try:
    import win32clipboard
except ImportError:
    win32clipboard = None
try:
    from lxml import etree
except ImportError:
    etree = None
try:
    from PIL import Image
except ImportError:
    Image = None
try:
    from requests_html import HTMLSession
    session = HTMLSession()
except ImportError:
    try:
        import requests as session
    except ImportError:
        session = None


def _restore(link) -> str:
    bytes_ = base64.b64decode(link)
    assert chardet, "Please install the `chardet` module."
    try:
        str_ = bytes_.decode(chardet.detect(bytes_)["encoding"])
    except (TypeError, AssertionError):
        try:
            str_ = bytes_.decode("utf8")
        except UnicodeDecodeError:
            str_ = bytes_.decode("gbk")
    return str_

############################################################
# allow

# allow([_type, ]_url)
def allow(*_str) -> bool:
    _url = ""
    _type = "*"
    regcom = re.compile(r"https?(://[^/]*)", re.I)
    while _url == "":
        for i in _str:
            if regcom.search(i):
                _url = i
            else:
                _type = i.upper()
    _list = _robots(_url)
    b = True  # 默认允许爬取
    if _list:
        for i in _list:
            # 爬虫名称或种类
            if i[0] == _type or i[0] == "*":
                i = i[1]
                for j in i:  # j ['Disallow', '.*?/s\\?.*']
                    reg = re.compile(j[1], re.I)
                    if reg.match(_url):  # fix 以第一个匹配到的为准。之前的写法是错的。
                        return False if j[0].upper() == "DISALLOW" else True
    return b

# 拼接链接，尝试http和https
def _robots(_url):
    url_com = str(re.search(r"https?(://[^/]*)", _url)[1])
    list1 = robots_(f"http{url_com}/robots.txt")
    if list1:
        return list1
    else:
        list2 = robots_(f"https{url_com}/robots.txt")
        return list2 if list2 else False

# _
def robots_(url):
    """
    任何一条Disallow记录为空，说明该网站的所有部分都允许被访问，在"/robots.txt"文件中，至少要有一条Disallow记录。
    如果"/robots.txt"是一个空文件，则对于所有的搜索引擎robot，该网站都是开放的。
    一个网站的所有URL默认是Allow的，所以Allow通常与Disallow搭配使用，实现允许访问一部分网页同时禁止访问其它所有URL的功能。
    需要特别注意的是Disallow与Allow行的顺序是有意义的，robot会根据第一个匹配成功的Allow或Disallow行确定是否访问某个URL。
    robots支持使用通配符"*"和"$"来模糊匹配url：  # 其他的不符合正则语法，需要转义
        "$" 匹配行结束符。
        "*" 匹配0或多个任意字符
    """
    assert session, "Please install the `requests_html` or `requests` module."
    cache = f"{md5(url)}.cache"
    status_code = None
    if not os.path.exists(cache):
        try:
            r = session.get(url)
        except:  # 尽量验证签名，（使用fiddler等）证书验证有问题时不验证签名。会有一个Warning，这样你就知道当前是没有验证签名的。也可以直接不验证签名，然后把Warning去掉，但不推荐。
            r = session.get(url, verify=False)
        status_code = r.status_code
        text = r.text
        with open(cache, "w", encoding="utf8") as f:
            f.write(text)
    else:
        with open(cache, "r", encoding="utf8") as f:
            text = f.read()
    if status_code == 200:
        _list1 = re.split(r"\n", text)
        list1 = []
        reg = re.compile(r"^User-agent:\s*(.*)", re.I)
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
                tmp = ".*?"+reg_.sub(r".*", regz.sub(r"\\\1", reg12.search(i)[3]))
                if not reg__.search(i):
                    tmp += ".*"
                list1[-1][1].append([reg12.search(i)[1], tmp])
            elif reg3.search(i):
                list1[-1][2].append(reg3.search(i)[1])
        return list1
    else:
        return False

# allow
############################################################

def chapterNum(aForHtml: str) -> str:
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

class Clipboard():
    @property
    def data(self):
        # Clipboard().data
        return self.getData()
    
    @data.setter
    def data(self, value):
        # Clipboard().data = "xxx"
        self.setData(value)
    
    @staticmethod
    def init():
        assert win32clipboard, "Please install the `win32clipboard` module."
        try:
            win32clipboard.CloseClipboard()  # 解决进程异常结束时可能存在的问题
        except:
            pass
    
    @staticmethod
    def getData():
        # Clipboard.getData()
        Clipboard.init()
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data

    @staticmethod
    def setData(data: str="") -> None:
        # Clipboard.setData()
        Clipboard.init()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(data)
        win32clipboard.CloseClipboard()

# download("http://www.baidu.com"[, path])
def download(*_str):
    if len(_str) > 0:
        url = _str[0]
        _type = re.sub(r".*//[^/]*", r"", url)
        _type = re.sub(r"[@\?].*", r"", _type)
        _type = re.sub(r".*/", r"", _type)
        try:
            _type = re.match(r".*?(\.[^\.]*)$", _type)[1]
        except:
            _type = ""
    else:
        return False
    if len(_str) > 1:
        fpath = _str[1] + md5(url) + _type
    else:
        fpath = md5(url) + _type
    if len(_str) > 2:
        new = _str[2]
    else:
        new = False
    if new or not os.path.exists(fpath):
        assert session, "Please install the `requests_html` or `requests` module."
        r = session.get(url)
        if r.status_code == 200:
            with open(fpath, "wb+") as f:
                f.write(r.content)
        else:
            raise Exception(f"The page request failed, the response code is: {r.status_code}\n\r")
        del r
    return os.path.abspath(fpath)

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

def flashgetLinkGenerator(link_: str) -> str:
    return "flashget://" + str(base64.b64encode(f"[FLASHGET]{link_}[FLASHGET]".encode("utf-8")))[2:-1]

def flashgetLinkRestore(link_: str):
    link = link_[11:]
    if len(link) == 0 or not link_.startswith("flashget://"):
        print("`{}`不是快车链接！".format(link_))
        return None
    return _restore(link)[10:-10]

def getIP(url):
    domain = len(re.findall(r"\.", url))
    if domain<1:
        return False
    assert session, "Please install the `requests_html` or `requests` module."
    if domain==1:
        r = session.get("https://{}.ipaddress.com".format(url))
    else:
        domain = re.search(r"[^\.]+\.[^\.]+$", url)[0]
        r = session.get("https://{}.ipaddress.com/{}".format(domain, url))
    _ip = re.findall("""https://www.ipaddress.com/ipv4/([\d\.]+)""", r.text)
    ip = []
    for i in _ip:
        if i not in ip:
            ip.append(i)
    return ip if ip else False

class hosts:
    """hosts in Windows"""
    def __init__(self, path: str=r"C:\WINDOWS\System32\drivers\etc\hosts"):
        self.path = path
        self.backup = os.path.join(os.getcwd(), "hosts_backup")
        os.system(f"copy {self.path} {self.backup}")
        self.new = os.path.join(os.getcwd(), "hosts_new")
        # 网络收集，不一定完善
        self._github_ = [
            "github.com", "api.github.com", "assets-cdn.github.com", "codeload.github.com",
            "gist.github.com", "avatars.githubusercontent.com", "camo.githubusercontent.com",
            "cloud.githubusercontent.com", "favicons.githubusercontent.com", "gist.githubusercontent.com",
            "raw.githubusercontent.com", "user-images.githubusercontent.com", "github.map.fastly.net",
            "github.githubassets.com", "github.global.ssl.fastly.net", "collector.githubapp.com",
            "github-releases.githubusercontent.com"
        ]
    
    def addGithub(self):
        self.removeGithub()
        os.system(f"copy {self.path} {self.backup}")
        os.system(f"copy {self.backup} {self.new}")
        with open(self.backup, "r", encoding="utf-8") as f:
            data = f.readlines()
        with open(self.new, "a+", encoding="utf-8") as f:
            f.write("# github\n")
            for value in self._github_:
                try:
                    ip_value = getIP(value)
                except AssertionError:  # 网页请求失败
                    continue
                print(f"{ip_value}    {value}")
                if ip_value:
                    for i in ip_value:
                        f.write(f"{i}    {value}\n")
                    continue
        assert subprocess, "Please install the `subprocess` module."
        subprocess.call(["copy", self.new, self.path, "/y"],shell=True)  # 复制到系统hosts路径
        subprocess.call(["ipconfig", "/flushdns"],shell=True)  # 刷新DNS缓存
        os.remove(self.new)
    
    def removeGithub(self):
        with open(self.backup, "r", encoding="utf-8") as f:
            data = f.readlines()
        with open(self.new, "w+", encoding="utf-8") as f:  # 清空文件
            pass
        _all_ = []
        with open(self.new, "a+", encoding="utf-8") as f:
            for i in data:
                if "github" in i:
                    if re.search(r"^#", i): continue  # 注释行
                    value = re.search(r"\d+\.\d+\.\d+\.\d+\s+([^\s]+)", i)[1]  # ipv4
                    if value: continue
                f.write(i)  # 其他
        assert subprocess, "Please install the `subprocess` module."
        subprocess.call(["copy", self.new, self.path, "/y"],shell=True)  # 复制到系统hosts路径
        subprocess.call(["ipconfig", "/flushdns"],shell=True)  # 刷新DNS缓存
        os.remove(self.new)
    
    def updateGithub(self):
        with open(self.backup, "r", encoding="utf-8") as f:
            data = f.readlines()
        with open(self.new, "w+", encoding="utf-8") as f:  # 清空文件
            pass
        _all_ = []
        with open(self.new, "a+", encoding="utf-8") as f:
            for i in data:
                if "github" in i:
                    if re.search(r"^#", i): continue  # 注释行
                    value = re.search(r"\d+\.\d+\.\d+\.\d+\s+([^\s]+)", i)[1]  # ipv4
                    if value in _all_: continue
                    _all_.append(value)
                    try:
                        ip_value = getIP(value)
                    except AssertionError:  # 网页请求失败
                        f.write(i)  # 保持不变
                        print(str(i))
                        continue
                    print(f"{ip_value}    {value}")
                    if ip_value:
                        for j in ip_value:
                            f.write(f"{j}    {value}\n")
                        continue
                f.write(i)  # 其他
        assert subprocess, "Please install the `subprocess` module."
        subprocess.call(["copy", self.new, self.path, "/y"],shell=True)  # 复制到系统hosts路径
        subprocess.call(["ipconfig", "/flushdns"],shell=True)  # 刷新DNS缓存
        os.remove(self.new)

class image:
    @staticmethod
    def compress(img: str, out: str="", out_size: int=150, step: int=10, quality: int=80):
        """保持图片长宽比例，压缩到指定大小size(KB)"""
        assert Image, "Please install the `PIL` module."
        img_size = os.path.getsize(img) / 1024
        if img_size <= out_size:
            return img
        name, suffix = os.path.splitext(img)
        if not out:
            out = f"{name}_compress{suffix}"
        im = Image.open(img)
        if re.search("jpe?g", os.path.splitext(out)[1], re.I):
            im = im.convert("RGB")  # fix `OSError: cannot write mode RGBA as JPEG`
        while img_size > out_size:
            im.save(out, quality=quality)
            img_size = os.path.getsize(out) / 1024
            if quality - step < 0:
                if step < 1 or quality <= 0: break
                step /= 2  # 动态调整
            quality -= step
        return out, img_size

def linkConverter(link_) -> dict:
    linkList = {}
    if link_.startswith("flashget://"):
        linkList["real"] = flashgetLinkRestore(link_)
    elif link_.startswith("qqdl://"):
        linkList["real"] = qqdlLinkRestore(link_)
    elif link_.startswith("thunder://"):
        linkList["real"] = thunderLinkRestore(link_)
    else:
        linkList["real"] = link_
    linkList["flashget"] = flashgetLinkGenerator(linkList["real"])
    linkList["qqdl"] = qqdlLinkGenerator(linkList["real"])
    linkList["thunder"] = thunderLinkGenerator(linkList["real"])
    return linkList

# md5(str[, encoding]) or md5(bytes) or md5(int)
def md5(*_str):
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

# tools.meiriyiwen().print()
def meiriyiwen(fdir="./cache/", new=False):
    """fdir: 缓存文件夹。new: 重新请求，默认优先使用已有缓存。"""
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
        _html = f.read()
        assert etree, "Please install the `lxml` module."
        html_ = etree.HTML(_html)
    article.title = html_.xpath("//h1")[0].text
    article.author = html_.xpath("//p[@class='article_author']/span")[0].text
    content_ = html_.xpath("//div[@class='article_text']//p")
    for i in content_:
        try:
            if i.text.strip():
                article.content += "    " + i.text.strip() + "\n\r"
        except Exception as err:  # todo 等待下一次报错，获取网页源码
            return err + "\n\r\n\r" + str(_html)
    return article

def qqdlLinkGenerator(link_: str) -> str:
    return "qqdl://" + str(base64.b64encode(link_.encode("utf-8")))[2:-1]

def qqdlLinkRestore(link_: str):
    link = link_[7:]
    if len(link) == 0 or not link_.startswith("qqdl://"):
        print("`{}`不是QQ旋风链接！".format(link_))
        return None
    return _restore(link)

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
    if path:
        sys_path_temp = list(sys.path)
        sys.path.insert(0, path)
    try:
        module_ = importlib.import_module(".", _module)
        _module_ = importlib.reload(module_)
        return _module_
    except ImportError as err:
        if path:
            sys.path = sys_path_temp
        if raise_:
            raise err
        return None

############################################################
# sendmail

def _sendmail(account, from_name, to, subject, content) -> bool:
    
    def _format_addr(s):
        name,addr = parseaddr(s)
        return formataddr((Header(name,"utf-8").encode(), addr if isinstance(addr,str) else addr))
    
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = _format_addr("{} <{}>".format(from_name, account["name"]))
    msg["To"] = to
    msg["Subject"] = subject
    
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
    account = {}
    account["name"] = username.strip()
    account["password"] = password.strip()
    account["smtp_host"] = smtp_host.strip()
    account["smtp_port"] = smtp_port if re.sub(r"[^\d]", r"", str(smtp_port)) == str(smtp_port) else 0
    
    if account["smtp_port"]==0:
        print("err")
        return False
    else:
        return _sendmail(account, from_name, send_to, subject, content)

# sendmail
############################################################

# 文本转语音，win10测试可行
def text2Speech(text) -> None:
    try:
        import win32com.client  # pip install pypiwin32
        # Microsoft Speech API
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
    except ImportError:
        # 语音识别的接口在我这电脑上不知道为什么用不了
        try:
            import speech
            speech.say(text)
        except SyntaxError:
            print("autofix: start")
            import os, sys
            for i in sys.path:
                if i.endswith("lib\\site-packages"):
                    path = os.path.join(i, "speech.py")
                    path_bak = os.path.join(i, "speech.py.bak")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf8") as f:
                            data = f.read()
                    with open(path_bak, "w", encoding="utf8") as f:
                        f.write(data)
                        print(f"backup: {path} => {path_bak}")
                    # python 有个 2to3 的小工具，但是这里的改动很少，直接替换也行
                    data = data.replace("import thread", "import _thread")\
                            .replace("print prompt", "print(prompt)")\
                            .replace("thread.start_new_thread(loop, ())",
                                "_thread.start_new_thread(loop, ())")
                    with open(path, "w", encoding="utf8") as f:
                        f.write(data)
            
            print("autofix: end")
            import speech
            speech.say(text)
        except ImportError as err:
            raise err

def thunderLinkGenerator(link_: str) -> str:
    return "thunder://" + str(base64.b64encode(f"AA{link_}ZZ".encode("utf-8")))[2:-1]

# 迅雷链接还原
def thunderLinkRestore(link_: str):
    link = link_[10:]
    if len(link) == 0 or not link_.startswith("thunder://"):
        print("`{}`不是迅雷链接！".format(link_))
        return None
    return _restore(link)[2:-2]


if __name__ == "__main__":
    print("部分功能测试（false表示存在异常）\n\r")
    
    temp = Clipboard.getData()
    Clipboard.setData("test")
    print("getClipboardData/setClipboardData: ", Clipboard.getData()=="test")
    Clipboard.setData(temp)  # 尝试恢复测试前的剪切板内容
    
    verify = {
        "flashget": "flashget://W0ZMQVNIR0VUXXRlc3RbRkxBU0hHRVRd",
        "qqdl": "qqdl://dGVzdA==",
        "real": "test",
        "thunder": "thunder://QUF0ZXN0Wlo="
    }
    linkList = linkConverter(verify["real"])
    print("flashgetLinkGenerator: ", linkList["flashget"]==verify["flashget"])
    print("flashgetLinkRestore: ", flashgetLinkRestore(verify["flashget"])==verify["real"])
    print("qqdlLinkGenerator: ", linkList["qqdl"]==verify["qqdl"])
    print("qqdlLinkRestore: ", qqdlLinkRestore(verify["qqdl"])==verify["real"])
    print("thunderLinkGenerator: ", linkList["thunder"]==verify["thunder"])
    print("thunderLinkRestore: ", thunderLinkRestore(verify["thunder"])==verify["real"])
    os.system("pause")
