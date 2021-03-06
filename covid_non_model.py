import torch 
import torch.nn as nn
import torch.nn.functional as F

# covid: 1, non_covid: 0 

# Define classifier class
class covid_non_model(nn.Module):
    def __init__(self):
        ''' Builds a feedforward network with arbitrary hidden layers.
        
            Arguments
            ---------
            input_size: integer, size of the input
            output_size: integer, size of the output layer
            hidden_layers: list of integers, the sizes of the hidden layers
            drop_p: float between 0 and 1, dropout probability
        '''
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv3 = nn.Conv2d(64, 128, 3)
        self.fc1 = nn.Linear(17*17*128, 120)
        self.fc2 = nn.Linear(120, 100)
        self.fc3 = nn.Linear(100, 1)

        self.initialize_weights()
        
    def forward(self, x):
        ''' Forward pass through the network, returns the output logits '''
        
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = torch.flatten(x, 1)
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = nn.Tanh()(self.fc1(x))
        x = nn.Tanh()(self.fc2(x))
        x = self.fc3(x)
        return torch.sigmoid(x) #Use F.sigmoid(x) or torch.sigmoid(x)

    def initialize_weights(self):
        for m in self.modules():
            # if isinstance(m, nn.Conv2d):
            #     nn.init.kaiming_uniform_(m.weight)
                    
            #     if m.bias is not None:
            #         nn.init.constant_(m.bias, 0)

            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)