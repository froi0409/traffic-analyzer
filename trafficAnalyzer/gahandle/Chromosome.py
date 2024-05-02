import copy
import random
from entities.Node import Node, NodeType
from entities.Edge import Edge


class Chromosome:
    def __init__(self, nodes, genes=None):
        self.nodes = copy.deepcopy(nodes)
        if genes is None:
            self.genes = []
            self.generate_chromosome()
        else:
            self.genes = genes

        self.input_nodes = []
        self.get_inputs()

        self.out_cars = 0
        self.fitness_function()
        self.fitness_value = self.out_cars

    def get_inputs(self):
        for node in self.nodes:
            if node.node_type == NodeType.INPUT:
                self.input_nodes.append(node)

    def generate_chromosome(self):
        for node in self.nodes:
            if node.node_type == NodeType.NORMAL or node.node_type == NodeType.INPUT:
                self.genes.append(self.generate_percentages(node))

    def generate_percentages(self, node):
        rest_percentage = 100
        # Substract min percentages
        for edge in node.output_edges:
            rest_percentage -= int(edge.origin_percentage)

        # Add rest percentage
        for index, edge in enumerate(node.output_edges):
            if index == len(node.output_edges) - 1:
                edge.origin_percentage = int(edge.origin_percentage) + rest_percentage
                rest_percentage = 0
            else:
                random_percentage = random.randint(0, rest_percentage)
                edge.origin_percentage = int(edge.origin_percentage) + random_percentage
                rest_percentage -= random_percentage

        return node

    def str_percentages(self):
        chain = ""
        for gene in self.genes:
            for edge in gene.output_edges:
                chain += str(edge.origin_percentage) + " "
            chain += " | "
        chain += str(self.fitness_value)
        return chain

    def fitness_function(self):
        for input in self.input_nodes:
            self.move_cars_from_input_node(node=input)

    def move_cars_from_input_node(self, node):
        for i in range(node.input_vehicles):
            random_value = random.randint(1,100)
            percentage_edge = 0
            flag = True
            for edge in node.output_edges:
                if flag:
                    percentage_edge += edge.origin_percentage
                    if random_value <= percentage_edge:
                        if edge.vehicles_in >= edge.capacity:
                            break
                        node.input_vehicles = int(node.input_vehicles) - 1
                        edge.vehicles_in = int(edge.vehicles_in) + 1
                        flag = False
            else:
                continue
            break

        for edge in node.output_edges:
            self.move_cars_from_edge(edge=edge)

    def move_cars_from_edge(self, edge):
        if edge.destiny_node.node_type == NodeType.OUTPUT:
            print("salen desde: " + str(edge.origin_percentage) + " - " + str(edge.vehicles_in))
            self.out_cars += edge.vehicles_in
            edge.vehicles_in = 0
        elif len(edge.destiny_node.output_edges) > 0:
            for i in range(edge.vehicles_in):
                random_value = random.randint(1,100)
                percentage_edge = 0
                flag = True
                for destiny_edge in edge.destiny_node.output_edges:
                    if flag:
                        percentage_edge += destiny_edge.origin_percentage
                        if random_value <= percentage_edge:
                            if destiny_edge.vehicles_in >= destiny_edge.capacity:
                                break
                            edge.vehicles_in = int(edge.vehicles_in) - 1
                            destiny_edge.vehicles_in = int(destiny_edge.vehicles_in) + 1
                            flag = False
                else:
                    continue
                break

            for destiny_edge in edge.destiny_node.output_edges:
                self.move_cars_from_edge(edge=destiny_edge)