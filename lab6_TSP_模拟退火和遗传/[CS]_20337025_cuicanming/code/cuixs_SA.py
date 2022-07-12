from cmath import exp
import sys
import matplotlib.pyplot as plt 
import random
import math
import matplotlib.animation as animation

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
    
print(map_)
f1=plt.figure(1)
plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
plt.show()


print(map_)

#随机生成初始状态
curr=random.sample(range(1, len(x1)+1), len(x1))


#计算两个城市之间的距离
def distance(a,b):
    s=pow(map_[a-1][1]-map_[b-1][1],2)+pow(map_[a-1][2]-map_[b-1][2],2)
    return math.sqrt(s)

#评估函数，返回距离总和
def evaluate(path):
    s=0
    for i in range (1,len(path)):
       s+=distance(path[i-1],path[i])
    s+=distance(path[0],path[len(path)-1])
    return s 


#生成下一个状态
def neighbour3(path):
    leng=len(path)
    charge=random.random()
    if charge<0.334:#分成四段，交换中间两段
        a1,a2,a3=random.sample(range(1, leng-1), 3) 
        if a1>a2:
            a1,a2=a2,a1
        if a2>a3:
            a2,a3=a3,a2
        if a1>a2:
            a1,a2=a2,a1
        tmp=path[0:a1]+path[a2:a3]+path[a1:a2]+path[a3:leng]

    elif charge<0.666:#交换两个城市
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

    else:#分成三段，将中间逆序
        k1,k2=random.sample(range(1, leng-1), 2)
        if k1>k2:
            k1,k2=k2,k1
        tmp=path[0:k1]+path[k1:k2][::-1]+path[k2:leng]
    return tmp

def neighbour2(path):
    #print("nei",len(path))
    leng=len(path)
    a1,a2,a3=random.sample(range(1, leng-1), 3)
    if a1>a2:
        a1,a2=a2,a1
    if a2>a3:
        a2,a3=a3,a2
    if a1>a2:
        a1,a2=a2,a1
    tmp1=path[0:a1]+path[a2:a3]+path[a1:a2]+path[a3:leng]

    i=random.randint(1,leng-2)
    j=random.randint(2,leng-1)
    #print(i,"<->",j)
    #print(path)
    if i!=j:
        path[i],path[j]=path[j],path[i]
        tmp2=path[:]
        path[i],path[j]=path[j],path[i]
    else:
        tmp2=path[:]
    
    if random.random()>0.5:
        return tmp1
    else:
        return tmp2
    

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


dis_change=[]#记录路径变化的数组

ims=[]
fig1 = plt.figure(1)#用于生成动态图
ctt=0

tem=1000000#设置初始温度
while tem>0.0001:
    tem=0.98*tem#降温操作，每次乘0.98
    if tem==0:
        break

    for i in range(1000):   #稳定状态定为每个温度进行1000次
        next_node=neighbour3(curr)
   
        e_new=evaluate(next_node)
        e_now=evaluate(curr)
        dis_change.append(e_now)
        #接受更好状态
        if e_new<e_now :
            curr=next_node
        
        #以一定概率接受
        else :
            k=min(1,math.exp((e_now-e_new)/tem))
            if k>random.random():
                print(math.exp((e_now-e_new)/tem),e_now-e_new,tem)
                curr=next_node

    #每隔一段时间进行采样
    if ctt%100==0:
        x1=[]
        y1=[]
        for var in curr:
            x1.append(map_[var-1][1])
            y1.append(map_[var-1][2])
        x1.append(map_[0][1])
        y1.append(map_[0][2]) 
        im=plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
        ims.append(im)
    ctt+=1
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


#保存动态图
ani = animation.ArtistAnimation(fig1, ims, interval=200, repeat_delay=1000)
ani.save("SA.gif",writer='pillow')

fig3 = plt.figure(3)#用于显示总共费用的降低过程
plt.title('the evolution of the cost')
x_=[i for i in range(len(dis_change))]
plt.plot(x_,dis_change)
plt.show()
print("hh")