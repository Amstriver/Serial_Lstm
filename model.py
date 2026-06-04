import torch
import torch.nn as nn

class TabNet(nn.Module):
    def __init__(self, input_size=3, num_classes=3):
        super(TabNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.model(x)