from cgi import test
import math
from ntpath import join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
## pca特征降维
# 导入相关模块
#coding=utf-8
from numpy import *
import seaborn as sns
import matplotlib.pyplot as plt
from numpy.linalg import eig
from sklearn.datasets import load_iris
import sys


def neiji(t1,t2):
    mul=0
    for i in range(0,len(t1)):
        mul+=t1[i]*t2[i]    
    return mul

def caculate_cos(t1,t2):
    abst1=0
    abst2=0
    mul=0
    for i in range(0,len(t1)):
        abst1+=t1[i]*t1[i]
        abst2+=t2[i]*t2[i]
        mul+=t1[i]*t2[i]
    abst1=math.sqrt(abst1)
    abst2=math.sqrt(abst2)    
    return mul/(abst1+abst2)



def classify_knn(sen,arr,types,sentances):
    all=[]
    index=sentances.index(sen)
    for i in range(0,1247):
        dis=0
        #if dis!=0:
        #    print(dis)
        #for j in range(len(arr[i])):
        #    hot=arr[index][j]
        #    tmp=(hot-arr[i][j])*(hot-arr[i][j])
        #    tmp=math.sqrt(tmp)
        #    dis+=tmp

        for j in range(len(arr[i])):
            hot=arr[index][j]
            dx=hot.real-arr[i][j].real
            dy=hot.imag-arr[i][j].imag
            tmp=dx*dx+dy*dy
            dis+=tmp

        t=(dis,types[i])
        all.append(t)
    all.sort()
    cnt=[0,0,0,0,0,0]
    for i in range(30):
        #print(all[i])
        if all[i][1]=='1':
            cnt[0]+=1
        elif all[i][1]=='2':
            cnt[1]+=1
        elif all[i][1]=='3':
            cnt[2]+=1
        elif all[i][1]=='4':
            cnt[3]+=1
        elif all[i][1]=='5':
            cnt[4]+=1
        elif all[i][1]=='6':
            cnt[5]+=1   
    max=-999
    flag=-1
    for i in range(6):
        if cnt[i]>max:
            max=cnt[i]
            flag=i           
    return flag+1


def eigValPct(eigVals,percentage):
    sortArray=sort(eigVals) #使用numpy中的sort()对特征值按照从小到大排序
    sortArray=sortArray[-1::-1] #特征值从大到小排序
    arraySum=sum(sortArray) #数据全部的方差arraySum
    tempSum=0
    num=0
    for i in sortArray:
        tempSum+=i
        num+=1
        if tempSum >=arraySum*percentage:
            return num

'''pca函数有两个参数，其中dataMat是已经转换成矩阵matrix形式的数据集，列表示特征；
其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
def pca(dataMat,percentage=0.99):
    meanVals=mean(dataMat,axis=0)  #对每一列求平均值，因为协方差的计算中需要减去均值
    meanRemoved=dataMat-meanVals
    covMat=cov(meanRemoved,rowvar=0)  #cov()计算方差
    eigVals,eigVects=linalg.eig(mat(covMat))  #利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
    #k=eigValPct(eigVals,percentage) #要达到方差的百分比percentage，需要前k个向量
    k=134  #选取k为134
    eigValInd=argsort(eigVals)  #对特征值eigVals从小到大排序
    eigValInd=eigValInd[:-(k+1):-1] #从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
    redEigVects=eigVects[:,eigValInd]   #返回排序后特征值对应的特征向量redEigVects（主成分）
    lowDDataMat=meanRemoved*redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
    reconMat=(lowDDataMat*redEigVects.T)+meanVals   #得到重构数据reconMat
    return lowDDataMat,reconMat,k


if __name__ == '__main__':

    delset=[]
    file =open("ban.txt","r")
    dlist=file.readlines()
    file.close()
    for i in range(0,len(dlist)):
        dlist[i]=dlist[i].strip("\n") 
        delset.append(dlist[i])

    file = open("all.txt","r")
    list = file.readlines()#每一行数据写入到list中
    file.close()
    sentances=[]
    types=[]

    for i in range(1,len(list)):
        list[i]=list[i].strip("\n") 
        tmp1=list[i].split()
        tmp2=tmp1[3:len(tmp1)]
        
        for k in tmp2[:]:
            if k in delset:
                tmp2.remove(k)

        tmp2=" ".join(tmp2)
        sentances.append(tmp2)
        types.append(tmp1[1])
           

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    X1 = transformer.fit_transform(vectorizer.fit_transform(sentances))
    #X1 = vectorizer.fit_transform(sentances)
    name=vectorizer.get_feature_names_out().tolist()
    arr=X1.toarray().tolist()
    
    #pca--------------------------------------------------------------
    a,b,c=pca(X1.toarray())
    #print(a)
    print("len(a)=",len(a[1]))
    print("len(b)=",len(b[1]))
    print("-----------------------------------------")
    arr=a.tolist()
    #for k in arr:
    #    print(k)
    print(c)
    print(len(name))




    #测试
    file = open("train.txt","r")
    test_list = file.readlines()#每一行数据写入到test_list中
    file.close()
    right=0     #统计正确的数量
    wrong=0     #统计错误的数量
    for i in range(1,len(test_list)):
        test_list[i]=test_list[i].strip("\n") 
        tmp1=test_list[i].split()
        tmp2=tmp1[3:len(tmp1)] 
        for k in tmp2[:]:
            if k in delset:
                tmp2.remove(k)
        ts=" ".join(tmp2) 
        correct=tmp1[1]
        charge=classify_knn(ts,arr,types,sentances)    #分类
        if charge == int(correct):
            right+=1
        else:
            wrong+=1         
        print('判断:',charge,'正确:',int(correct),tmp2)#输出分类结果
    print("rate: ",100*right/len(test_list),"%",sep='')#输出正确率
