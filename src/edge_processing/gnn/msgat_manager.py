import torch
from torch_geometric.data import Data
import os

from models.msgat_model import MSGAT


class MSGATManager:

    def __init__(self, model_path=None):

        self.model = MSGAT()
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        
        self.model.eval()
        self.history = []


    def graph_to_data(self, graph, people):

        if len(people) == 0:
            return None

        node_map = {p["gid"]: i for i, p in enumerate(people)}

        x = []
        for p in people:
            cx, cy = p["center"]
            vx, vy = p.get("velocity", (0,0))
            bbox_size = p.get("bbox_size", 0)

            x.append([
                float(cx),
                float(cy),
                float(vx),
                float(vy),
                float(bbox_size)
            ])

        edge_index = []
        edge_attr = []

        for edge in graph["edges"]:

            src = node_map.get(edge["source"])
            dst = node_map.get(edge["target"])

            if src is None or dst is None:
                continue

            edge_index.append([src, dst])
            edge_index.append([dst, src])
            
            e_dist = float(edge.get("distance", 0))
            e_rel_v = float(edge.get("relative_velocity", 0))
            
            edge_attr.append([e_dist, e_rel_v])
            edge_attr.append([e_dist, e_rel_v])

        if len(edge_index) == 0:
            edge_index = torch.empty((2, 0), dtype=torch.long)
            edge_attr = torch.empty((0, 2), dtype=torch.float)
        else:
            edge_index = torch.tensor(edge_index).t().contiguous()
            edge_attr = torch.tensor(edge_attr, dtype=torch.float)

        x = torch.tensor(x, dtype=torch.float)

        batch = torch.zeros(x.shape[0], dtype=torch.long)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, batch=batch)
    

    def predict(self, graph, people):

        data = self.graph_to_data(graph, people)

        if data is None:
            score = 0.0
        else:
            with torch.no_grad():
                # Model expects batch containing potentially sequence, here it is length 1
                score = float(self.model(data).squeeze())

        # Smoothing via moving average
        self.history.append(score)

        if len(self.history) > 20:
            self.history.pop(0)

        return sum(self.history) / len(self.history)