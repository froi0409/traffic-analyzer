import tkinter as tk
from tkinter import Canvas, Button

class CircleGraph:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()
        self.nodes = []
        self.connections = []

        self.create_circle_button = Button(root, text="Crear Círculo", command=self.create_circle_on_click)
        self.create_circle_button.pack()

        self.canvas.bind("<Button-1>", self.create_circle)

        self.canvas.bind("<Button-3>", self.connect_circles)

    def create_circle_on_click(self):
        # No necesitas hacer nada aquí, ya que el círculo se crea al hacer clic en el lienzo
        pass

    def create_circle(self, event):
        x, y = event.x, event.y
        circle = self.canvas.create_oval(x-10, y-10, x+10, y+10)
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
                    self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1], arrow=tk.LAST)
                    self.connections = []

root = tk.Tk()
app = CircleGraph(root)
root.mainloop()
