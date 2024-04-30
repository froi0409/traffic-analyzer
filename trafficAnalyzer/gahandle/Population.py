from gahandle.Chromosome import Chromosome


class Population():
    def __init__(self, nodes, populationSize=10):
        self.nodes = [node_data["node"] for node_data in nodes]
        self.populationSize = populationSize
        self.population = []
        # Generate init population
        self.generate_population()

    def generate_population(self):
        for i in range(self.populationSize):
            self.population.append(Chromosome(nodes=self.nodes))

    def print_population(self):
        print("size: " + str(len(self.population)))
        for chromosome in self.population:
            print(chromosome.str_percentages())
