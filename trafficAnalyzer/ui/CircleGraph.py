import tkinter as tk
from tkinter import Canvas, Button, Entry, Label

from tkinter import *
from tkinter.ttk import Combobox

from entities.Node import Node
from entities.Edge import Edge


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

        self.aux_button = Button(root, text="Nodos y Aristas", command=self.print_nodes_and_connections)
        self.aux_button.place(x=300, y=10)

        self.nodes = []
        self.connections = []
        self.arrows = []
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

    def print_nodes_and_connections(self):
        # Limpiar la consola
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

        # Imprimir los valores de nodes
        print("Nodes:")
        for node_data in self.nodes:
            print(node_data)

        # Imprimir los valores de connections
        print("\nConnections:")
        for arrow_data in self.connections:
            print(arrow_data)

    def handle_canvas_click(self, event):
        if self.create_circle_button_active:
            self.create_circle(event)
        elif self.delete_button_active:
            self.delete_item(event)
        else:
            self.toggle_circle_color(event)

    def create_circle(self, event):
        x, y = event.x, event.y
        circle = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="white")
        circle_data = {
            "id": circle,
            "center": (x, y),
            "selected": False
        }
        self.nodes.append(circle_data)

    def connect_circles(self, event):
        for node_data in self.nodes:
            node = node_data["id"]
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if len(self.arrows) < 2:
                    self.arrows.append(node_data)
                    if not node_data["selected"]:
                        self.canvas.itemconfig(node, fill="yellow")
                        node_data["selected"] = True
                if len(self.arrows) == 2:
                    start_node_data, end_node_data = self.arrows
                    start_node = start_node_data["id"]
                    end_node = end_node_data["id"]
                    start_center_x, start_center_y = start_node_data["center"]
                    end_center_x, end_center_y = end_node_data["center"]
                    # Calcular la dirección desde el centro del primer círculo hasta el centro del segundo
                    direction = (end_center_x - start_center_x, end_center_y - start_center_y)
                    # Normalizar la dirección para que tenga una longitud de 1
                    length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
                    direction = (direction[0] / length, direction[1] / length)
                    # Calcular el punto en el borde del primer círculo
                    start_point = (start_center_x + direction[0] * 15, start_center_y + direction[1] * 15)
                    # Calcular el punto en el borde del segundo círculo
                    end_point = (end_center_x - direction[0] * 15, end_center_y - direction[1] * 15)
                    arrow = self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1],
                                                    arrow=tk.LAST, width=3)
                    arrow_data = {
                        "id": arrow,
                        "start_node": start_node_data,
                        "end_node": end_node_data
                    }
                    self.connections.append(arrow_data)
                    self.arrows = []
                    start_node_data["selected"] = False
                    end_node_data["selected"] = False
                    self.canvas.itemconfig(start_node, fill="white")  # Cambiar color de círculo de origen a blanco
                    self.canvas.itemconfig(end_node, fill="white")
                break

    def toggle_circle_color(self, event):
        for node_data in self.nodes:
            node = node_data["id"]
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if not node_data["selected"]:
                    self.canvas.itemconfig(node, fill="yellow")
                    node_data["selected"] = True
                else:
                    self.canvas.itemconfig(node, fill="white")
                    node_data["selected"] = False
                break

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
        for node_data in self.nodes:
            node = node_data["id"]
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                connections_to_delete = []
                # Eliminar todas las líneas conectadas al círculo
                for line in self.connections:
                    print(line["start_node"]["id"], "-", line["end_node"]["id"])
                    if node == line["start_node"]["id"] or node == line["end_node"]["id"]:
                        self.canvas.delete(line["id"])
                        connections_to_delete.append(line)

                for deleted_connection in connections_to_delete:
                    self.connections.remove(deleted_connection)
                self.canvas.delete(node)
                self.nodes.remove(node_data)
                break
