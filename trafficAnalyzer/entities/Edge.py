class Edge:
    def __init__(self, origin_node, destiny_node, capacity=10, origin_percentage=0, destination_percentage=0, canvas_text_id=None):
        self.origin_node = origin_node
        self.destiny_node = destiny_node
        self.capacity = capacity
        self.origin_percentage = int(origin_percentage)
        self.destination_percentage = int(destination_percentage)
        self.vehicles_in = 0
        self.canvas_text_id = canvas_text_id
