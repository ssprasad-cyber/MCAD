import numpy as np


class InteractionGraph:

    def __init__(self, distance_threshold=150):

        self.distance_threshold = distance_threshold


    def build(self, people):

        nodes = []
        edges = []

        for p in people:
            nodes.append(p["gid"])

        for i in range(len(people)):
            for j in range(i + 1, len(people)):

                p1 = people[i]
                p2 = people[j]

                x1, y1 = p1["center"]
                x2, y2 = p2["center"]

                dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

                if dist < self.distance_threshold:

                    edges.append({
                        "source": p1["gid"],
                        "target": p2["gid"],
                        "distance": dist
                    })

        return nodes, edges