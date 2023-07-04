from tkinter import Canvas

class LED:
    def __init__(self, root, name, state=True):
        self.state = state
        self.canvas = Canvas(root, width=20, height=20, bg='black')
        self.canvas.pack()
        self.name = name

    def update_state(self):
        color = 'red' if self.state else 'green'
        self.canvas.configure(bg=color)
        

class DigitalCircuitSimulator:
    def __init__(self, root):
        self.root = root
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def update_circuit(self):
        for component in self.components:
            component.update_state()
