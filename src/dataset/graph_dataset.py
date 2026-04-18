"""
Graph Dataset Loader — UCF-Crime window format
==============================================

Loads JSON files produced by generate_graphs.py.

Each JSON file = one temporal window (sliding-window output).
Schema:
    {
        "video": "...",
        "window_start_frame": int,
        "window_end_frame": int,
        "label": 0 or 1,
        "class_id": int or null,
        "sequence": [ { "timestamp":, "nodes":, "edges": }, ... ]
    }

Supports:
  - Binary mode (label 0/1)          — default
  - Multi-class mode (class_id)      — enabled with multi_class=True
  - Class-balanced sampling hint     — .class_weights property
"""

import json
import torch
import numpy as np
from pathlib import Path
from torch.utils.data import Dataset, WeightedRandomSampler
from torch_geometric.data import Data, Batch


def _frame_to_data(frame: dict) -> Data:
    """Convert one graph frame dict to a torch_geometric Data object."""
    nodes = frame.get("nodes", [])
    edges = frame.get("edges", [])

    node_map = {n["gid"]: i for i, n in enumerate(nodes)}

    x = []
    for n in nodes:
        cx, cy = n["center"]
        vx, vy = n["velocity"]
        bbox_size = n.get("bbox_size", 0)
        x.append([float(cx), float(cy), float(vx), float(vy), float(bbox_size)])

    edge_index, edge_attr = [], []
    for e in edges:
        src = node_map.get(e["source"])
        dst = node_map.get(e["target"])
        if src is None or dst is None:
            continue
        edge_index += [[src, dst], [dst, src]]
        dist = float(e.get("distance", 0))
        rel_v = float(e.get("relative_velocity", 0))
        edge_attr += [[dist, rel_v], [dist, rel_v]]

    if len(x) == 0:
        x_t = torch.zeros((1, 5), dtype=torch.float)
        ei_t = torch.empty((2, 0), dtype=torch.long)
        ea_t = torch.empty((0, 2), dtype=torch.float)
    else:
        x_t = torch.tensor(x, dtype=torch.float)
        if len(edge_index) == 0:
            ei_t = torch.empty((2, 0), dtype=torch.long)
            ea_t = torch.empty((0, 2), dtype=torch.float)
        else:
            ei_t = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
            ea_t = torch.tensor(edge_attr, dtype=torch.float)

    return Data(x=x_t, edge_index=ei_t, edge_attr=ea_t)


class GraphDataset(Dataset):
    """
    Loads pre-generated window JSON files.

    Args:
        data_dirs:    str or list of str/Path — directories containing JSON files.
                      Accepts mixed anomaly + normal dirs, e.g. ['data/graphs/anomaly', 'data/graphs/normal'].
        multi_class:  if True, uses class_id as label (int). Default False (binary 0/1).
        max_samples:  optional cap on total samples (useful for quick experiments).
    """

    def __init__(self, data_dirs, multi_class=False, max_samples=None):

        if isinstance(data_dirs, (str, Path)):
            data_dirs = [data_dirs]

        self.multi_class = multi_class
        self.records = []   # list of Path objects to JSON files

        for d in data_dirs:
            p = Path(d)
            if not p.exists():
                print(f"[WARN] Dataset dir not found: {p}")
                continue
            files = sorted(p.glob("*.json"))
            self.records.extend(files)

        if max_samples:
            self.records = self.records[:max_samples]

        if len(self.records) == 0:
            raise RuntimeError(
                f"No JSON files found in: {data_dirs}. "
                "Run generate_graphs.py first."
            )

        print(f"GraphDataset: {len(self.records)} windows loaded from {data_dirs}")

    # ------------------------------------------------------------------
    # Class weights for balanced sampling
    # ------------------------------------------------------------------
    @property
    def class_weights(self):
        """Returns a weight per sample for WeightedRandomSampler."""
        labels = []
        for p in self.records:
            with open(p) as f:
                d = json.load(f)
            labels.append(d["label"])
        labels = np.array(labels)
        counts = np.bincount(labels)
        weight_per_class = 1.0 / np.maximum(counts, 1)
        return torch.tensor([weight_per_class[l] for l in labels], dtype=torch.double)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        with open(self.records[idx]) as f:
            record = json.load(f)

        sequence = record["sequence"]

        # Convert each frame to a PyG Data object, then batch them
        # into one disjoint graph batch (temporal window)
        graph_list = [_frame_to_data(frame) for frame in sequence]
        batched = Batch.from_data_list(graph_list)

        if self.multi_class:
            class_id = record.get("class_id")
            label = torch.tensor([class_id if class_id is not None else 0], dtype=torch.long)
        else:
            label = torch.tensor([record["label"]], dtype=torch.float)

        return batched, label


# ------------------------------------------------------------------
# Collate function for DataLoader
# ------------------------------------------------------------------
def collate_fn(batch):
    """
    Each item is (Batch, label_tensor).
    We cannot simply stack Batch objects, so we return lists.
    The training loop handles them individually.
    """
    windows, labels = zip(*batch)
    return list(windows), torch.stack(labels)


def make_sampler(dataset: GraphDataset) -> WeightedRandomSampler:
    """Build a WeightedRandomSampler for class-balanced training."""
    weights = dataset.class_weights
    return WeightedRandomSampler(weights, num_samples=len(weights), replacement=True)
