class TemporalManager:

    def __init__(self, memory):

        self.memory = memory


    def process(self, graph):

        self.memory.update(graph)

        sequence = self.memory.get_sequence()

        return sequence