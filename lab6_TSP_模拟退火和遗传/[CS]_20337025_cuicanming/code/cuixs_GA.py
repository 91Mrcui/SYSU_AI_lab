from cmath import exp
import sys
import matplotlib.pyplot as plt 
import random
import math
import matplotlib.animation as animation
from scipy import rand

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
    
f1=plt.figure(1)
plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
plt.show()

def distance(a,b):
    s=pow(map_[a-1][1]-map_[b-1][1],2)+pow(map_[a-1][2]-map_[b-1][2],2)
    return math.sqrt(s)

def evaluate(path):
    s=0
    for i in range (1,len(path)):
       s+=distance(path[i-1],path[i])
    #s+=distance(1,path[len(path)-1])
    return s 

#交叉产生下一代
def reproduce_ox(p1,p2):
    length=len(p1)
    sta,end=random.sample(range(1, length), 2)
    if end<sta:
        sta,end=end,sta
    child=p1[sta:end]
    c1=[]
    c2=[]
    for i in range(0,length):
        if p2[i] not in child:
            if i<sta:
                c1.append(p2[i])
            else:
                c2.append(p2[i])
    child=c1+child+c2
    return child
    
#变异函数
def neighbour3(path):
    leng=len(path)
    charge=random.random()
    if charge<0.4:
        a1,a2,a3=random.sample(range(1, leng-1), 3) 
        if a1>a2:
            a1,a2=a2,a1
        if a2>a3:
            a2,a3=a3,a2
        if a1>a2:
            a1,a2=a2,a1
        tmp=path[0:a1]+path[a2:a3]+path[a1:a2]+path[a3:leng]
    elif charge<0.6:
        i=random.randint(1,leng-2)
        j=random.randint(2,leng-1)
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
        #print(len(tmp))
    return tmp

#贪心算法生成初始种群
def greed(vist,gcur):
    max=9999999
    flag=-1
    for i in range(len(gcur)):
        if gcur[i] not in vist:
            for j in range(len(vist)):
                tmp=distance(vist[j],gcur[i])
                if tmp<max:
                    max=tmp
                    flag=i
    return flag

population=[]
leng=len(map_)
mutate=0.3#变异概率
#随机生成一半
for i in range(10):
    curr=random.sample(range(1, leng+1), leng)
    population.append(curr)
tool=population[1][:]
#贪心生成另外一半
for i in range(10):
    sta_city=random.randint(1,leng-1)
    vist=[]
    vist.append(sta_city)
    while len(vist)<leng:
        index=greed(vist,tool)
        vist.append(tool[index])
    population.append(vist)
for var in population:
    print(evaluate(var))
print("----------------------------------------")
ims=[]
fig1 = plt.figure(1)#用于生成动态图
dis_change=[]
iteration=0
#迭代的过程
while iteration<10000:
    new_population=[]#新种群
    for count in range(0,10):
        plen=len(population)     
        the_weight=[]#代表权重的数组
        for cnt in range(0,len(population)):
            the_weight.append(1000000/evaluate(population[cnt]))#距离总和越小权重越大

        #轮盘赌选择亲代
        ch1=random.choices(population,the_weight,k=1)
        ch2=random.choices(population,the_weight,k=1)
        #杂交出两个子代
        child1=reproduce_ox(ch1[0],ch2[0])
        child2=reproduce_ox(ch2[0],ch1[0])
        #有一定概率变异
        if random.random()<mutate :
            child1==neighbour3(child1)
            child2==neighbour3(child2)
        #为了防止子代全部都一样，当杂交两者相等时进行变异
        if child1==child2:
            child1=neighbour3(child1)
            child2=neighbour3(child2)
        #并入新种群
        new_population.append(child1)
        new_population.append(child2)
    flag=-1
    max=9999999
    #选取最优良的个体保存到下一代
    for i2 in range(0,len(population)):
        if evaluate(population[i2])<max:
            max=evaluate(population[i2])
            flag=i2
    temp_one=population[flag][:]
    #显示当前迭代次数和最优值
    print(iteration, evaluate(temp_one))
    dis_change.append(max)
    population.clear()
    #更新
    population=new_population[0:19]
    new_population.clear()
    population.append(temp_one)
    iteration+=1
    #每隔一段时间进行采样
    if iteration%10==0:
        x1=[]
        y1=[]
        for var in temp_one:
            x1.append(map_[var-1][1])
            y1.append(map_[var-1][2])
        x1.append(map_[0][1])
        y1.append(map_[0][2]) 
        im=plt.plot(x1, y1, marker = '.', color = 'red',linewidth=1) 
        ims.append(im)

#结束
print("loop end")
flag=-1
max=9999999
for i in range(0,len(population)):
    if evaluate(population[i])<max:
        min=evaluate(population[i])
        flag=i

curr=population[flag]
xo=[]
yo=[]
for var in curr:
    xo.append(map_[var-1][1])
    yo.append(map_[var-1][2])
print(evaluate(curr))
fig2 = plt.figure(2)#用于显示最终的解
plt.plot(xo, yo, marker = '.', color = 'red',linewidth=1) 
#保存动态图
ani = animation.ArtistAnimation(fig1, ims, interval=200, repeat_delay=1000)
ani.save("GA.gif",writer='pillow')
fig3 = plt.figure(3)#用于显示总共费用的降低过程
plt.title('the evolution of the cost')
x_=[i for i in range(len(dis_change))]
plt.plot(x_,dis_change)
plt.show()
print("hh")