import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold 

def visual(X):
    tsne=manifold.TSNE(n_components=2,init='pca',random_state=501)
    X_tsne=tsne.fit_transform(X)
    x_min,x_max=X_tsne.min(0),X_tsne.max(0)
    X_norm=(X_tsne-x_min)/(x_max-x_min)
    return X_norm


def caculate(a,b):
    dis=0
    for i in range(len(a)):
        dis+=(a[i]-b[i])**2
    dis**0.5
    return dis

#进行一次聚类的函数
def classify(arr,centroids,k):
    distance=[]#保存每个样本到各个质心距离的数组
    for i in range(len(arr)):
        distance.append([])
        for j in range(len(centroids)):
            distance[i].append(caculate(arr[i],centroids[j]))
    minDistIndices = np.argmin(distance, axis=1).tolist()#保存各个样本距离最小的质心
    cluster=[[],[],[],[],[],[]]#聚类列表
    for i in range(len(minDistIndices)):#进行聚类
        cluster[minDistIndices[i]].append(arr[i])
    newCentroid=[]
    for i in range(k):
        #调用numpy.mean()函数计算每个聚类的平均值，得到新质心
        newCentroid.append(np.mean(cluster[i],axis=0).tolist())
    return newCentroid,cluster


#k-means++算法中选择初始质心的函数
def chose(arr):
    centers=[]
    first_cent=random.sample(arr,1)[0]#随机生成第一个质心
    centers.append(first_cent)
    for cnt in range(5):#选取剩下的
        distance=[]#保存每个样本到已选取的各个质心距离的数组
        for i in range(len(arr)):
            dis=0
            for j in range(len(centers)):
                dis+=caculate(arr[i],centers[j])#计算到已有的质心的距离
            distance.append(dis)
        while 1:#按概率选取
            newone=random.choices(arr,distance,k=1)[0]#距离作为权重矩阵
            if newone not in centers:#确保不重复
                break
        centers.append(newone)
    return centers

def my_k_means(arr,k):
    # 随机取质心
    #centroids = random.sample(arr, k)
    #k_means++的初始质心选择：
    centroids=chose(arr)
    cnt=1
    newcentroids,cluster=classify(arr,centroids,6)
    while cnt<20:
        cnt+=1
        newcentroids,cluster=classify(arr,newcentroids,6)
        #打印相关的信息，可以看到每个聚类中的数目
        for i in range(len(cluster)):
            print(len(cluster[i]))
        print("--------------------------------------------",cnt)
    return newcentroids,cluster


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
        types.append(int(tmp1[1]))
        sentances.append(tmp2)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    X1 = transformer.fit_transform(vectorizer.fit_transform(sentances))
    name=vectorizer.get_feature_names_out().tolist()
    arr=X1.toarray().tolist()

    newcentroids,Cluster=my_k_means(arr,6)
    colour=['#000000','#0000FF','#FFFF00','#FF0000','#008000','#800080']
    allnum=0
    Clu=Cluster[:]
#---------计算罗德系数----------------------------------------------
    ra=0
    for i in range(len(Cluster)):
        for j in range(len(Cluster[i])):
            for k in range(j+1,len(Cluster[i])):
                if types[arr.index(Cluster[i][j])] == types[arr.index(Cluster[i][k])]:
                    ra+=1
    
    rb=0
    for i1 in range(len(Cluster)):
        for i2 in range(i1+1,len(Cluster)):
            for j1 in range(len(Cluster[i1])):
                for j2 in range(len(Cluster[i2])):
                    if types[arr.index(Cluster[i1][j1])] != types[arr.index(Cluster[i2][j2])]:
                        rb+=1

    com=math.factorial(len(arr))/(2*math.factorial(len(arr)-2))
    rand_index=(ra+rb)/com
    
#--------------------------------------------------------------------

    for i in range(len(Cluster)):
        Cluster[i]=visual(Cluster[i]).tolist()

    for i in range(len(Cluster)):
        x=[]
        y=[]
        cnt=[0,0,0,0,0,0]
        for j in range(len(Cluster[i])):
            cnt[types[arr.index(Clu[i][j])]-1]+=1
            x.append(Cluster[i][j][0])
            y.append(Cluster[i][j][1])
        cnt.sort(reverse=True)
        print("rate:",cnt[0]/len(Cluster[i]))
        plt.scatter(x, y, cmap=plt.cm.Spectral,marker='.',s=80,color=colour[i])
    print("rand index = ",rand_index)  
    plt.show()