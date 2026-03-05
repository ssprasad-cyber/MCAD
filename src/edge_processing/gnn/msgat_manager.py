import torch
from torch_geometric.data import Data

from .msgat_model import MSGAT


class MSGATManager:

    def __init__(self):

        self.model = MSGAT()
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

            x.append([
                cx,
                cy,
                vx,
                vy
            ])

        edge_index = []

        for edge in graph["edges"]:

            src = node_map.get(edge["source"])
            dst = node_map.get(edge["target"])

            if src is None or dst is None:
                continue

            edge_index.append([src, dst])
            edge_index.append([dst, src])

        if len(edge_index) == 0:
            edge_index = torch.empty((2, 0), dtype=torch.long)
        else:
            edge_index = torch.tensor(edge_index).t().contiguous()

        x = torch.tensor(x, dtype=torch.float)

        batch = torch.zeros(x.shape[0], dtype=torch.long)

        return Data(x=x, edge_index=edge_index, batch=batch)
    


    def predict(self, graph, people):

        data = self.graph_to_data(graph, people)

        if data is None:
            return 0.0

        with torch.no_grad():
            score = float(self.model(data))

        self.history.append(score)

        if len(self.history) > 20:
            self.history.pop(0)

        return sum(self.history) / len(self.history)