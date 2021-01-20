# -*- coding: utf-8 -*-
import os
from lxml import etree
try:
    from .download import download
except ImportError:
    import download

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
        html_ = f.read()
        html_ = etree.HTML(html_)
    article.title = html_.xpath("//h1")[0].text
    article.author = html_.xpath("//p[@class='article_author']/span")[0].text
    content_ = html_.xpath("//div[@class='article_text']//p")
    for i in content_:
        if i.text.strip():
            article.content += "    " + i.text.strip() + "\n\r"
    return article


if __name__ == "__main__":
    pass
