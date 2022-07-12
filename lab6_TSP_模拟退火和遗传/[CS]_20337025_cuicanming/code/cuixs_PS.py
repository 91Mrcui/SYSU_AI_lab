from cmath import exp
import matplotlib.animation as animation
import sys
import matplotlib.pyplot as plt 
import random
import time
import math

from numpy import block

file = open("temp2.txt","r")
list = file.readlines()#每一行数据写入到list中
x1=[]
y1=[]
map_=[]


for fields in list:
    fields=fields.strip()#fields.strip()用来删除字符串两端的空白字符。
    fields=fields.strip("\n")    # fields.strip("[]")用来删除字符串两端方括号。
    tmp=fields.split(" ")
    for j in range(10):
        if '' in tmp:
            tmp.remove('')  
    temp=[]
    temp.append(int(tmp[0]))
    temp.append(float(tmp[1]))
    temp.append(float(tmp[2]))
    map_.append(temp)
    x1.append(temp[1])
    y1.append(temp[2])
    #print(tmp[1],tmp[2])

    #plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
    #plt.pause(0.005)
print(map_)

ims=[]
f1=plt.figure(1)
plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
#ims.append(im)
plt.show() 
#plt.pause(2)
#plt.close(fig)


#print(map_)
print(map_)

curr=random.sample(range(1, len(x1)+1), len(x1))

def distance(a,b):
    s=pow(map_[a-1][1]-map_[b-1][1],2)+pow(map_[a-1][2]-map_[b-1][2],2)
    return math.sqrt(s)

def evaluate(path):
    s=0
    for i in range (1,len(path)):
       s+=distance(path[i-1],path[i])
    s+=distance(path[0],path[len(path)-1])
    return s 


def neighbour1(path):
    leng=len(path)
    i=random.randint(1,leng-2)
    j=random.randint(2,leng-1)
    #print(i,"<->",j)
    #print(path)
    if i!=j:
        path[i],path[j]=path[j],path[i]
        tmp=path[:]
        path[i],path[j]=path[j],path[i]
    #print(path)
        return tmp
    else :
        return path


def neighbour3(path):
    leng=len(path)
    a1,a2,a3=random.sample(range(1, leng-1), 3) 
    if a1>a2:
        a1,a2=a2,a1
    if a2>a3:
        a2,a3=a3,a2
    if a1>a2:
        a1,a2=a2,a1
    tmp=path[0:a1]+path[a2:a3]+path[a1:a2]+path[a3:leng]
    return tmp

def neighbour2(path):
    leng=len(path)
    k1,k2=random.sample(range(1, leng-1), 2)
    if k1>k2:
        k1,k2=k2,k1
    tmp=path[0:k1]+path[k1:k2][::-1]+path[k2:leng]
    return tmp


#生成下一个状态
def neighbour4(path):
    leng=len(path)
    charge=random.random()
    if charge<0.334:
        a1,a2,a3=random.sample(range(1, leng-1), 3) 
        if a1>a2:
            a1,a2=a2,a1
        if a2>a3:
            a2,a3=a3,a2
        if a1>a2:
            a1,a2=a2,a1
        tmp=path[0:a1]+path[a2:a3]+path[a1:a2]+path[a3:leng]
    elif charge<0.666:
        i=random.randint(0,leng-2)
        j=random.randint(1,leng-1)
        #print(i,"<->",j)
        #print(path)
        if i!=j:
            path[i],path[j]=path[j],path[i]
            tmp=path[:]
            path[i],path[j]=path[j],path[i]
        else:
            tmp=path[:]

    else:
        k1,k2=random.sample(range(1, leng-1), 2)
        if k1>k2:
            k1,k2=k2,k1
        tmp=path[0:k1]+path[k1:k2][::-1]+path[k2:leng]
       

    return tmp
        
dis_change=[]#记录数组
fig1 = plt.figure(1)#用于生成动态图
tem=200000#迭代次数
while tem>0:
    tem-=1
    print(tem)#显示当前的迭代次数，便于观察
    child=neighbour4(curr)#生成下一个状态
    ori=evaluate(curr)
    new=evaluate(child)
    if ori>new:#只有更优时才接受
        curr=child[:]
        dis_change.append(new)

    
    #实时显示 
    if tem%3000==0:
        x1=[]
        y1=[]
        for var in curr:
            x1.append(map_[var-1][1])
            y1.append(map_[var-1][2])
        x1.append(map_[0][1])
        y1.append(map_[0][2]) 
        im=plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
        ims.append(im)
        #plt.draw()
        #plt.pause(0.01)# 间隔的秒数：6s
        #plt.close(fig)
    
print(evaluate(curr))

fig2 = plt.figure(2)#用于显示最终的解
xo=[]
yo=[]
for var in curr:
    xo.append(map_[var-1][1])
    yo.append(map_[var-1][2])

xo.append(map_[0][1])
yo.append(map_[0][2])

plt.title('Final solution of TSP')

plt.plot(xo, yo, marker = '.', color = 'red',linewidth=1) 
#ims.append(im)

#保存动态图
ani = animation.ArtistAnimation(fig1, ims, interval=200, repeat_delay=1000)
ani.save("PS.gif",writer='pillow')



fig3 = plt.figure(3)#用于显示总共费用的降低过程
plt.title('the evolution of the cost')
x_=[i for i in range(len(dis_change))]
plt.plot(x_,dis_change)
plt.show()
print("hh")

