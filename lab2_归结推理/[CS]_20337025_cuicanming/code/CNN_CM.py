import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch
from matplotlib import pyplot as plt
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset

batch_size=128  #批大小设置为128
learn_rate=0.001    #学习率
my_transform = transforms.Compose([
        transforms.CenterCrop(128),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))  # 归一化
    ])

class MyDataset(Dataset):
    def __init__(self, txt_path, transform = None):
        fh = open(txt_path, 'r') #读制作好的txt文件的图片路径和标签到imgs里
        imgs = []
        for line in fh:
            line = line.rstrip()
            words = line.split('!')
            imgs.append((words[0], int(words[1])))
            self.imgs = imgs 
            self.transform = transform
    def __getitem__(self, index):
        fn, label = self.imgs[index] #self.imgs是一个list，self.imgs的一个元素是一个str，包含
        #图片路径，图片标签，这些信息是在init函数中从txt文件中读取的
        # fn是一个图片路径
        img = Image.open(fn).convert('RGB') #利用Image.open对图片进行读取，img类型为 Image ，mode=‘RGB’
        if self.transform is not None:
            img = self.transform(img) 
        return img, label
    def __len__(self):
        return len(self.imgs)

train_data = MyDataset('E://VSCODE/py/alltrain.txt',transform=my_transform)
test_data=MyDataset('E://VSCODE/py/alltest.txt',transform=my_transform)
train_loader = torch.utils.data.DataLoader(train_data,
						batch_size=batch_size,shuffle=True,num_workers=0,pin_memory=True)
test_loader = torch.utils.data.DataLoader(test_data,
						batch_size=batch_size,shuffle=False,num_workers=0,pin_memory=False)         




class cuixs_convNet(nn.Module):
    def __init__(self):
        super(cuixs_convNet,self).__init__()
        #卷积层
        self.features=nn.Sequential(
            
            nn.Conv2d(in_channels=3,out_channels=64,kernel_size=3,stride=1,padding=1),#卷积
            nn.BatchNorm2d(num_features=64), 
            #归一化处理         
            nn.ReLU(inplace=True),#激活函数
            nn.MaxPool2d(kernel_size=2,stride=2),#池化

            
            nn.Conv2d(64,128,3,1,1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2,2),
     

            
            nn.Conv2d(128,256,3,1,1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(4,4),
        )

        #分类层
        self.classify=nn.Sequential(
            #Dropout层,防止过拟合
            nn.Dropout(0.5),
            
            nn.Linear(256*8*8,256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),

            nn.Dropout(0.5),
            nn.Linear(256,256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),

            nn.Dropout(0.5),
            nn.Linear(256,5),
        )
    
    def forward(self,x):
        #特征提取
        x=self.features(x)
        #展平成一维向量
        x=x.flatten(1)
        
        x=self.classify(x)
        return x

def Train(epochs_num,_model,_device,_criterion,_optim,_exp_lr_scheduler,_trian_loader):
    _model.train()  #训练模式
    _exp_lr_scheduler.step()    #开始调度
    loss_set=[]
    #对训练集训练epochs_num次
    for epoch in range(epochs_num):
        for i,(img,label) in enumerate(_trian_loader):
            sample=img.to(device)
            label=label.to(device)
            #reshape得到的结果就是128张图片，每一张图片都是3通道的128 * 128，四维张量          
            sample=sample.reshape(-1,3,128,128)
            output=_model(sample)
            #损失函数
            loss=_criterion(output,label)
            #设置内部参数为0
            _optim.zero_grad()
            #向后传播
            loss.backward()
            #参数更新
            _optim.step()
            print()
            print("Epoch:{}/{}, step:{}, loss:{:.4f}".format(epoch + 1, epochs_num, i + 1, loss.item()))
            loss_set.append(loss.item())
    return loss_set

def Test(_test_loader,_model,_device,_criterion):
    _model.eval()#测试模式
    loss=0
    correct=0
    with torch.no_grad():
        for data,target in _test_loader:
            data=data.to(_device)
            target=target.to(_device)
            output=_model(data.reshape(-1,3,128,128))
            loss+=_criterion(output,target).item()
            pred=output.data.max(1,keepdim=True)[1]
            correct+=pred.eq(target.data.view_as(pred)).cpu().sum()
    loss /= len(_test_loader.dataset)
    print('\nAverage loss: {:.4f}, Accuracy: {}/{} ({:.3f}%)\n'.format(
        loss, correct, len(_test_loader.dataset),
        100. * correct / len(_test_loader.dataset)))


if __name__ == '__main__':
    #将网络操作移动到GPU或CPU
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model=cuixs_convNet().to(device)
    #交叉熵损失函数
    criterion=nn.CrossEntropyLoss().to(device)
    #定义模型优化器：输入模型参数，定义初始学习率
    optim=torch.optim.Adam(model.parameters(),lr=learn_rate)
    # 定义学习率调度器：输入包装的模型，定义学习率衰减周期step_size，gamma为衰减的乘法因子
    exp_lr_scheduler = lr_scheduler.StepLR(optim, step_size=6, gamma=0.1)
    #设置epoch次数
    epoch_num=2
    loss_set=Train(epoch_num,model,device,criterion,optim,exp_lr_scheduler,train_loader)
    index = [i for i in range(len(loss_set))]
    plt.plot(index,loss_set)
    plt.xlabel("Train times")
    plt.ylabel("Loss")
    plt.show()
    Test(test_loader,model,device,criterion)