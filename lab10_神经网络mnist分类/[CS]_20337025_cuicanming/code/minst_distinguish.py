from cgi import test
from random import sample
from numpy.core.fromnumeric import size
import numpy as np
import struct
import sys
import os
import math
import torch
from matplotlib import pyplot as plt
from tqdm import trange

def decode_idx3_ubyte(file):
    """
    解析数据文件
    """
    # 读取二进制数据
    with open(file, 'rb') as fp:
        bin_data = fp.read()
    
    # 解析文件中的头信息
    # 从文件头部依次读取四个32位，分别为：
    # magic，numImgs, numRows, numCols
    # 偏置
    offset = 0
    # 读取格式: 大端
    fmt_header = '>iiii'
    magic, numImgs, numRows, numCols = struct.unpack_from(fmt_header, bin_data, offset)
    print(magic,numImgs,numRows,numCols)
    
    # 解析图片数据
    # 偏置掉头文件信息
    offset = struct.calcsize(fmt_header)
    # 读取格式
    fmt_image = '>'+str(numImgs*numRows*numCols)+'B'
    data = torch.tensor(struct.unpack_from(fmt_image, bin_data, offset)).reshape(numImgs, numRows, numCols)
    return data


def decode_idx1_ubyte(file):
    """
    解析标签文件
    """
    # 读取二进制数据
    with open(file, 'rb') as fp:
        bin_data = fp.read()
    
    # 解析文件中的头信息
    # 从文件头部依次读取两个个32位，分别为：
    # magic，numImgs
    # 偏置
    offset = 0
    # 读取格式: 大端
    fmt_header = '>ii'
    magic, numImgs = struct.unpack_from(fmt_header, bin_data, offset)
    print(magic,numImgs)
    
    # 解析图片数据
    # 偏置掉头文件信息
    offset = struct.calcsize(fmt_header)
    # 读取格式
    fmt_image = '>'+str(numImgs)+'B'
    data = torch.tensor(struct.unpack_from(fmt_image, bin_data, offset))
    return data


#print(type(train_set[0]))

#激活函数
def active(x):
    y=[]
    for i in range(len(x)):
        y.append(1/(1+math.exp(-x[i])))
    y=np.array(y)
    return y

def Test(w,v,offset1,offset2,test_label,test_data):
    correct=0
    for i in trange(len(test_data)):
        hv=np.dot(test_data[i],w)+offset1
        hv_a=active(hv)
        ov=np.dot(hv_a,v)+offset2
        ov_a=active(ov)
        #print("real: ",test_label[i]," predict: ",np.argmax(ov_a))
        if test_label[i]==np.argmax(ov_a):
            correct+=1
    print("Rate: ",correct/len(test_data))

# 文件路径
data_path = r'D:\minst'
file_names = ['t10k-images.idx3-ubyte',
              't10k-labels.idx1-ubyte',
              'train-images.idx3-ubyte',
              'train-labels.idx1-ubyte']

train_set = (decode_idx3_ubyte(os.path.join(data_path, file_names[0])),
             decode_idx1_ubyte(os.path.join(data_path, file_names[1])))
test_set = (decode_idx3_ubyte(os.path.join(data_path, file_names[2])),
            decode_idx1_ubyte(os.path.join(data_path, file_names[3])))

train_data=[]
train_label=train_set[1]
test_data=[]
test_label=test_set[1]

for i in range(len(train_set[0])):
    train_data.append(train_set[0][i].reshape(784,))
    test_data.append(test_set[0][i].reshape(784,))

for i in range(len(train_set[0])):
    train_data[i]=train_data[i].cpu().numpy() 
    test_data[i]=test_data[i].cpu().numpy()
    train_data[i]=train_data[i]/160.0
    test_data[i]= test_data[i]/160.0

train_data=np.array(train_data)
test_data=np.array(test_data)

sample_num=len(train_data)
input_num=size(train_data[0])
output_num=10
hidden=60

# 初始化输入层与隐层之间的连接权值矩阵为一个(inputNum*hiddenNum)维的随机矩阵
w = 0.2 * np.random.random((input_num, hidden)) - 0.1
# 初始化隐层与输出层之间的连接权值矩阵为一个(hiddenNum*outputNum)维的随机矩阵
v = 0.2 * np.random.random((hidden, output_num))- 0.1

#偏置向量
offset1=np.zeros(hidden)
offset2=np.zeros(output_num)

#设置学习率
input_learn_rate=0.2
output_learn_rate=0.2

loss=[]

#def Train():
print("Training......................................")
for cnt in trange(len(train_data)):
    #正确的结果
    real_labels=np.zeros(output_num)

    real_labels[train_label[cnt]]=1

    #计算第一层
    hidden_value=np.dot(train_data[cnt],w)+ offset1
    #第一层输出
    hidden_result=active(hidden_value)

    #输出层
    out_value=np.dot(hidden_result,v)+ offset2
    out_result=active(out_value)


    #计算误差的导数
    E=real_labels - out_result
    if cnt%100==0:
        loss.append(abs(np.mean(E)))
    #输出对输入求导--激励函数的导数
    delta_output=E*out_result*(1-out_result)#输出层

    

    delta_hidden=hidden_result*(1-hidden_result)* np.dot(v,delta_output)#隐藏层

    #权重更新
    for i in range(output_num):
        v[:,i]+=output_learn_rate*delta_output[i]*hidden_result
    for i in range(hidden):
        w[:,i]+=input_learn_rate*delta_hidden[i]*train_data[cnt]


    offset2 += output_learn_rate*delta_output
    offset1 += input_learn_rate*delta_hidden

#def Test():
print("Testing.......................................")
Test(w,v,offset1,offset2,test_label,test_data)

s_x = [i for i in range(len(loss))]


plt.plot(s_x,loss)
plt.show()
