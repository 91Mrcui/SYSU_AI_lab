from cgi import test
from ntpath import join
from sklearn.feature_extraction.text import CountVectorizer


def caculate(num,arr,test_sentabce,name):
    res=0
    for i in range(0,len(arr[num])):
        mul=1
        for j in range(0,len(test_sentabce)):
            if test_sentabce[j] in name[num]:
                now=name[num].index(test_sentabce[j])
                mul*=arr[num][i][now]
                
            else:
                continue 
        res+=mul

    return res

def classify(arr,test_sentabce,name):
    max=-9999
    flag=-1
    for i in range(6):
        res=caculate(i,arr,test_sentabce,name)
        if res>max:
            max=res
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

    file = open("train.txt","r")
    list = file.readlines()#每一行数据写入到list中
    file.close()
    anger_set=[]
    disgust_set=[]
    fear_set=[]
    joy_set=[]
    sad_set=[]  
    surprise_set=[]

    for i in range(1,len(list)):
        list[i]=list[i].strip("\n") 
        tmp1=list[i].split()
        tmp2=tmp1[3:len(tmp1)]
        
        for k in tmp2[:]:
            if k in delset:
                tmp2.remove(k)
        
        tmp2=" ".join(tmp2)
        if tmp1[1]=='1':
            anger_set.append(tmp2)
         
        elif tmp1[1]=='2':
            disgust_set.append(tmp2)
          
        elif tmp1[1]=='3':
            fear_set.append(tmp2)
        
        elif tmp1[1]=='4':
            joy_set.append(tmp2)
        
        elif tmp1[1]=='5':
            sad_set.append(tmp2)
         
        elif tmp1[1]=='6':
            surprise_set.append(tmp2)
           

    arr=[]
    name=[]
    vectorizer = CountVectorizer()
    X1 = vectorizer.fit_transform(anger_set)
    name1=vectorizer.get_feature_names_out().tolist()
    arr1=X1.toarray().tolist()
    
    #将字符串转为列表方便操作
    for i in range(len(anger_set)):
        anger_set[i]=anger_set[i].split()

    #计算TF的过程
    for i1 in range(len(arr1)):
        for i2 in range(len(arr1[i1])):
            total_len=len(anger_set[i1]) #该句子的长度
            cnt=0
            for i3 in range(total_len):
                if anger_set[i1][i3]==name1[i2]:
                    cnt+=1
            arr1[i1][i2]=cnt

    #归一和平滑过程：
    sum=0
    for i in range(len(arr1)):
        sum=0
        for j in range(len(arr1[i])):
            sum+=arr1[i][j]
        sum+=len(name1)
        for j in range(len(arr1[i])):
            arr1[i][j]=(arr1[i][j]+1)/sum#贝叶斯估计
            arr1[i][j]*=10000000
    arr.append(arr1)
    name.append(name1)
    #----------------------下面的都是重复劳动--------------------------------------------------------
    vectorizer = CountVectorizer()
    X2 = vectorizer.fit_transform(disgust_set)
    name2=vectorizer.get_feature_names_out().tolist()
    arr2=X2.toarray().tolist()
    for i in range(len(disgust_set)):
        disgust_set[i]=disgust_set[i].split()
    for i1 in range(len(arr2)):
        for i2 in range(len(arr2[i1])):
            total_len=len(disgust_set[i1])
            cnt=0
            for i3 in range(total_len):
                if disgust_set[i1][i3]==name2[i2]:
                    cnt+=1
            arr2[i1][i2]=cnt
    sum=0
    for i in range(len(arr2)):
        sum=0
        for j in range(len(arr2[i])):
            #sum+=pow(arr1[i][j],2)
            sum+=arr2[i][j]
        sum+=len(name2)
        for j in range(len(arr2[i])):
            arr2[i][j]=(arr2[i][j]+1)/sum
            arr2[i][j]*=10000000

    arr.append(arr2)
    name.append(name2)
    #------------------------------------------------------------------------------
    vectorizer = CountVectorizer()
    X3 = vectorizer.fit_transform(fear_set)
    name3=vectorizer.get_feature_names_out().tolist()
    arr3=X3.toarray().tolist()
    for i in range(len(fear_set)):
        fear_set[i]=fear_set[i].split()
    for i1 in range(len(arr3)):
        for i2 in range(len(arr3[i1])):
            total_len=len(fear_set[i1])
            cnt=0
            for i3 in range(total_len):
                if fear_set[i1][i3]==name3[i2]:
                    cnt+=1
            arr3[i1][i2]=cnt
    sum=0
    for i in range(len(arr3)):
        sum=0
        for j in range(len(arr3[i])):
            #sum+=pow(arr1[i][j],2)
            sum+=arr3[i][j]
        sum+=len(name3)
        for j in range(len(arr3[i])):
            arr3[i][j]=(arr3[i][j]+1)/sum
            arr3[i][j]*=10000000
    arr.append(arr3)
    name.append(name3)
    #------------------------------------------------------------------------------
    vectorizer = CountVectorizer()
    X4 = vectorizer.fit_transform(joy_set)
    name4=vectorizer.get_feature_names_out().tolist()
    arr4=X4.toarray().tolist()
    for i in range(len(joy_set)):
        joy_set[i]=joy_set[i].split()
    for i1 in range(len(arr4)):
        for i2 in range(len(arr4[i1])):
            total_len=len(joy_set[i1])
            cnt=0
            for i3 in range(total_len):
                if joy_set[i1][i3]==name4[i2]:
                    cnt+=1
            arr4[i1][i2]=cnt
    sum=0
    for i in range(len(arr4)):
        sum=0
        for j in range(len(arr4[i])):
            #sum+=pow(arr1[i][j],2)
            sum+=arr4[i][j]
        sum+=len(name4)
        for j in range(len(arr4[i])):
            arr4[i][j]=(arr4[i][j]+1)/sum
            arr4[i][j]*=10000000
    arr.append(arr4)
    name.append(name4)
    #------------------------------------------------------------------------------
    vectorizer = CountVectorizer()
    X5 = vectorizer.fit_transform(sad_set)
    name5=vectorizer.get_feature_names_out().tolist()
    arr5=X5.toarray().tolist()
    for i in range(len(sad_set)):
        sad_set[i]=sad_set[i].split()
    for i1 in range(len(arr5)):
        for i2 in range(len(arr5[i1])):
            total_len=len(sad_set[i1])
            cnt=0
            for i3 in range(total_len):
                if sad_set[i1][i3]==name5[i2]:
                    cnt+=1
            arr5[i1][i2]=cnt
    sum=0
    for i in range(len(arr5)):
        sum=0
        for j in range(len(arr5[i])):
            #sum+=pow(arr1[i][j],2)
            sum+=arr5[i][j]
        sum+=len(name5)
        for j in range(len(arr5[i])):
            arr5[i][j]=(arr5[i][j]+1)/sum
            arr5[i][j]*=10000000
    arr.append(arr5)
    name.append(name5)
    #------------------------------------------------------------------------------
    vectorizer = CountVectorizer()
    X6 = vectorizer.fit_transform(surprise_set)
    name6=vectorizer.get_feature_names_out().tolist()
    arr6=X6.toarray().tolist()
    for i in range(len(surprise_set)):
        surprise_set[i]=surprise_set[i].split()
    for i1 in range(len(arr6)):
        for i2 in range(len(arr6[i1])):
            total_len=len(surprise_set[i1])
            cnt=0
            for i3 in range(total_len):
                if surprise_set[i1][i3]==name6[i2]:
                    cnt+=1
            arr6[i1][i2]=cnt
    sum=0
    for i in range(len(arr6)):
        sum=0
        for j in range(len(arr6[i])):
            #sum+=pow(arr1[i][j],2)
            sum+=arr6[i][j]
        sum+=len(name6)
        for j in range(len(arr6[i])):
            arr6[i][j]=(arr6[i][j]+1)/sum
            arr6[i][j]*=10000000
    arr.append(arr6)
    name.append(name6)
    #---------------------------重复劳动结束，对测试集进行测试---------------------------------------------------
    file = open("test.txt","r")
    test_list = file.readlines()#每一行数据写入到test_list中
    file.close()
    right=0     #统计正确的数量
    wrong=0     #统计错误的数量
    for i in range(1,len(test_list)):
        test_list[i]=test_list[i].strip("\n") 
        tmp1=test_list[i].split()
        tmp2=tmp1[3:len(tmp1)]  
        correct=tmp1[1]
        charge=classify(arr, tmp2, name)    #分类
        if charge == int(correct):
            right+=1
        else:
            wrong+=1         
        print('判断:',charge,'正确:',int(correct),tmp2)#输出分类结果
    print("rate: ",100*right/len(test_list),"%",sep='')#输出正确率