import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from collections import OrderedDict
import os
import matplotlib.pyplot as plt

#17 stop
#33 turn right
#34 turn left
#35 go straight

if __name__=='__main__':
    data_transform=transforms.Compose([
        transforms.Resize((32,32)),
        transforms.ToTensor(),
    ])

    img=datasets.ImageFolder('D:\EEEEEEEEEEEEEEEEEEEEEEEEEEEEE\Dataset\\train\Dataset\image',transform=data_transform)
    imgLoader=torch.utils.data.DataLoader(img,batch_size=1,shuffle=True,num_workers=1)
    train_X,train_y,test_X,test_y=[],[],[],[]
    cnt=0
    for X,y in imgLoader:
        cnt+=1
        if (cnt<=65):
            train_X.append(X.numpy())
            train_y.append(y.numpy())
        test_X.append(X.numpy())
        test_y.append(y.numpy())
    print(cnt)
    train_X=np.concatenate(train_X,axis=0)
    train_y=np.concatenate(train_y,axis=0)
    test_X=np.concatenate(test_X,axis=0)
    test_y=np.concatenate(test_y,axis=0)
    train_X=train_X.reshape(train_X.shape[0],3*32*32)
    test_X=test_X.reshape(test_X.shape[0],3*32*32)
    from sklearn.preprocessing import StandardScaler
    ss=StandardScaler()
    train_X=ss.fit_transform(train_X)
    test_X=ss.transform(test_X)
    import joblib
    joblib.dump(ss, os.path.dirname(os.path.realpath(__file__))+'\\scalar01')
    print(train_X.shape[0],test_X.shape[0])
    train_X=train_X.reshape(train_X.shape[0],1,3,32,32)
    test_X=test_X.reshape(test_X.shape[0],1,3,32,32)
    train_X=torch.from_numpy(train_X)
    test_X=torch.from_numpy(test_X)
    train_y=train_y.reshape(train_y.shape[0],1)
    test_y=test_y.reshape(test_y.shape[0],1)
    train_y=torch.from_numpy(train_y)
    test_y=torch.from_numpy(test_y)

    class Net(nn.Module):
        def __init__(self):
            super(Net,self).__init__()
            self.convnet=nn.Sequential(OrderedDict([
                ('c1',nn.Conv2d(3,10,kernel_size=(5,5))),
                ('relu1',nn.ReLU()),
                ('s2',nn.MaxPool2d(kernel_size=(2,2),stride=2)),
                ('c3',nn.Conv2d(10,30, kernel_size=(5,5))),
                ('relu3',nn.ReLU()),
                ('s4',nn.MaxPool2d(kernel_size=(2,2),stride=2)),
                ('c5',nn.Conv2d(30,120,kernel_size=(5,5))),
                ('relu5',nn.ReLU())
            ]))
            self.fc = nn.Sequential(OrderedDict([
                ('f6',nn.Linear(120,84)),
                ('relu6',nn.ReLU()),
                ('f7',nn.Linear(84,10)),
                ('sig7',nn.LogSoftmax(dim=-1))
            ]))

        def forward(self,img):
            output=self.convnet(img)
            output=output.view(img.size(0),-1)
            output=self.fc(output)
            return output

    net=Net()
    criterion=nn.CrossEntropyLoss()
    optimizer=optim.Adam(net.parameters(),lr=1e-3)

    def train(epoch):
        net.train()
        for i in range(train_X.shape[0]):
            optimizer.zero_grad()
            X=torch.tensor(train_X[i],dtype=torch.float32)
            pred=net(X)
            y=torch.tensor(train_y[i],dtype=torch.int64)
            loss=criterion(pred,y)
            loss.backward()
            optimizer.step()

    def validate():
        net.eval()
        acc=0.0
        avg_loss=0.0
        for i in range(test_X.shape[0]):
            X=torch.tensor(test_X[i],dtype=torch.float32)
            pred=net(X)
            y=torch.tensor(test_y[i],dtype=torch.int64)
            avg_loss+=criterion(pred,y).sum()
            predicted=pred.detach().max(1)[1]
            acc+=predicted.eq(test_y[i].view_as(predicted)).sum()
        avg_loss/=(test_X.shape[0])
        acc/=(test_X.shape[0])
        print('Validation - Average loss: %f, Accuracy: %f'%(avg_loss,acc))
        if (acc==1):
            return 1
        else:
            return 0

    for epoch in range(100):
        train(epoch)
        if (validate()):
            break
    
    file=os.path.dirname(os.path.realpath(__file__))+'\\model.pt'
    print(net)
    print(file)
    torch.save(net,file)