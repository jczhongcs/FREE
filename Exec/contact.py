import os
import shutil
 
def CreateDir(path):
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        print(path+' 目录创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
 
def CopyFile(filepath, newPath):
    # 获取当前路径下的文件名，返回List
    fileNames = os.listdir(filepath)
    for file in fileNames:
        # 将文件命加入到当前文件路径后面
        newDir = filepath + '/' + file
        # 如果是文件
        if os.path.isfile(newDir):
            print(newDir)
            newFile = newPath + file
            shutil.copyfile(newDir, newFile)
        #如果不是文件，递归这个文件夹的路径
        else:
            CopyFile(newDir,newPath)                
 
if __name__ == "__main__":
    path1 = "E:\\SXR\\features1"
    path2 = "E:\\SXR\\features2"
    path3 = "E:\\SXR\\features3"
    path4 = "E:\\SXR\\features4"
    path5 = "E:\\SXR\\features5"
    path6 = "E:\\SXR\\features6"
    # 创建目标文件夹
    mkPath = "E:\\SXR\\features_zf"
    CreateDir(mkPath)
    CopyFile(path1,mkPath)
    CopyFile(path2,mkPath)
    CopyFile(path3,mkPath)
    CopyFile(path4,mkPath)
    CopyFile(path5,mkPath)
    CopyFile(path6,mkPath)