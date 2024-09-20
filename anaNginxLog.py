#!/usr/bin/env python
# coding=utf-8
import os
import re

import openpyxl as oxl

import myUtils
from ExportExcellUtils import ExportExcellUtils
import warnings
warnings.filterwarnings("ignore")

headerDict = {}
headerDict["ip"] = "源IP"
# headerDict["username1"] = "客户端用户名1"
# headerDict["username2"] = "客户端用户名2"
headerDict["time"] = "访问时间"
headerDict["reqtype"] = "请求类型"
headerDict["request"] = "请求地址(URI)"
# headerDict["requestPro"] = "协议版本"
headerDict["status"] = "响应码"
headerDict["bytes"] = "请求包大小"
headerDict["data"] = "请求数据"
headerDict["referer"] = "refer信息"
headerDict["ua"] = "user-agent"

# 分析的日志后缀名
solveSuffixs=[]
solveSuffixs.append(".log")

# 匹配单行日志的正则表达式
anaLogRegStrList = []
anaLogRegStrList.append(r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?) (?P<request>/.*?) (?P<requestPro>HTTP/\d\.\d)" (?P<status>\d+?) (?P<bytes>\d+?) "(?P<data>.*?)" "(?P<referer>.*?)" "(?P<ua>.*?)"')
anaLogRegStrList.append(r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?) (?P<request>/.*?) (?P<requestPro>HTTP/\d\.\d)" (?P<status>\d+) (?P<bytes>\d+) "(?P<data>.*?)" "(?P<ua>.*?)"')
anaLogRegStrList.append(r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?) (?P<request>/.*?) (?P<requestPro>HTTP/\d\.\d)" (?P<status>\d+) (?P<bytes>\d+)')


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
        tmpResult = parseLogLine(line)
        if tmpResult == "":
            errorResultList.append({"index": rowIndex + 1, "content": line})
            continue
        resultLine.append(tmpResult)
    print("")
    return resultLine, errorResultList


def parseLogLine(line):
    # 解析单行日志
    result = ""
    for tmpAnaLogStr in anaLogRegStrList:
        reObj = re.compile(tmpAnaLogStr)
        try:
            result = reObj.match(line).groupdict()
            break
        except:
            continue
    return result


def solvedLogResults(resultList):
    showHeaderList = []
    useKeyList = []
    solvedResultList = []
    if len(resultList)!=0:
        firstResultDict =  resultList[0]
        useKeyList = [tmpKey for tmpKey in firstResultDict.keys() if tmpKey in headerDict.keys()]
        showHeaderList = [headerDict[tmpUseKey] for tmpUseKey in useKeyList]
    else:
        pass
    for tmpResultDict in resultList:
        tmpLineList = []
        for tmpUseKey in useKeyList:
            tmpLineList.append(tmpResultDict[tmpUseKey])
        solvedResultList.append(tmpLineList)
    return showHeaderList,solvedResultList


if __name__ == '__main__':
    logFolder = input("请输入想分析的日志所在的文件夹：")
    logFiles = []
    fileNames = os.listdir(logFolder)
    for tmpFileName in fileNames:
        tmpSuffix = os.path.splitext(tmpFileName)[1]
        if tmpSuffix in solveSuffixs:
            logFiles.append(os.path.join(logFolder, tmpFileName))
    exportExcellUtils = ExportExcellUtils(saveCount=10000)
    for fileIndex, nowFile in enumerate(logFiles):
        print("---------------------------------------------------")
        fileName = os.path.split(nowFile)[1]
        print("开始处理文件：{0}({1}/{2})".format(nowFile, fileIndex + 1, len(logFiles)))
        print("正在解析文件")
        resultLine, errorLineList = load_log(nowFile)
        print("解析完成")

        # 根据获得结果动态生成表头
        showHeaderList,solvedResultsList = solvedLogResults(resultLine)


        # 添加一个excell文件对象
        nowExcellFileObj = exportExcellUtils.addFile(fileName)
        nowExcellSheetObj = nowExcellFileObj.getFinalSheet()
        nowExcellSheetObj.sheetName = fileName
        nowExcellSheetObj.setHeaderList(exportExcellUtils.transformListToHeaderList(showHeaderList))
        nowExcellSheetObj.addRows([exportExcellUtils.transformListToCellList(tmpResults) for tmpResults in solvedResultsList])

        exportExcellUtils.exportExcell(fileIndex)

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
