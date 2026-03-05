from collections import deque


class TemporalMemory:

    def __init__(self, window_size=10):

        self.window_size = window_size
        self.memory = deque(maxlen=window_size)


    def update(self, graph):

        self.memory.append(graph)


    def get_sequence(self):

        return list(self.memory)