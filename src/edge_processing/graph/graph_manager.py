from .interaction_graph import InteractionGraph


class GraphManager:

    def __init__(self):

        self.graph_builder = InteractionGraph()


    def process(self, tracked_people):

        nodes, edges = self.graph_builder.build(tracked_people)

        return {
            "nodes": nodes,
            "edges": edges
        }
    