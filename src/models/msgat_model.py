import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv, global_mean_pool

class MSGAT(nn.Module):
    def __init__(self, in_dim=5, edge_dim=2, hidden_dim=64):
        super().__init__()
        
        # GATv2Conv handles edge features natively
        self.gat1 = GATv2Conv(in_dim, hidden_dim, heads=4, edge_dim=edge_dim)
        self.gat2 = GATv2Conv(hidden_dim * 4, hidden_dim, edge_dim=edge_dim)
        
        # Simple GRU for temporal aggregation over a window of graphs
        self.gru = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, data):
        """
        data: torch_geometric Batch object
        data.x: [num_nodes, 5] (cx, cy, vx, vy, bbox_size)
        data.edge_index: [2, num_edges]
        data.edge_attr: [num_edges, 2] (distance, relative_velocity)
        """
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch
        
        x = F.elu(self.gat1(x, edge_index, edge_attr=edge_attr))
        x = F.elu(self.gat2(x, edge_index, edge_attr=edge_attr))
        
        # Global pooling per graph in the batch
        x = global_mean_pool(x, batch)
        
        # Assuming batch corresponds to a temporal sequence of graphs:
        # Reshape to (1, sequence_length, hidden_dim) for GRU
        # If training with multiple sequences, data loading must provide sequence bounds.
        # For simplicity in this implementation, we assume `batch_size` = sequence_length.
        x = x.unsqueeze(0) 
        
        out, _ = self.gru(x)
        
        # Take the output of the last timestep
        out = out[:, -1, :] 
        
        return self.classifier(out)
