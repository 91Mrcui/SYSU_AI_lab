from cgi import test
import math
from ntpath import join
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#向量内积的方法
def neiji(t1,t2):
    mul=0
    for i in range(0,len(t1)):
        mul+=t1[i]*t2[i]    
    return mul

#余弦相似度的方法，使用时记得将sort函数的参数reverse设置为true
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
    all=[]#记录距离和对应类型的列表
    index=sentances.index(sen)#找到对应下标
    for i in range(0,1247):
        dis=0
        #计算曼哈顿距离
        for j in range(len(arr[i])):
            hot=arr[index][j]
            tmp=abs(hot-arr[i][j])          
            dis+=tmp
        #采用元组的方式记录
        t=(dis,types[i])
        all.append(t)
    all.sort(reverse=True)#对距离进行从小到大排序
    cnt=[0,0,0,0,0,0]#统计前k个中每个类型出现的次数
    #k取14
    for i in range(14):
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
    #找到出现次数最多的类型
    for i in range(6):
        if cnt[i]>max:
            max=cnt[i]
            flag=i           
    return flag+1

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
    #得到tf_idf矩阵X1
    X1 = transformer.fit_transform(vectorizer.fit_transform(sentances))
    #矩阵中每一列对应的特征列表
    name=vectorizer.get_feature_names_out().tolist()
    #将矩阵转为列表
    arr=X1.toarray().tolist()
   

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


    