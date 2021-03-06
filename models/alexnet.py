'''
A PyTorch implementation of AlexNet.
The original paper can be found at http://www.cs.toronto.edu/~fritz/absps/imagenet.pdf.
'''

import torch
import torch.nn as nn

from .activations import activetion_func


class AlexNet(nn.Module):
    def __init__(self, activation='relu', num_classes=10):
        super(AlexNet, self).__init__()
        self.activation = activetion_func(activation)
        # Convolutional part.
        '''
        The following implementation is slightly different from the original paper.
        It is because the image size of CIFAR dataset is 32x32.
        '''
        self.conv = nn.Sequential(
            nn.Conv2d(3, 96, kernel_size=5, stride=1), self.activation,
            nn.MaxPool2d(kernel_size=3, stride=1),
            nn.Conv2d(96, 256, kernel_size=5, stride=1,
                      padding=2), self.activation,
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(256, 384, kernel_size=3, stride=1,
                      padding=1), self.activation,
            nn.Conv2d(384, 384, kernel_size=3, stride=1,
                      padding=1), self.activation,
            nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1),
            self.activation, nn.MaxPool2d(kernel_size=3, stride=2))
        # Fully connected part
        self.fc = nn.Sequential(nn.Linear(256 * 5 * 5, 4096), self.activation,
                                nn.Dropout(0.5), nn.Linear(4096, 4096),
                                self.activation, nn.Dropout(0.5),
                                nn.Linear(4096, num_classes))

    def forward(self, x):
        out = self.conv(x)
        out = torch.flatten(out, 1)
        out = self.fc(out)
        return out


def alexnet(activation='relu', num_classes=10):
    return AlexNet(activation, num_classes)


if __name__ == "__main__":
    from ptflops import get_model_complexity_info

    net = alexnet(activation='mish')
    macs, params = get_model_complexity_info(net, (3, 32, 32),
                                             as_strings=True,
                                             print_per_layer_stat=True,
                                             verbose=True)
    print('{:<30}  {:<8}'.format('Number of parameters: ', params))
    print('{:<30}  {:<8}'.format('Computational complexity: ', macs))
