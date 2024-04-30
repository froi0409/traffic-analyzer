import copy
import random
from entities.Node import Node, NodeType
from entities.Edge import Edge

class Chromosome:
    def __init__(self, nodes):
        self.nodes = copy.deepcopy(nodes)
        self.genes = []
        self.generate_chromosome()

    def generate_chromosome(self):
        for node in self.nodes:
            if node.node_type == NodeType.NORMAL or node.node_type == NodeType.INPUT:
                self.genes.append(self.generate_percentages(node))

    def generate_percentages(self, node):
        rest_percentage = 100
        # Substract min percentages
        for edge in node.output_edges:
            rest_percentage -= int(edge.origin_percentage)
            print(str(rest_percentage))

        # Add rest percentage
        for index, edge in enumerate(node.output_edges):
            if index == len(node.output_edges) - 1:
                edge.origin_percentage = int(edge.origin_percentage) + rest_percentage
                rest_percentage = 0
            else:
                random_percentage = random.randint(0, rest_percentage)
                print("Random: " + str(random_percentage))
                print("origin before: " + str(edge.origin_percentage))
                edge.origin_percentage = int(edge.origin_percentage) + random_percentage
                print("origin: " + str(edge.origin_percentage))
                rest_percentage -= random_percentage

        return node

    def str_percentages(self):
        chain = ""
        for gene in self.genes:
            for edge in gene.output_edges:
                chain += str(edge.origin_percentage) + " "
            chain += " | "
        return chain
