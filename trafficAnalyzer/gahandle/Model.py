from gahandle.Population import Population


class Model:
    def __init__(self, population_size, mutations_number, mutations_cycle_generations, end_criterion, end_criterion_value, nodes):
        self.population_size = int(population_size)
        self.mutations_number = int(mutations_number)
        self.mutations_cycle_generations = int(mutations_cycle_generations)
        self.end_criterion = end_criterion
        self.end_criterion_value = end_criterion_value
        self.nodes = nodes

    def run_model(self):
        print("generate init population")
        population = Population(nodes=self.nodes, populationSize=self.population_size)
        population.print_population()