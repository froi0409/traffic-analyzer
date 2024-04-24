class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.input_edges = []
        self.output_edges = []
