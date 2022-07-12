import torch
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import DataLoader as DataLoader
from torchvision import datasets
from torch.optim import lr_scheduler
from matplotlib import pyplot as plt


#下载mnist数据集
mnist_train = datasets.MNIST('mnist', train=True, transform=transforms.Compose([
    transforms.ToTensor()
]), download=True)
mnist_train = DataLoader(mnist_train, batch_size=32, shuffle=True)
 
 
mnist_test = datasets.MNIST('mnist', train=False, transform=transforms.Compose([
    transforms.ToTensor()
]), download=True)
mnist_test = DataLoader(mnist_test, batch_size=32)


#自编码器的网络结构
class AE(nn.Module):
    def __init__(self):
        super(AE, self).__init__()
        #编码器的网络结构
        self.encoder = nn.Sequential(
            # [b, 784] => [b, 256]
            nn.Linear(784, 256),
            nn.ReLU(),
            # [b, 256] => [b, 64]
            nn.Linear(256, 64),
            nn.ReLU(),
            # [b, 64] => [b, 20]
            nn.Linear(64, 20),
            nn.ReLU()
        )
        #译码器的网络结构
        self.decoder = nn.Sequential(
            # [b, 20] => [b, 64]
            nn.Linear(20, 64),
            nn.ReLU(),
            # [b, 64] => [b, 256]
            nn.Linear(64, 256),
            nn.ReLU(),
            # [b, 256] => [b, 784]
            nn.Linear(256, 784),
            nn.Sigmoid()
        )
 
 
    def forward(self, x):
        batchsz = x.size(0)
        #展平
        x = x.view(batchsz, -1)
        #编码
        x = self.encoder(x)
        #译码
        x = self.decoder(x)
        #将其恢复原来的格式
        x = x.view(batchsz, 1, 28, 28)
        return x

#训练过程
def Train(epochs_num,_model,_criterion,_optim,_exp_lr_scheduler,_trian_loader):
    _model.train()
    _exp_lr_scheduler.step()
    loss_set=[]
    for ep in range(epochs_num):
        for i,(img,label) in enumerate(_trian_loader):
            output=_model(img)
            loss=_criterion(output,img)

            _optim.zero_grad()
            #反向传播
            loss.backward()
            _optim.step()
            print("Epoch:{}/{}, step:{}, loss:{:.4f}".format(ep + 1, epochs_num, i + 1, loss.item()))
            loss_set.append(loss.item())
    return loss_set

#测试过程
def Test():
    model.eval()
    N=4
    M=8
    #迭代器
    dataiter = iter(mnist_test)
    images, labels = dataiter.next()
    with torch.no_grad():
        _images = model(images)
    p1=plt.figure(1)
    for i in range(32):
        plt.subplot(N,M,i+1)#表示第i张图片，下标只能从1开始，不能从0
        plt.imshow(images[i].numpy().squeeze(), cmap='gray_r')
        plt.xticks([])
        plt.yticks([])
    p2=plt.figure(2)
    for i in range(32):
        plt.subplot(N,M,i+1)#表示第i张图片，下标只能从1开始，不能从0
        plt.imshow(_images[i].numpy().squeeze(), cmap='gray_r')
        plt.xticks([])
        plt.yticks([])
    plt.show()

#每个数字选10个进行测试和进行与原图片的对比
#通过修改num的值来选择数字
num=6
def Test2():
    model.eval()
    N=3
    M=4
    dataiter = iter(mnist_test)
    images, labels = dataiter.next()
    with torch.no_grad():
        _images = model(images)
    p1=plt.figure(1)
    cnt=0
    while 1:
        for i in range(32):
            if labels[i]==num:
                plt.subplot(N,M,cnt+1)
                plt.imshow(images[i].numpy().squeeze(), cmap='gray_r')
                plt.xticks([])
                plt.yticks([])
                cnt+=1
            if cnt==10:
                break
        
        if cnt==10:
            break
        else:
            images, labels = dataiter.next()

    dataiter = iter(mnist_test)
    images, labels = dataiter.next()
    with torch.no_grad():
        _images = model(images)
    p2=plt.figure(2)
    cnt=0
    while 1:
        for i in range(32):
            if labels[i]==num:
                plt.subplot(N,M,cnt+1)
                plt.imshow(_images[i].numpy().squeeze(), cmap='gray_r')
                plt.xticks([])
                plt.yticks([])
                cnt+=1
            if cnt==10:
                break
        
        if cnt==10:
            break
        else:
            images, labels = dataiter.next()
            with torch.no_grad():
                _images = model(images)

    plt.show()

if __name__=='__main__':
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model=AE().to(device)
    epochs_num=2

    #损失函数
    criterion=nn.MSELoss()
    #学习率
    learn_rate=1e-3
    optim=torch.optim.Adam(model.parameters(),lr=learn_rate)

   
    # 定义学习率调度器：输入包装的模型，定义学习率衰减周期step_size，gamma为衰减的乘法因子
    exp_lr_scheduler = lr_scheduler.StepLR(optim, step_size=6, gamma=0.1)
    #进行训练，返回损失函数的变化过程
    loss_set=Train(epochs_num,model,criterion,optim,exp_lr_scheduler,mnist_train)
    index = [i for i in range(len(loss_set))]
    fig1 = plt.figure(1)
    plt.plot(index,loss_set)
    plt.xlabel("Train times")
    plt.ylabel("Loss")
    plt.show()

    Test2()