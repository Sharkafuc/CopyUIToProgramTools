#coding=utf-8
import sys
import os
import re
import shutil
from xml.etree import cElementTree

#执行且返回结果
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def arrayToPatStr(array):
    ret = ''
    for item in array:
        ret += str(item) + '|'
    ret = ret[:-1]
    return ret

def getRightStrOrder(array):
    ret = []
    for item in array:
        if len(item) == 4:
            ret.append(item)
    print("right str order:",ret)
    return ret

#获取UI目录下被版本号改动的目录
def getChangeDirList(uiAssetsPath,commitOrders):
    commitOrders = getRightStrOrder(commitOrders)
    orderStr = arrayToPatStr(commitOrders)
    dirChildren = os.listdir(uiAssetsPath)
    changeDirList = []
    for dir in dirChildren:
        dirPath = os.path.join(uiAssetsPath, dir)
        if (os.path.isdir(dirPath)):
            exeStr = "svn log " + dirPath + " -l 10"
            exeResult = execCmd(exeStr)
            patstr = r'.*?#'+orderStr+'.*?\【?.*?\】?'
            orderMatch = re.search(patstr, exeResult)
            if orderMatch:
                changeDirList.append(dir)
                print("get change dir:",dir)
    print("changeDirList:",changeDirList)
    return changeDirList

#更新SVN
def updateSvn(updateArray):
    for updatePath in updateArray:
        command = r'svn update '+updatePath
        print(command)
        os.system(command)

#从UI目录将改动拷贝到程序目录
def copyUItoProgDir(uiPath,progPath,changeDirList):
    for dir in changeDirList:
        rmcmd = r'rd /s /q '+progPath+'\\' + dir
        print(rmcmd)
        os.system(rmcmd)

        cpcmd = r'xcopy '+uiPath+'\\'+dir+' '+progPath+'\\'+dir+'\\ /e'
        print(cpcmd)
        os.system(cpcmd)

#获取最近cnt条log
def getDirLatestCntLog(cnt,dirPath):
    exeStr = "svn log " + dirPath + " -l "+str(cnt)
    exeResult = execCmd(exeStr)
    return exeResult

def getLoglines(rawlog):
    patstr = r'------------------------------------------------------------------------([\s\S]+?#\d{4}.*?\【?.*?\】?)'
    logLines = re.findall(patstr,rawlog)
    return logLines


#获取log中特定单号的版本号
def getRevisionsFromLogOrders(log,commitOrders):
    loglines = getLoglines(log)
    revisions = []
    commitOrders = getRightStrOrder(commitOrders)
    orderStr = arrayToPatStr(commitOrders)
    for eachlog in loglines:
        patstr = r'[\s\S]+r(\d+)[\s\S]+#' + orderStr + '.*?\【?.*?\】?'
        orderMatch = re.match(patstr, eachlog)
        if orderMatch:
            revision = orderMatch.group(1)
            if revision not in revisions:
                revisions.append(revision)
    return revisions

#获取log中特定版本的文件改动
def getChangesFromRevisions(uiProjPath,revisions):
    revisions.sort()
    exeStr = "svn log "+uiProjPath+" -v "
    exeResult = None
    if len(revisions) > 0:
        for rivision in revisions:
            exeStr += "-r"+rivision+" "
        exeResult = execCmd(exeStr)
    rel_url = getSVNRelativePath(uiProjPath)
    patstr = r'([A|D|M].*?' + rel_url + '/.*)\n'
    changeList = []
    if exeResult:
        changeList = re.findall(patstr,exeResult)
    return changeList

#获取SVN相对路径
def getSVNRelativePath(path):
    exeStr = "svn info " + path + " --xml"
    exeResult = execCmd(exeStr)
    root = cElementTree.fromstring(exeResult)
    return root.find("entry/relative-url").text[1:]

def doChangesBetweenPaths(changeList,srcPath,destPath):
    for change in changeList:
        rel_url = getSVNRelativePath(srcPath)
        patstr = r'([A|D|M]).*?'+rel_url+'(/.*)'
        changematch = re.match(patstr, change)
        if changematch:
            operate = changematch.group(1)
            rel_file = changematch.group(2).replace("/","\\")
            src_file_name = srcPath + rel_file
            dest_file_name = destPath + rel_file
            if os.path.exists(src_file_name):
                #存在，可以拷贝
                if os.path.isfile(src_file_name):
                    #文件
                    if operate in ["M","A"]:
                        cover_copy_file(src_file_name,dest_file_name)
                else:
                    #目录
                    if operate == "A":
                        add_dir(src_file_name,dest_file_name)

            else:
                #不存在，可以删除
                if operate == "D":
                    if os.path.isfile(dest_file_name):
                        #文件
                        delete_file(src_file_name, dest_file_name)
                    else:
                        #目录
                        delete_dir(src_file_name,dest_file_name)



def cover_copy_file(src, dest):
    if os.path.exists(src) and os.path.isfile(src):
        shutil.copy(src, dest)

def add_dir(src, dest):
    if os.path.exists(src) and os.path.exists(dest) == False and os.path.isdir(src):
        shutil.copytree(src, dest)

def delete_file(src, dest):
    if os.path.exists(src) == False and os.path.exists(dest) and os.path.isfile(dest):
        os.remove(dest)

def delete_dir(src,dest):
    if os.path.exists(src) == False and os.path.exists(dest) and os.path.isdir(dest):
        shutil.rmtree(dest)

file_operate_handler = {
    "M":cover_copy_file,
    "A":cover_copy_file,
    "D":delete_file,
}

dir_operate_handler = {
    "A":add_dir,
    "D":delete_dir,
}

def order_files_change(commitOrders,uiProjPath,progProjPath):
    uiProjLast10Log = getDirLatestCntLog(10,uiProjPath)
    uiProjRevisions = getRevisionsFromLogOrders(uiProjLast10Log,commitOrders)
    uiProjChanges = getChangesFromRevisions(uiProjPath,uiProjRevisions)
    doChangesBetweenPaths(uiProjChanges,uiProjPath,progProjPath)

