#!/usr/bin/python
#coding=utf-8  

import os,zipfile,shutil  


#要压缩的文件目录
myFilePath = '/Users/llbt/Desktop/MBSiPhone'
#要压缩的文件拷贝目录
myFilePathCopy = myFilePath + '_copy'

#  info.plist文件
infoFilePath = myFilePath + '/MBSiPhone/MBSiPhone-Info.plist' 


# 获取Xcode工程版本号
def getXcodeVersion():
    count = 0;
    verson = ''
    with open(infoFilePath, 'r') as f:
         for line in f.readlines():
             if count == 1:
                return line.strip()[8:14]
             if 'CFBundleShortVersionString' in line.strip():
                count+=1
         return ''

print getXcodeVersion()
#压缩文件要到哪个目录
mySavePath = '/Users/llbt/Desktop/v%s版本/'%getXcodeVersion()


# 创建zip文件
def createZip(filePath,savePath):  
    ''''' 
    将文件夹下的文件保存到zip文件中。 
    :param filePath: 待备份文件 
    :param savePath: 备份路径 
    :return: 
    '''  
    # 压缩的文件列表
    fileList=[]  
   
    # 目标目录不存在 创建目录
    if os.path.exists(savePath):  
        pass
    else:
         os.makedirs(savePath)  

          #  保存路径
    target = savePath + 'MBSiPhone.zip'
    #创建zip 
    newZip = zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED)  



    #遍历备份文件
    for dirpath,dirnames,filenames in os.walk(filePath):  
    	print(dirnames);
    	print(filenames);
        for filename in filenames:  
            fileList.append(os.path.join(dirpath,filename))  
    for tar in fileList:  
        newZip.write(tar,tar[len(filePath):])#tar为写入的文件，tar[len(filePath)]为保存的文件名  
    newZip.close()  
    print('backup to',target)  

# 删除特定名字目录
def MBS_DeleteDir(rootdir,search_dir_name):
    if os.path.isdir(rootdir):
        list_new = os.listdir(rootdir)
        for  it in list_new:
            if it == search_dir_name: 
                #os.rmdir(os.path.join(rootdir,it)) #不能删除有文件的文件夹
                shutil.rmtree(os.path.join(rootdir,it))
            else:
                MBS_DeleteDir(os.path.join(rootdir,it),search_dir_name)
    else:
        return

# 如果存在备份目录 删除
if (os.path.exists(myFilePathCopy)):
    shutil.rmtree(myFilePathCopy)
# 拷贝原目录到备份目录
shutil.copytree(myFilePath,myFilePathCopy)
# 删除打包文件夹
MBS_DeleteDir(myFilePathCopy,'build')
# 删除svn信息
MBS_DeleteDir(myFilePathCopy,'.svn')
# 压缩文件
createZip(myFilePathCopy,mySavePath)    