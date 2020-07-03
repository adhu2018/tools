# -*- coding: utf-8 -*-
import re


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

if __name__ == '__main__':
    pass
