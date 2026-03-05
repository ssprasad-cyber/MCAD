import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv, global_mean_pool


class MSGAT(nn.Module):

    def __init__(self, in_dim=4, hidden_dim=32):

        super().__init__()

        self.gat1 = GATConv(in_dim, hidden_dim, heads=4)
        self.gat2 = GATConv(hidden_dim * 4, hidden_dim)

        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, data):

        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = F.elu(self.gat1(x, edge_index))
        x = F.elu(self.gat2(x, edge_index))

        x = global_mean_pool(x, batch)

        return self.classifier(x)