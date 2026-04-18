import numpy as np


class InteractionGraph:

    def __init__(self, distance_threshold=150):

        self.distance_threshold = distance_threshold


    def build(self, people):

        nodes = []
        edges = []

        for p in people:
            nodes.append({
                "gid": p["gid"],
                "center": p["center"],
                "velocity": p["velocity"],
                "bbox_size": p.get("bbox_size", 0)
            })

        for i in range(len(people)):
            for j in range(i + 1, len(people)):

                p1 = people[i]
                p2 = people[j]

                x1, y1 = p1["center"]
                x2, y2 = p2["center"]
                
                v1x, v1y = p1["velocity"]
                v2x, v2y = p2["velocity"]

                dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                rel_v = np.sqrt((v1x - v2x)**2 + (v1y - v2y)**2)

                if dist < self.distance_threshold:

                    edges.append({
                        "source": p1["gid"],
                        "target": p2["gid"],
                        "distance": dist,
                        "relative_velocity": rel_v
                    })

        return nodes, edges