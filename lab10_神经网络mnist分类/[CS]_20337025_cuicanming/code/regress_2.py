from cgi import test
from random import sample
from numpy.core.fromnumeric import size
import numpy as np
from matplotlib import pyplot as plt
from tqdm import trange
import csv
np.set_printoptions(suppress=True, threshold=np.inf)
# 解决坐标轴刻度负号乱码
plt.rcParams['axes.unicode_minus'] = False
# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['Simhei']
#迭代次数
iteration=500
#损失函数变化列表
loss_record=np.zeros((iteration,1))
learn_rate=0.02

def caculate_loss(hy,Y):
    n=len(Y)
    loss=np.sum(np.power(hy-Y,2))/(2*n)
    return loss

def Train(X,Y,w):
    #lenth=len(w)
    N=len(Y)
    #迭代
    for i in trange(iteration):
        hy=np.dot(X,w)
        #根据公式梯度下降
        w=w-(learn_rate/N)*(np.dot(np.transpose(X),hy-Y))
        loss_record[i]=caculate_loss(hy,Y)
    final_w=w
    return final_w




path='D://regress/regress_data2.csv'
csv_reader=csv.reader(open(path,encoding='utf-8'))
train_data=[]
test_data=[]
cnt=0
for row in csv_reader:
    cnt+=1
    for i in range(len(row)):
        row[i]=float(row[i])
    train_data.append(np.array(row))
    if cnt>35:
        test_data.append(np.array(row))
train_data=np.array(train_data)
test_data=np.array(test_data)

X=np.array(train_data[:,0:2])   # X取前两列的数据
Y=np.array(train_data[:,2])
Y=Y.reshape(-1,1)

#归一化的过程
aver_of_x=np.mean(X,0)
std_of_x=np.std(X,0)
#print(len(X))
for i in range(len(X[0])):
    X[:,i]=(X[:,i]-aver_of_x[i])/std_of_x[i]

#设x0为1，则在数组前面插入一列47*1的全为1的列向量
X=np.hstack((np.ones((len(X),1)),X))

num_of_w=len(X[0])
#print(num_of_w)
#参数矩阵3*1
w=np.zeros((num_of_w,1))

last_w=Train(X,Y,w)

fig1=plt.figure(1)
#绘loss变化图-----------------------------------------
plt.plot(np.arange(iteration),loss_record)
plt.xlabel("num of iteration")
plt.ylabel("value of loss")
plt.title("Loss函数变化图")

#绘制函数图像-----------------------------------------

plt.figure(figsize=(5,5))
x=X[:,1]
y=X[:,2]
    
temp=last_w.flatten()
temp=temp.reshape(1,3)

z=temp[0,0]+(temp[0,1]*x)+(temp[0,2]*y)

ax=plt.subplot(111,projection='3d')
ax.plot_trisurf(x,y,z)
ax.scatter(X[:,1],X[:,2],Y,label='真实值')

ax.set_xlabel('房屋大小')
ax.set_ylabel('房间数')
ax.set_zlabel('价格')
plt.show()
#----------------------------------------------------

#预测
test_X=np.array(X[37:47])   # X取前两列的数据
test_Y=np.array(Y[37:47])
pre=np.dot(test_X,last_w)
for i in range(len(pre)):
    print("real:",test_Y[i],"predict:",pre[i])

