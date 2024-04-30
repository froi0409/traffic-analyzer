from enum import Enum


class NodeType(Enum):
    NORMAL = 1
    INPUT = 2
    OUTPUT = 3


class Node:
    def __init__(self, id, input_vehicles=0):
        self.id = id
        self.input_edges = []
        self.output_edges = []
        self.node_type = NodeType.NORMAL
        self.input_vehicles = input_vehicles
