from gahandle.Population import Population
import tkinter as tk
import time


class Model:
    def __init__(self, population_size, mutations_number, mutations_cycle_generations, end_criterion, end_criterion_value, nodes, canvas, root, efficiency_text):
        self.population_size = int(population_size)
        self.mutations_number = int(mutations_number)
        self.mutations_cycle_generations = int(mutations_cycle_generations)
        self.end_criterion = end_criterion
        self.end_criterion_value = int(end_criterion_value)
        self.nodes = nodes
        self.canvas = canvas
        self.root = root
        self.efficiency_text = efficiency_text

    def run_model(self):
        print("generate init population")
        population = Population(nodes=self.nodes, populationSize=self.population_size)
        population.print_population()
        if self.end_criterion == "Generaciones":
            for i in range(self.end_criterion_value):
                population.new_generation()
                solution = population.get_best_chromosome()
                solution.update_canvas_value(canvas_plain=self.canvas)

                efficiency_text_value = "Eficiencia: " + str(solution.fitness_value) + "%"
                self.canvas.itemconfig(self.efficiency_text, text=efficiency_text_value)
                print("\n-------------Generación " + str(i+1) + "-------------\n")
                population.print_population()
                self.root.update_idletasks()

                if (i+1) % self.mutations_cycle_generations == 0:
                    for j in range(self.mutations_number):
                        population.mutate_population()
