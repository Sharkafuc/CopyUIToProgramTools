# -*- coding: utf-8 -*-
#拷贝UI工程到程序目录

import sys
import AssetsUtils

#中文版
uiProjPath = r'E:\Projects\voyage_wechatgame\develop\client\ui\uiproj\laya\pages\game'   #ui ui工程
progProjPath = r'E:\Projects\voyage_wechatgame\develop\client\trunk\h5client\laya\pages\game'    #程序 ui工程

#英文版
en_uiProjPath = r'E:\Projects\voyage_wechatgame\develop\client\ui\uiproj_en\laya\pages\game'   #ui ui工程
en_progProjPath = r'E:\Projects\voyage_wechatgame\develop\client\trunk\h5client\laya_en\pages\game'    #程序 ui工程

def cover_copy(commitOrders):
    # 得到改动的ui资源目录
    cn_changeDirList = AssetsUtils.getChangeDirList(uiProjPath, commitOrders)
    en_changeDirList = AssetsUtils.getChangeDirList(en_uiProjPath, commitOrders)

    # 把改动目录覆盖到程序目录
    AssetsUtils.copyUItoProgDir(uiProjPath, progProjPath, cn_changeDirList)
    AssetsUtils.copyUItoProgDir(en_uiProjPath, en_progProjPath, en_changeDirList)

if __name__ == "__main__":
    # update svn
    updateList = [uiProjPath,progProjPath,en_uiProjPath,en_progProjPath]
    AssetsUtils.updateSvn(updateList)

    commitOrder = (sys.argv[1]).strip()
    print("order is:", commitOrder)
    commitOrders = commitOrder.split(',')

    AssetsUtils.order_files_change(commitOrders,uiProjPath,progProjPath)
    AssetsUtils.order_files_change(commitOrders, en_uiProjPath, en_progProjPath)
    print("finished")