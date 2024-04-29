class Edge:
    def __init__(self, origin_node, destiny_node, capacity=10, origin_percentage=0, destination_percentage=0):
        self.origin_node = origin_node
        self.destiny_node = destiny_node
        self.capacity = capacity
        self.origin_percentage = origin_percentage
        self.destination_percentage = destination_percentage