
import tkinter as tk
from tkinter import Canvas, Button, Entry, Label

from tkinter import *
from tkinter.ttk import Combobox

class CircleGraph:
    def __init__(self, root):
        self.root = root

        self.create_circle_button = Button(root, text="Crear Círculo", command=self.toggle_create_circle_button)
        self.create_circle_button.place(x=10, y=10)

        self.delete_button = Button(root, text="Eliminar Circulos y Flechas", command=self.toggle_delete_button)
        self.delete_button.place(x=120, y=10)

        self.canvas = Canvas(root, width=1280, height=720, bg='#CAC9C9')
        self.canvas.place(x=0, y=40)

        self.population_size_label = Label(root, text="Población")
        self.population_size_label.place(x=130, y=770)
        self.population_size_entry = Entry(root)
        self.population_size_entry.place(x=200, y=770)

        self.mutations_number_label = Label(root, text="Mutaciones")
        self.mutations_number_label.place(x=10, y=800)
        self.mutations_number_entry = Entry(root)
        self.mutations_number_entry.place(x=80, y=800)

        self.mutations_cycle_generations_label = Label(root, text="Generaciones")
        self.mutations_cycle_generations_label.place(x=210, y=800)
        self.mutations_cycle_generations_entry = Entry(root)
        self.mutations_cycle_generations_entry.place(x=290, y=800)

        self.end_criterion_label = Label(root, text="Finalización")
        self.end_criterion_label.place(x=10, y=830)
        self.end_criterion_entry = Combobox(root, width=17)
        self.end_criterion_entry["values"] = ("Generaciones", "Eficiencia")
        self.end_criterion_entry.place(x=80, y=830)

        self.end_criterion_value_label = Label(root, text="Valor")
        self.end_criterion_value_label.place(x=210, y=830)
        self.end_criterion_value_entry = Entry(root)
        self.end_criterion_value_entry.place(x=290, y=830)

        self.nodes = []
        self.connections = []
        self.create_circle_button_active = False
        self.delete_button_active = False

        # set window properties
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = 1280
        height = int(screen_height * 0.8)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")

        self.canvas.bind("<Button-1>", self.handle_canvas_click)
        self.canvas.bind("<Button-3>", self.connect_circles)
        self.canvas.bind("<Button-2>", self.delete_item)

    def handle_canvas_click(self, event):
        if self.create_circle_button_active:
            self.create_circle(event)
        elif self.delete_button_active:
            self.delete_item(event)

    def create_circle(self, event):
        x, y = event.x, event.y
        circle = self.canvas.create_oval(x-15, y-15, x+15, y+15)
        self.nodes.append((circle, (x, y)))

    def connect_circles(self, event):
        for node, (center_x, center_y) in self.nodes:
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if len(self.connections) < 2:
                    self.connections.append((node, (center_x, center_y)))
                if len(self.connections) == 2:
                    start_node, start_center = self.connections[0]
                    end_node, end_center = self.connections[1]
                    # Calcular la dirección desde el centro del primer círculo hasta el centro del segundo
                    direction = (end_center[0] - start_center[0], end_center[1] - start_center[1])
                    # Normalizar la dirección para que tenga una longitud de 1
                    length = (direction[0]**2 + direction[1]**2)**0.5
                    direction = (direction[0] / length, direction[1] / length)
                    # Calcular el punto en el borde del primer círculo
                    start_point = (start_center[0] + direction[0] * 10, start_center[1] + direction[1] * 10)
                    # Calcular el punto en el borde del segundo círculo
                    end_point = (end_center[0] - direction[0] * 10, end_center[1] - direction[1] * 10)
                    self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1], arrow=tk.LAST, width=3)
                    self.connections = []

    def toggle_create_circle_button(self):
        self.create_circle_button_active = not self.create_circle_button_active
        if self.create_circle_button_active:
            self.delete_button_active = False
            self.delete_button.config(relief=tk.RAISED)
        self.update_button_state()

    def toggle_delete_button(self):
        self.delete_button_active = not self.delete_button_active
        if self.delete_button_active:
            self.create_circle_button_active = False
            self.create_circle_button.config(relief=tk.RAISED)
        self.update_button_state()

    def update_button_state(self):
        if self.create_circle_button_active:
            self.create_circle_button.config(relief=tk.SUNKEN)
        else:
            self.create_circle_button.config(relief=tk.RAISED)
        if self.delete_button_active:
            self.delete_button.config(relief=tk.SUNKEN)
        else:
            self.delete_button.config(relief=tk.RAISED)

    def delete_item(self, event):
        for node, (center_x, center_y) in self.nodes:
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                # Eliminar todas las líneas conectadas al círculo
                for line in self.canvas.find_withtag("line"):
                    x1, y1, x2, y2 = self.canvas.coords(line)
                    if (x1 <= center_x <= x2 and y1 <= center_y <= y2) or (
                            x1 <= center_x <= x2 and y1 >= center_y >= y2):
                        self.canvas.delete(line)
                self.canvas.delete(node)
                self.nodes.remove((node, (center_x, center_y)))
                break
        else:
            for line in self.canvas.find_withtag("line"):
                x1, y1, x2, y2 = self.canvas.coords(line)
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.canvas.delete(line)
                    break


root = tk.Tk()
app = CircleGraph(root)
root.mainloop()
