import copy
import random
from gahandle.Chromosome import Chromosome


class Population():
    def __init__(self, nodes, populationSize=10):
        self.nodes = [node_data["node"] for node_data in nodes]

        self.populationSize = populationSize
        self.population = []
        self.aux_population = []
        # Generate init population
        self.generate_population()
        self.max_value = self.get_max_value()

    def generate_population(self):
        for i in range(self.populationSize):
            self.population.append(Chromosome(nodes=self.nodes))

    def print_population(self):
        print("size: " + str(len(self.population)))
        for chromosome in self.population:
            print(chromosome.str_percentages())

    def new_generation(self):
        # get couple number
        couple_number = int(len(self.population) / 2)
        for i in range(couple_number):
            parent_1 = self.get_parent()
            parent_2 = self.get_parent()
            self.crossover(parent_1_object=parent_1, parent_2_object=parent_2)

        if len(self.population) % 2 != 0:
            random_number = random.randint(0, len(self.population) - 1)
            self.aux_population.append(self.population[random_number])
        self.population = self.aux_population
        self.aux_population = []


    def get_parent(self):
        value = random.randint(self.population[0].fitness_value, self.max_value)
        sum = 0
        for i in range(len(self.population)):
            sum += self.population[i].fitness_value
            if sum > value:
                return self.population[i]
        return self.population[len(self.population) - 1]

    def crossover(self, parent_1_object, parent_2_object):
        parent_1 = copy.deepcopy(parent_1_object.clean_genes)
        parent_2 = copy.deepcopy(parent_2_object.clean_genes)

        # cross point
        crossover_point = len(parent_1) // 2

        first_child = Chromosome(nodes=self.nodes, genes=parent_1[:crossover_point] + parent_2[crossover_point:])
        second_child = Chromosome(nodes=self.nodes, genes=parent_2[:crossover_point] + parent_1[crossover_point:])

        print("De los padres")
        print(str(parent_1_object.str_percentages()))
        print(str(parent_2_object.str_percentages()))

        print("\nSalen")
        print(str(first_child))
        print(str(second_child))

        self.aux_population.append(first_child)
        self.aux_population.append(second_child)

    def get_max_value(self):
        value = self.population[0].fitness_value
        for i in range(len(self.population)):
            value += self.population[i].fitness_value
        return value

    def get_best_chromosome(self):
        max_fv = 0
        best_chromosome = None
        for chromosome in self.population:
            if chromosome.fitness_value > max_fv:
                best_chromosome = chromosome
            max_fv = chromosome.fitness_value
        return best_chromosome

    def mutate_population(self):
        random_value = random.randint(0, len(self.population) - 1)
        self.population[random_value].mutate()
