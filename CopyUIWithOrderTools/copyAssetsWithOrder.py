#coding=utf-8
#拷贝UI资源到程序目录
import sys
import AssetsUtils

#中文版
uiAssetsPath = r'E:\Projects\voyage_wechatgame\develop\client\ui\uiproj\laya\assets\game'   #ui assets资源
progAssetsPath = r'E:\Projects\voyage_wechatgame\develop\client\trunk\h5client\laya\assets\game'    #程序 assets

#英文版
en_uiAssetsPath = r'E:\Projects\voyage_wechatgame\develop\client\ui\uiproj_en\laya\assets\game'   #ui assets资源
en_progAssetsPath = r'E:\Projects\voyage_wechatgame\develop\client\trunk\h5client\laya_en\assets\game'    #程序 assets

def cover_copy(commitOrders):
    # 按单号得到美术目录改动的文件
    # 将文件覆盖到程序目录
    #得到改动的ui资源目录
    cn_changeDirList = AssetsUtils.getChangeDirList(uiAssetsPath, commitOrders)
    en_changeDirList = AssetsUtils.getChangeDirList(en_uiAssetsPath, commitOrders)

    # 把改动目录覆盖到程序目录
    print("copy ui to prog")
    AssetsUtils.copyUItoProgDir(uiAssetsPath, progAssetsPath, cn_changeDirList)
    AssetsUtils.copyUItoProgDir(en_uiAssetsPath, en_progAssetsPath, en_changeDirList)

if __name__ == "__main__":
    #update svn
    updateList = [uiAssetsPath,progAssetsPath,en_uiAssetsPath,en_progAssetsPath]
    AssetsUtils.updateSvn(updateList)

    commitOrder = (sys.argv[1]).strip()
    print("order is:", commitOrder)
    commitOrders = commitOrder.split(',')

    AssetsUtils.order_files_change(commitOrders, uiAssetsPath, progAssetsPath)
    AssetsUtils.order_files_change(commitOrders, en_uiAssetsPath, en_progAssetsPath)
    print("finished")

