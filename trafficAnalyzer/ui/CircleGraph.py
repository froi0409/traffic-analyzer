import pickle
import tkinter as tk
from tkinter import Canvas, Button, Entry, Label

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox

from gahandle.Model import Model
from entities.Node import Node
from entities.Node import NodeType
from entities.Edge import Edge


class CircleGraph:
    def __init__(self, root):
        self.root = root

        self.create_circle_button = Button(root, text="Crear Círculo", command=self.toggle_create_circle_button)
        self.create_circle_button.place(x=10, y=10)

        self.delete_button = Button(root, text="Eliminar Circulos y Flechas", command=self.toggle_delete_button)
        self.delete_button.place(x=120, y=10)

        self.set_input_button = Button(root, text="Agregar Entrada", command=self.toggle_set_input_button)
        self.set_input_button.place(x=300, y=10)

        self.set_output_button = Button(root, text="Agregar Salida", command=self.toggle_set_output_button)
        self.set_output_button.place(x=420, y=10)

        self.save_button = Button(root, text="Guardar Modelo", command=self.save_dict_recursive)
        self.save_button.place(x=530, y=10)

        self.load_button = Button(root, text="Cargar Modelo", command=self.load_dict_recursive)
        self.load_button.place(x=650, y=10)

        self.canvas = Canvas(root, width=1280, height=720, bg='#CAC9C9')
        self.canvas.place(x=0, y=40)

        self.fitness_value_text = self.canvas.create_text(85, 15, text="Eficiencia: 0%", font=("Arial", 12, "bold"), fill="black")

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
        self.aux_button.place(x=1000, y=10)

        self.run_model_button = Button(root, height=5, width=50, fg="white", bg="green", text="Ejecutar Modelo",
                                       command=self.run_model)
        self.run_model_button.place(x=450, y=770)

        self.stop_model_button = Button(root, height=5, width=50, fg="white", bg="red", text="Parar Ejecución",
                                        command=self.stop_model)
        self.stop_model_button.place(x=850, y=770)
        self.stop_model_button.configure(state="disabled")

        self.nodes = []
        self.connections = []
        self.arrows = []
        self.create_circle_button_active = False
        self.delete_button_active = False
        self.set_input_button_active = False
        self.set_output_button_active = False

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
        elif self.set_input_button_active:
            self.set_input_node(event)
        elif self.set_output_button_active:
            self.set_output_node(event)

    def create_circle(self, event):
        x, y = event.x, event.y
        circle = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white")
        node = Node(id=circle)
        circle_data = {
            "id": circle,
            "center": (x, y),
            "selected": False,
            "node": node
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
                    edge = Edge(origin_node=start_node_data["node"], destiny_node=end_node_data["node"])
                    arrow_data = {
                        "id": arrow,
                        "start_node": start_node_data,
                        "end_node": end_node_data,
                        "edge": edge
                    }
                    start_node_data["node"].output_edges.append(edge)
                    self.connections.append(arrow_data)
                    self.arrows = []
                    start_node_data["selected"] = False
                    end_node_data["selected"] = False

                    self.change_node_color(start_node_data)
                    self.change_node_color(end_node_data)
                    self.add_properties_window(arrow_data)
                break

    def change_node_color(self, node_data):
        if node_data["node"].node_type == NodeType.INPUT:
            self.canvas.itemconfig(node_data["id"], fill="green")
        elif node_data["node"].node_type == NodeType.OUTPUT:
            self.canvas.itemconfig(node_data["id"], fill="red")
        else:
            self.canvas.itemconfig(node_data["id"], fill="white")

    def set_input_node(self, event):
        for node_data in self.nodes:
            node = node_data["id"]
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                node_data["node"].node_type = NodeType.INPUT
                self.change_node_color(node_data)
                self.add_input_properties_window(node_data)
                break

    def set_output_node(self, event):
        for node_data in self.nodes:
            node = node_data["id"]
            x1, y1, x2, y2 = self.canvas.coords(node)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                node_data["node"].node_type = NodeType.OUTPUT
                self.change_node_color(node_data)
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
                    self.change_node_color(node_data)
                    node_data["selected"] = False
                break

    def toggle_create_circle_button(self):
        self.create_circle_button_active = not self.create_circle_button_active
        if self.create_circle_button_active:
            self.delete_button_active = False
            self.delete_button.config(relief=tk.RAISED)
            self.set_output_button_active = False
            self.set_output_button.config(relief=tk.RAISED)
            self.set_input_button_active = False
            self.set_output_button.config(relief=tk.RAISED)
        self.update_button_state()

    def toggle_delete_button(self):
        self.delete_button_active = not self.delete_button_active
        if self.delete_button_active:
            self.create_circle_button_active = False
            self.create_circle_button.config(relief=tk.RAISED)
            self.set_output_button_active = False
            self.set_output_button.config(relief=tk.RAISED)
            self.set_input_button_active = False
            self.set_output_button.config(relief=tk.RAISED)
        self.update_button_state()

    def toggle_set_input_button(self):
        self.set_input_button_active = not self.set_input_button_active
        if self.set_input_button_active:
            self.delete_button_active = False
            self.delete_button.config(relief=tk.RAISED)
            self.create_circle_button_active = False
            self.create_circle_button.config(relief=tk.RAISED)
            self.set_output_button_active = False
            self.set_output_button.config(relief=tk.RAISED)
        self.update_button_state()

    def toggle_set_output_button(self):
        self.set_output_button_active = not self.set_output_button_active
        if self.set_output_button_active:
            self.delete_button_active = False
            self.delete_button.config(relief=tk.RAISED)
            self.create_circle_button_active = False
            self.create_circle_button.config(relief=tk.RAISED)
            self.set_input_button_active = False
            self.set_input_button.config(relief=tk.RAISED)
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
        if self.set_input_button_active:
            self.set_input_button.config(relief=tk.SUNKEN)
        else:
            self.set_input_button.config(relief=tk.RAISED)
        if self.set_output_button_active:
            self.set_output_button.config(relief=tk.SUNKEN)
        else:
            self.set_output_button.config(relief=tk.RAISED)

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

    def add_properties_window(self, arrow_data):
        properties_window = tk.Toplevel()
        properties_window.title("Propiedades del Camino")

        capacity_label = Label(properties_window, text="Capacidad:")
        capacity_label.grid(row=0, column=0)
        capacity_entry = Entry(properties_window)
        capacity_entry.grid(row=0, column=1)

        origin_percentage_label = Label(properties_window, text="% Origen:")
        origin_percentage_label.grid(row=1, column=0)
        origin_percentage_entry = Entry(properties_window)
        origin_percentage_entry.grid(row=1, column=1)

        save_button = Button(properties_window, text="Guardar",
                             command=lambda: self.save_properties(arrow_data, capacity_entry.get(),
                                                                  origin_percentage_entry.get(),
                                                                  properties_window))
        save_button.grid(row=3, column=0, columnspan=2)

    def save_properties(self, arrow_data, capacity, origin_percentage, properties_window):
        arrow_data["edge"].capacity = int(capacity)
        arrow_data["edge"].origin_percentage = int(origin_percentage)
        properties_window.destroy()

        # Crear el texto con la información de la flecha
        start_node_data, end_node_data = arrow_data["start_node"], arrow_data["end_node"]
        start_center_x, start_center_y = start_node_data["center"]
        end_center_x, end_center_y = end_node_data["center"]
        direction = (end_center_x - start_center_x, end_center_y - start_center_y)
        length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        direction = (direction[0] / length, direction[1] / length)
        start_point = (start_center_x + direction[0] * 15, start_center_y + direction[1] * 15)
        end_point = (end_center_x - direction[0] * 15, end_center_y - direction[1] * 15)
        text_x = (start_point[0] + end_point[0]) / 2
        text_y = (start_point[1] + end_point[1]) / 2
        text = f"Capacidad: {arrow_data['edge'].capacity}\nOrigen: {arrow_data['edge'].origin_percentage}\nDestino: {arrow_data['edge'].destination_percentage}"
        text_id = self.canvas.create_text(text_x, text_y, text=text, fill="yellow", font=("Arial", 12, "bold"))

        # Almacenar el ID del texto en el diccionario de la flecha
        arrow_data["text_id"] = text_id
        arrow_data["edge"].canvas_text_id = text_id

    def add_input_properties_window(self, node_data):
        properties_window = tk.Toplevel()
        properties_window.title("Propiedades de Entrada")

        input_vehicles_label = Label(properties_window, text="Vehiculos Entrantes:")
        input_vehicles_label.grid(row=0, column=0)
        input_vehicles_entry = Entry(properties_window)
        input_vehicles_entry.grid(row=0, column=1)

        save_button = Button(properties_window, text="Guardar",
                             command=lambda: self.save_input_properties(node_data,
                                                                        int(input_vehicles_entry.get()),
                                                                        properties_window))
        save_button.grid(row=3, columnspan=2)

    def save_input_properties(self, node_data, input_vehicles, properties_window):
        node_data["node"].input_vehicles = int(input_vehicles)
        properties_window.destroy()

        center_x, center_y = node_data["center"]
        text_id = self.canvas.create_text(center_x, center_y, text=input_vehicles, fill="white")

        node_data["text_id"] = text_id

    def run_model(self):
        self.run_model_button.configure(state="disabled")
        self.stop_model_button.configure(state="normal")
        model = Model(
            population_size=int(self.population_size_entry.get()),
            mutations_number=int(self.mutations_number_entry.get()),
            mutations_cycle_generations=int(self.mutations_cycle_generations_entry.get()),
            end_criterion=self.end_criterion_entry.get(),
            end_criterion_value=int(self.end_criterion_value_entry.get()),
            nodes=self.nodes,
            canvas=self.canvas,
            root=self.root,
            efficiency_text=self.fitness_value_text
        )

        model.run_model()

    def stop_model(self):
        self.run_model_button.configure(state="normal")
        self.stop_model_button.configure(state="disabled")

    def save_dict_recursive(self):
        data = {
            "data_nodes_file": self.nodes,
            "data_edges_file": self.connections
        }
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
            print("Diccionario guardado en:", file_path)
        else:
            print("Guardado cancelado.")

    def load_dict_recursive(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            loaded_data = self.load_dict(file_path)
            print("Datos cargados:", loaded_data)
            self.nodes = loaded_data.get("data_nodes_file", [])
            self.connections = loaded_data.get("data_edges_file", [])
        else:
            print("Carga cancelada.")

    def load_dict(self, file_path):
        with open(file_path, 'rb') as file:
            loaded_data = pickle.load(file)
        return loaded_data
