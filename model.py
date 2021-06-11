# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dBi99eYOiPuCZH14jbkfD1jGjNMy5JC4
"""

from google.colab import drive

drive.mount('/gdrive')

# Specify the directory path where `assignemnt3.ipynb` exists.
# For example, if you saved `assignment3.ipynb` in `/gdrive/My Drive/cs376/assignment3` directory,
# then set root = '/gdrive/My Drive/cs376/assignment3'
gdrive_root = '/gdrive/My Drive/Colab_Notebooks/new_efficiency_1'

import os
import shutil

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision
from torchvision import transforms

# !pip install -U tensorboardcolab
# from tensorboardcolab import TensorBoardColab

torch.manual_seed(470)
torch.cuda.manual_seed(470)

# training & optimization hyper-parameters
max_epoch = 70
learning_rate = 0.001
batch_size = 64
device = 'cuda'

# model hyper-parameters
output_dim = 16

# Boolean value to select training process
training_process = True

# ######### split into test and train folder ############
# 1번 했으니 안해도 됨




# import random
# #brands = ['1_Hermes']
# #'1_Hermes', '2_SaintLaurent', '4_Lemaire', '5_CommeDesGarcons', '6_OffWhite', '8_Dior', '9_Gucci', '10_Burberry', '11_Prada', '13_ThomBrowne', '14_A.P.C', 
# brands = ['1_Hermes', '2_SaintLaurent', '4_Lemaire', '5_CommeDesGarcons', '6_OffWhite', '8_Dior', '9_Gucci', '10_Burberry', '11_Prada', '13_ThomBrowne', '14_A.P.C', '15_AlexanderMcqueen', '16_Balenciaga', '17_Chanel', '18_LouisVuitton', '19_MiuMiu']
# for brand in brands:
#     image_folder = "/gdrive/My Drive/ee474_dataset/0_Dataset/" + brand
#     train_folder = "/gdrive/My Drive/ee474_dataset/0_Dataset/train/" + brand
#     test_folder = "/gdrive/My Drive/ee474_dataset/0_Dataset/test/" + brand
#     if not os.path.exists(train_folder):
#         os.makedirs(train_folder)
#     if not os.path.exists(test_folder):
#         os.makedirs(test_folder)
#     image_files = [_ for _ in os.listdir(image_folder) if _.endswith('jpg')]
#     random.shuffle(image_files)
#     for image in image_files[:int(len(image_files)*0.8)]:
#         image_path = os.path.join(image_folder, image)
#         newpath = image_path.replace(brand, 'train/' + brand)
#         shutil.move(image_path, newpath)
#     for image in image_files[int(len(image_files)*0.8):]:
#         image_path = os.path.join(image_folder, image)
#         newpath = image_path.replace(brand, 'test/' + brand)
#         shutil.move(image_path, newpath)

########## dataload ###########

data_dir = "/gdrive/My Drive/ee474_dataset/0_Dataset/"

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.480, 0.437, 0.425), (0.257, 0.247, 0.245))])

train_dir = data_dir + 'train'
test_dir = data_dir + 'test'

train_data = torchvision.datasets.ImageFolder(root=train_dir, transform=transform)
test_data = torchvision.datasets.ImageFolder(root=test_dir, transform=transform)

train_dataloader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=2)
test_dataloader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=2)

print(train_data.class_to_idx)

classes = ('Burberry', 'Prada', 'Thom Browne', 'A.P.C', 'Alexander Mcqueen', 'Balenciaga', 'Chanel', 'Louis Vuitton', 'Miu Miu', 'Hermes', 'Saint Laurent', 'Lemaire', 'Comme Des Garcons', 'Off White', 'Dior', 'Gucci')

# data_dir = os.path.join(gdrive_root, 'my_data')

# transform = transforms.Compose(
#     [transforms.ToTensor(),
#      transforms.Normalize((0.4914, 0.4822, 0.4465), (0.247, 0.243, 0.261))])

# train_dataset = torchvision.datasets.CIFAR10(root=data_dir, train=True, download=True, transform=transform)
# train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)

# test_dataset = torchvision.datasets.CIFAR10(root=data_dir, train=False, download=True, transform=transform)
# test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

# classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# # Let's build your own model. 



# class Node(nn.Module):
#   def __init__(self, channel_in, channel_out, st):
#     super(Node, self).__init__()
#     self.CV1 = nn.Conv2d(channel_in, channel_out, kernel_size = 3, stride = st, padding = 1, bias = False)
#     self.CV2 = nn.Conv2d(channel_out, channel_out, kernel_size = 3, stride = 1, padding = 1, bias = False)
#     self.chno = channel_out
#     self.St = st
#     self.chin = channel_in
#     self.B2d1 = nn.BatchNorm2d(channel_out)
#     self.B2d2 = nn.BatchNorm2d(channel_out)
#     self.add = nn.Sequential()
    
    
#     self.CV3 = nn.Conv2d(self.chin, channel_out, kernel_size = 1, stride = self.St, bias = False)
#     self.B2d3 = nn.BatchNorm2d(channel_out)
    
  
#   def forward(self, x):
#     o = self.CV1(x)
#     o = self.B2d1(o)
#     o = F.relu(o)
#     o = self.CV2(o)
#     o = self.B2d2(o)
#     k = x
#     if self.St != 1 or self.chno != self.chin:
#       k = self.CV3(x)
#       k = self.B2d3(k)
#     o += k
#     o = F.relu(o)
#     return o

# class RootNode(nn.Module):
#   def __init__(self, channel_in, channel_out, ks):
#     super(RootNode, self).__init__()
#     self.CV = nn.Conv2d(channel_in, channel_out, kernel_size=1, stride=1, padding=(ks-1) // 2, bias=False)
#     self.chno = channel_out
#     self.B2d = nn.BatchNorm2d(self.chno)
  
#   def forward(self, x):
#     x = torch.cat(x, 1)
#     x = self.CV(x)
#     x = self.B2d(x)
#     x = F.relu(x)
#     return x

# class TreeNode(nn.Module):
#   def __init__(self, node, channel_in, channel_out, level, st):
#     super(TreeNode, self).__init__()
#     if level == 1:
#       self.L = node(channel_in, channel_out, st)
#       self.R = node(channel_out, channel_out, 1)
#     else:
#       self.L = TreeNode(node, channel_in, channel_out, level-1, st)
#       self.R = TreeNode(node, channel_out, channel_out, level-1, 1)
#     self.root = RootNode(2*channel_out, channel_out, 1)
    
#   def forward(self, x):
#     o1 = self.L(x)
#     o2 = self.R(o1)
#     x = self.root([o1, o2])
#     return x

# class MyOwnClassifier(nn.Module):
#     def __init__(self):
#         super(MyOwnClassifier, self).__init__()
#         # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#         self.CV1 = nn.Conv2d(3, 32, kernel_size=7, stride=2, padding=3, bias=False)
#         self.B1 = nn.BatchNorm2d(32)
#         self.R1 = nn.ReLU(inplace = True)
#         self.D1 = nn.Dropout(p=0.3)
#         self.P1 = nn.MaxPool2d(3, stride=2)

#         #self.CV2 = nn.Conv2d(16, 16, kernel_size=3, stride=1, padding=1, bias=False)
#         #self.B2 = nn.BatchNorm2d(16)
#         #self.R2 = nn.ReLU(inplace = True)
        

#         #self.CV3 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1, bias=False)
#         #self.B3 = nn.BatchNorm2d(32)
#         #self.R3 = nn.ReLU(inplace = True)
        

#         self.Tree4 = TreeNode(Node, 32, 64, 1, 1)
#         self.D2 = nn.Dropout(p=0.3)
#         self.Tree5 = TreeNode(Node, 64, 128, 2, 2)
#         self.D3 = nn.Dropout(p=0.3)
#         self.Tree6 = TreeNode(Node, 128, 256, 4, 2)
#         self.D4 = nn.Dropout(p=0.3)
#         self.Tree7 = TreeNode(Node, 256, 512, 2, 2)
#         self.D5 = nn.Dropout(p=0.3)
#         self.Tree8 = TreeNode(Node, 512, 1024, 2, 2)
#         self.D6 = nn.Dropout(p=0.3)

#         self.Lin = nn.Linear(1024, output_dim)

#         # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*******        
#     def forward(self, x):
#         # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
#         x = self.CV1(x)
#         x = self.B1(x)
#         x = self.R1(x)
#         x = self.D1(x)
#         x = self.P1(x)
        
#         #x = self.CV2(x)
#         #x = self.B2(x)
#         #x = self.R2(x)

#         #x = self.CV3(x)
#         #x = self.B3(x)
#         #x = self.R3(x)
        

#         x = self.Tree4(x)
#         x = self.D2(x)
#         x = self.Tree5(x)
#         x = self.D3(x)
#         x = self.Tree6(x)
#         x = self.D4(x)
#         x = self.Tree7(x)
#         x = self.D5(x)
#         x = self.Tree8(x)
#         x = self.D6(x)

#         x = F.avg_pool2d(x, x.size()[2:])
#         x = self.Lin(x.view(x.size(0), -1))

#         # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*******        
#         return x

def swish(x):
    return x * x.sigmoid()


def drop_connect(x, drop_ratio):
    keep_ratio = 1.0 - drop_ratio
    mask = torch.empty([x.shape[0], 1, 1, 1], dtype=x.dtype, device=x.device)
    mask.bernoulli_(keep_ratio)
    x.div_(keep_ratio)
    x.mul_(mask)
    return x


class SE(nn.Module):
    '''Squeeze-and-Excitation block with Swish.'''

    def __init__(self, in_channels, se_channels):
        super(SE, self).__init__()
        self.se1 = nn.Conv2d(in_channels, se_channels,
                             kernel_size=1, bias=True)
        self.se2 = nn.Conv2d(se_channels, in_channels,
                             kernel_size=1, bias=True)

    def forward(self, x):
        out = F.adaptive_avg_pool2d(x, (1, 1))
        out = swish(self.se1(out))
        out = self.se2(out).sigmoid()
        out = x * out
        return out


class Block(nn.Module):
    '''expansion + depthwise + pointwise + squeeze-excitation'''

    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size,
                 stride,
                 expand_ratio=1,
                 se_ratio=0.,
                 drop_rate=0.):
        super(Block, self).__init__()
        self.stride = stride
        self.drop_rate = drop_rate
        self.expand_ratio = expand_ratio

        # Expansion
        channels = expand_ratio * in_channels
        self.conv1 = nn.Conv2d(in_channels,
                               channels,
                               kernel_size=1,
                               stride=1,
                               padding=0,
                               bias=False)
        self.bn1 = nn.BatchNorm2d(channels)

        # Depthwise conv
        self.conv2 = nn.Conv2d(channels,
                               channels,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=(1 if kernel_size == 3 else 2),
                               groups=channels,
                               bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

        # SE layers
        se_channels = int(in_channels * se_ratio)
        self.se = SE(channels, se_channels)

        # Output
        self.conv3 = nn.Conv2d(channels,
                               out_channels,
                               kernel_size=1,
                               stride=1,
                               padding=0,
                               bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)

        # Skip connection if in and out shapes are the same (MV-V2 style)
        self.has_skip = (stride == 1) and (in_channels == out_channels)

    def forward(self, x):
        out = x if self.expand_ratio == 1 else swish(self.bn1(self.conv1(x)))
        out = swish(self.bn2(self.conv2(out)))
        out = self.se(out)
        out = self.bn3(self.conv3(out))
        if self.has_skip:
            if self.training and self.drop_rate > 0:
                out = drop_connect(out, self.drop_rate)
            out = out + x
        return out


class EfficientNet(nn.Module):
    def __init__(self, cfg, num_classes=16):
        super(EfficientNet, self).__init__()
        self.cfg = cfg
        self.conv1 = nn.Conv2d(3,
                               32,
                               kernel_size=3,
                               stride=1,
                               padding=1,
                               bias=False)
        self.bn1 = nn.BatchNorm2d(32)
        self.layers = self._make_layers(in_channels=32)
        self.linear = nn.Linear(cfg['out_channels'][-1], num_classes)

    def _make_layers(self, in_channels):
        layers = []
        cfg = [self.cfg[k] for k in ['expansion', 'out_channels', 'num_blocks', 'kernel_size',
                                     'stride']]
        b = 0
        blocks = sum(self.cfg['num_blocks'])
        for expansion, out_channels, num_blocks, kernel_size, stride in zip(*cfg):
            strides = [stride] + [1] * (num_blocks - 1)
            for stride in strides:
                drop_rate = self.cfg['drop_connect_rate'] * b / blocks
                layers.append(
                    Block(in_channels,
                          out_channels,
                          kernel_size,
                          stride,
                          expansion,
                          se_ratio=0.25,
                          drop_rate=drop_rate))
                in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        out = swish(self.bn1(self.conv1(x)))
        out = self.layers(out)
        out = F.adaptive_avg_pool2d(out, 1)
        out = out.view(out.size(0), -1)
        dropout_rate = self.cfg['dropout_rate']
        if self.training and dropout_rate > 0:
            out = F.dropout(out, p=dropout_rate)
        out = self.linear(out)
        return out


def EfficientNetB0():
    cfg = {
        'num_blocks': [1, 2, 1],
        'expansion': [1, 8, 8],
        'out_channels': [16, 24, 40],
        'kernel_size': [3, 3, 3],
        'stride': [2, 2, 2],
        'dropout_rate': 0.6,
        'drop_connect_rate': 0.6,
    }
    return EfficientNet(cfg)

my_classifier = EfficientNetB0()
my_classifier = my_classifier.to(device)

# Print your neural network structure
print(my_classifier)

optimizer = optim.Adam(my_classifier.parameters(), lr=learning_rate)

ckpt_dir = os.path.join(gdrive_root, 'checkpoints')
ckpt_dir=os.path.join(ckpt_dir, 'new_efficientnet_1')
if not os.path.exists(ckpt_dir):
  os.makedirs(ckpt_dir)
  
best_acc = 0.
ckpt_path = os.path.join(ckpt_dir, 'lastest.pt')
if os.path.exists(ckpt_path):
  ckpt = torch.load(ckpt_path)
  try:
    my_classifier.load_state_dict(ckpt['my_classifier'])
    optimizer.load_state_dict(ckpt['optimizer'])
    best_acc = ckpt['best_acc']
  except RuntimeError as e:
      print('wrong checkpoint')
  else:    
    print('checkpoint is loaded !')
    print('current best accuracy : %.2f' % best_acc)

from pathlib import Path
# Basic settings
name='main'
ckpt_dir='ckpts'
ckpt_reload='10'
gpu=True
log_dir='logs'
log_iter = 100

result_dir = Path(gdrive_root) / 'new_efficientnet_1' / name
ckpt_dir = result_dir / ckpt_dir
ckpt_dir.mkdir(parents=True, exist_ok=True)
log_dir = result_dir / log_dir
log_dir.mkdir(parents=True, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() and gpu else 'cpu'

# Setup tensorboard.
# from torch.utils.tensorboard import SummaryWriter 
# writer = SummaryWriter(log_dir)
# %load_ext tensorboard
# %tensorboard --logdir '/gdrive/My Drive/'{str(log_dir).replace('/gdrive/My Drive/', '')}

from torch.utils.tensorboard import SummaryWriter 
writer = SummaryWriter(log_dir)

if training_process:
  it = 0
  train_losses = []
  test_losses = []
  train_accs = []
  test_accs = []
  for epoch in range(max_epoch):
    # train phase
    my_classifier.train()
    for inputs, labels in train_dataloader:
      it += 1

      # load data to the GPU.
      #P8.1. Send 'inputs' and 'labels' to either cpu or gpu using 'device' variable
      inputs = inputs.to(device)
      labels = labels.to(device)


      # feed data into the network and get outputs.
      # P8.2. Feed `inputs` into the network, get an output, and keep it in a variable called `logit`. 
      logits = my_classifier(inputs)


      # calculate loss
      # Note: `F.cross_entropy` function receives logits, or pre-softmax outputs, rather than final probability scores.
      # P8.3. Compute loss using `logit` and `labels`, and keep it in a variable called `loss` 
      loss =  F.cross_entropy(logits, labels)


      # Note: You should flush out gradients computed at the previous step before computing gradients at the current step. 
      #       Otherwise, gradients will accumulate.
      # P8.4. flush out the previously computed gradient 
      optimizer.zero_grad()


      # backprogate loss.
      # P8.5. backward the computed loss. 
      loss.backward()


      # P8.6. update the network weights. 
      optimizer.step()


      # calculate accuracy.
      acc = (logits.argmax(dim=1) == labels).float().mean()

      if it % 2000 == 0 and writer is not None:
          # P8.7. Log `loss` with a tag name 'train_loss' using `writer`. Use `global_step` as a timestamp for the log. 
          # writer.writer_your_code_here (one-liner).
          writer.add_scalar('train_loss', loss, global_step=epoch)

          # P8.8. Log `accuracy` with a tag name 'train_accuracy' using `writer`. Use `global_step` as a timestamp for the log. 
          # writer.writer_your_code_here (one-liner).
          writer.add_scalar('train_accuracy', acc, global_step=epoch)

          print('[epoch:{}, iteration:{}] train loss : {:.4f} train accuracy : {:.4f}'.format(epoch+1, it, loss.item(), acc.item()))

    # save losses in a list so that we can visualize them later.
    train_losses.append(loss)  
    train_accs.append(acc)


    # test phase
    n = 0.
    test_loss = 0.
    test_acc = 0.

    my_classifier.eval()
    for test_inputs, test_labels in test_dataloader:
      #P8.9. Send 'inputs' and 'labels' to either cpu or gpu using 'device' variable
      #test_inputs = write your code here (one-liner).
      #test_labels = write your code here (one-liner).
      test_inputs = test_inputs.to(device)
      test_labels = test_labels.to(device)


      # P8.10. Feed `inputs` into the network, get an output, and keep it in a variable called `logit`. 
      # logits = write your code here (one-liner).
      logits = my_classifier(test_inputs)


      # Yes, for your convenience.
      test_loss += F.cross_entropy(logits, test_labels, reduction='sum').item()
      test_acc += (logits.argmax(dim=1) == test_labels).float().sum().item()
      n += test_inputs.size(0)

    test_loss /= n
    test_acc /= n
    test_losses.append(test_loss)
    test_accs.append(test_acc)


    # P8.11. Log `test_loss` with a tag name 'test_loss' using `writer`. Use `global_step` as a timestamp for the log.
    # writer.write_your_code_here (one-liner).
    writer.add_scalar('test_loss', test_loss, global_step=epoch)


    # P8.12. Log `test_accuracy` with a tag name 'test_accuracy' using `writer`. Use `global_step` as a timestamp for the log.
    # writer.write_your_code_here (one-liner).
    writer.add_scalar('test_accuracy', test_acc, global_step=epoch)


    print('[epoch:{}, iteration:{}] test_loss : {:.4f} test accuracy : {:.4f}'.format(epoch+1, it, test_loss, test_acc)) 

    writer.flush()
    # save checkpoint whenever there is some improvement in performance
    if test_acc > best_acc:
      best_acc = test_acc
      # Save records.
      ckpt = {'my_classifier':my_classifier.state_dict(),
              'optimizer':optimizer.state_dict(),
              'best_acc':best_acc}
      torch.save(ckpt, ckpt_path)

import matplotlib.pyplot as plt

plt.plot(train_losses, label='train loss')
plt.plot(test_losses, label='test loss')
plt.legend()

if not training_process:
  # Re-load trained model
  my_classifier.load_state_dict(ckpt['my_classifier'])
  optimizer.load_state_dict(ckpt['optimizer'])

  # Testing
  n = 0.
  test_loss = 0.
  test_acc = 0.
  my_classifier.eval()
  for test_inputs, test_labels in test_dataloader:
    test_inputs = test_inputs.to(device)
    test_labels = test_labels.to(device)

    logits = my_classifier(test_inputs)
    test_loss += F.cross_entropy(logits, test_labels, reduction='sum').item()
    test_acc += (logits.argmax(dim=1) == test_labels).float().sum().item()
    n += test_inputs.size(0)

  test_loss /= n
  test_acc /= n
  print('Test_loss : {:.4f}, Test accuracy : {:.4f}'.format(test_loss, test_acc))

plt.plot(train_accs, label='train acc')
plt.plot(test_accs, label='test acc')
plt.legend()

import random

import matplotlib.pyplot as plt
import numpy as np

my_classifier.eval()

num_test_samples = len(test_data)
random_idx = random.randint(0, num_test_samples)

test_input, test_label = test_data.__getitem__(random_idx)
test_prediction = F.softmax(my_classifier(test_input.unsqueeze(0).to(device)), dim=1).argmax().item()
print('label : %s' % classes[test_label])
print('prediction : %s' % classes[test_prediction])

# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

# show images
imshow(torchvision.utils.make_grid(test_input))

class_correct = list(0. for i in range(output_dim))
class_total = list(0. for i in range(output_dim))
my_classifier.eval()
with torch.no_grad():
    for data in test_dataloader:
        images, labels = data
        inputs = images.to(device)
        labels = labels.to(device)
        outputs = my_classifier(inputs)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(list(labels.size())[0]):
            label = labels[i]
            if c[i]: class_correct[label] += 1
            class_total[label] += 1


for i in range(output_dim):
    print('Accuracy of %5s : %2d %%' % (
        classes[i], 100 * class_correct[i] / class_total[i]))