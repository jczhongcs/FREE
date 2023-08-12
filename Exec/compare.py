# 判断两个文件是否相同。要求用函数实现文件比较功能，在main函数中进行验证。
# 下述函数完成文件是否相同的比较功能
def compareFile(file1,file2):
    #请在此添加代码，实现文件是否相同的判断
    # 如果相等返回[1,0,0]
    # 如果不相等返回[0,a,b] a,b表示第一个不相等字符所在的行号和列号
    #********** Begin *********#
    len1=len(file1)
    len2=len(file2)
    minlen1=min(len1,len2)          #计算两个列表的最小行数
    for i in range(minlen1):        #用最小行数进行迭代和比较
        if(file1[i]!=file2[i]):     #如果两行不相等，判断是在哪一列不相等 
           #获取这两行最小列数
            minlen2=min(len(file1[i]),len(file2[i]))
            for j in range(minlen2):        #用最小的列数进行迭代和比较
                if(file1[i][j]!=file2[i][j]):
                    return [0,i+1,j+1]      #返回不相等所在的行号和列号
            else:
                #若这两行的列数不相同，则也不相等
                if(len(file1)!=len(file2)):
                    return [0,i+1,1]
    else:
        #若这两个文件的行数不同，则也不相等
        if(len(file1)!=len(file2)):
            return [0,minlen1+1,1]
        else:
            return [1,0,0]
    #********** End *********#

# 定义函数main，完成文件名输入、比较函数调用和结果输出功能
def main():
    # 输入两个文件所在路径和文件名，如：d:\temp\t1.txt
    str1=input('E:\\SXR\\ouput_envs_envcnn\\Envelope_1332.env')
    str2=input('E:\\SXR\\ouput_envs_envcnnme\\Envelope_1332.env')
    #请在此添加代码，完成相应功能
    #********** Begin *********#
    file1=open(str1,'r')
    file2=open(str2,'r')        #以只读方式打开文件
    #用readlines（）方法把文件内容逐行读入一个列表对象
    lsFile1=file1.readlines()       
    lsFile2=file2.readlines()
    file1.close()
    file2.close()
    result,row,col=compareFile(lsFile1,lsFile2)
    if(result==1):
        #函数第一个返回结果为1，则相等
        print("这两个文件相等")
    else:
        print("这两个文件在{0}行{1}列开始不相等".format(row,col))
    #********** End *********#

main()
