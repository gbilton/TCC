import torch
from torch import nn


class DQN(nn.Module):
    def __init__(self, input_size=4, output_size=2,
                 device=torch.device('cpu')):
        super(DQN, self).__init__()

        self.fc1 = nn.Linear(input_size, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 100)
        self.out = nn.Linear(100, output_size)

        self.device = device
        self.to(self.device)

    def forward(self, t):
        t = torch.tanh(self.fc1(t))
        t = torch.tanh(self.fc2(t))
        t = torch.tanh(self.fc3(t))
        t = self.out(t)
        return t

    def act(self, observation):
        observation = torch.tensor(
            observation, dtype=torch.float).to(self.device)
        action = self.forward(observation)
        return action.argmax().item()