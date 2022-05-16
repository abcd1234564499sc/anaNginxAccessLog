#!/usr/bin/env python
# coding=utf-8
import os
import re

import openpyxl as oxl

import myUtils

header = ["源IP", "客户端用户名1", "客户端用户名2", "访问时间", "请求类型", "请求地址(URI)", "协议版本", "响应码", "请求包大小", "数据", "refer信息",
          "user-agent"]
logFiles = [r"test.log"]
obj = re.compile(
    r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?) (?P<request>.*?) (?P<requestPro>.*?)" (?P<status>.*?) (?P<bytes>.*?) (?P<data>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')
objErr = re.compile(
    r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?) ?(?P<request>.*) ?(?P<requestPro>.*?)" (?P<status>.*?) (?P<bytes>.*?) (?P<data>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')


def load_log(path):
    resultLine = []
    fileLines = []
    errorResultList = []
    with open(path, mode="r", encoding="utf-8") as f:
        fileLines = f.readlines()

    for rowIndex, line in enumerate(fileLines):
        print("\r正在解析{0}/{1}行".format(rowIndex + 1, len(fileLines)), end="")
        line = line.strip()
        if line == "":
            continue
        tmpResult = parse(line)
        if tmpResult == "":
            errorResultList.append({"index": rowIndex + 1, "content": line})
            continue
        resultLine.append(tmpResult)
    print("")
    return resultLine, errorResultList


def parse(line):
    # 解析单行nginx日志
    try:
        result = obj.match(line).groups()
    except:
        try:
            result = objErr.match(line).groups()
        except:
            result = ""
    return result


def writeExcell(ws, resultList, notAlignColIndexArr=[]):
    for rowIndex, result in enumerate(resultList):
        print("\r正在导出{0}/{1}行".format(rowIndex + 1, len(resultList)), end="")
        myUtils.writeExcellCell(ws, rowIndex + 2, 1, rowIndex + 1, 0, True)
        for headerIndex, headerText in enumerate(header):
            ifAlign = True
            if headerIndex + 1 in notAlignColIndexArr:
                ifAlign = False
            else:
                ifAlign = True
            myUtils.writeExcellCell(ws, rowIndex + 2, headerIndex + 2,
                                    result[headerIndex] if result[headerIndex] != "" else "-", 0, ifAlign)
        myUtils.writeExcellSpaceCell(ws, rowIndex + 2, len(header) + 2)
    print()


if __name__ == '__main__':
    for fileIndex, nowFile in enumerate(logFiles):
        print("---------------------------------------------------")
        fileName = os.path.split(nowFile)[1]
        print("开始处理文件：{0}({1}/{2})".format(nowFile, fileIndex + 1, len(logFiles)))
        print("正在解析文件")
        resultLine, errorLineList = load_log(nowFile)
        print("解析完成")

        excellFileName = fileName + ".xlsx"
        # 创建一个excell文件对象
        wb = oxl.Workbook()
        # 创建URL扫描结果子表
        ws = wb.active
        ws.title = fileName
        print("开始导出文件")
        myUtils.writeExcellHead(ws, ["序号"] + header)
        notAlignColIndexArr = [6, 10, 11, 12]  # 写入excell默认居中，该数组定义不居中的列序号，序号从0开始
        writeExcell(ws, resultLine, notAlignColIndexArr=notAlignColIndexArr)
        # 设置列宽
        colWidthArr = [7, 17, 17, 17, 30, 10, 70, 10, 10, 15, 40, 80, 80]
        myUtils.setExcellColWidth(ws, colWidthArr)
        # 设置冻结
        ws.freeze_panes="C2"
        myUtils.saveExcell(wb, excellFileName)
        print("成功导出文件：{}".format(excellFileName))
        if len(errorLineList) != 0:
            print("导出异常行数据")
            errorFileName = "error-{0}-{1}.txt".format(fileName, myUtils.getNowSeconed())
            errorFileName = myUtils.updateFileNameStr(errorFileName)
            with open(errorFileName, "w+", encoding="utf-8") as fr:
                for errorIndex, errorLine in enumerate(errorLineList):
                    print("\r正在导出{0}/{1}行".format(errorIndex + 1, len(errorLineList)), end="")
                    fr.write("行数：{0},内容：{1}\n".format(errorLine["index"], errorLine["content"]))
            print("\n成功导出异常内容文件：{}".format(errorFileName))

        print("---------------------------------------------------")
