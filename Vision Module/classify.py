import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from collections import OrderedDict
import os

if __name__=='__main__':
    data_transform=transforms.Compose([
        transforms.Resize((32,32)),
        transforms.ToTensor(),
    ])

    img=datasets.ImageFolder(os.path.dirname(os.path.realpath(__file__)),transform=data_transform)
    imgLoader=torch.utils.data.DataLoader(img,batch_size=1,shuffle=False,num_workers=1)
    test_X=[]
    for X,y in imgLoader:
        test_X.append(X.numpy())
    test_X=np.concatenate(test_X,axis=0)
    test_X=test_X.reshape(test_X.shape[0],3*32*32)
    import joblib
    from sklearn.preprocessing import StandardScaler
    ss=joblib.load(os.path.dirname(os.path.realpath(__file__))+'\\scalar01')
    test_X=ss.transform(test_X)
    test_X=test_X.reshape(test_X.shape[0],1,3,32,32)
    test_X=torch.from_numpy(test_X)
    
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

    file=os.path.dirname(os.path.realpath(__file__))+'\\model.pt'
    net=torch.load(file)
    criterion=nn.CrossEntropyLoss()

    def predict():
        net.eval()
        for i in range(test_X.shape[0]):
            X=torch.tensor(test_X[i],dtype=torch.float32)
            pred=net(X)
            predicted=pred.detach().max(1)[1]
            print(predicted.item())

    predict()