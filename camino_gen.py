import numpy as np
import random

class binary_tree:
    def __init__(self, depth):
        # Depth must be an even number (e.g., 4, 6, 8)
        self.depth = depth
        self.total_time = 0
        self.finish = False

        # Using int() or // to ensure all node IDs remain integers
        self.first_half_node = int(2**(self.depth // 2))
        self.last_half_node = int(2**(self.depth // 2 + 1) - 1)
        self.total_nodes = int(2**(self.depth // 2 + 1) + 2**(self.depth // 2) - 2)
        
        self.c_inferior = int(3 * 2**(self.depth // 2 - 1))
        
    def set_extreme_points(self, start, end):
        self.total_time = 0
        self.finish = False
        self.node = start
        self.end_node = end
        
    def random_step(self):
        actual_node = self.node
        
        if (actual_node == 1):
            node_outcomes = (2, 3)

        elif (actual_node < self.first_half_node):
            node_outcomes = (actual_node // 2, 2*actual_node, 2*actual_node + 1)

        elif (self.first_half_node <= actual_node <= self.last_half_node):
            node_outcomes = (actual_node // 2, actual_node // 2 + self.c_inferior)
        
        # MOVED UP: Check for exit node before checking for bottom internal nodes
        elif (actual_node == self.total_nodes):
            node_outcomes = (self.total_nodes - 1, self.total_nodes - 2)

        elif (actual_node > self.last_half_node):
            node_outcomes = (actual_node // 2 + self.c_inferior, 2*(actual_node - self.c_inferior), 2*(actual_node - self.c_inferior) + 1)


        new_node = random.choice(node_outcomes)
        self.node = new_node
        self.total_time += 1

        if (self.node == self.end_node):
            self.finish = True



# MAIN LOOP de tu simulación original
tree = binary_tree(6) 
tree.set_extreme_points(1, tree.total_nodes)

# Abrimos el archivo en modo escritura ("w")
with open("camino.txt", "w") as f:
    f.write(f"{tree.node} ") # Guardamos el nodo inicial
    while (not tree.finish):
        tree.random_step()
        f.write(f"{tree.node} ") # Guardamos cada paso separado por un espacio