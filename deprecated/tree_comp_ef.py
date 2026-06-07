import numpy as np
import random

class binary_tree:
    def __init__(self, depth):
        self.depth = depth
        self.total_time = 0
        self.finish = False

        self.first_half_node = 2**(self.depth/2)
        self.last_half_node = (2**(self.depth/2 + 1) - 1)
        self.total_nodes = 2**(self.depth/2 + 1) + 2**(self.depth/2) - 2
        
        self.c_inferior = 3 * 2**(self.depth/2 - 1)
        

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

        elif (actual_node == self.total_nodes):
            node_outcomes = (self.total_nodes - 1, self.total_nodes - 2)
        
        elif (actual_node > self.last_half_node):
            node_outcomes = (actual_node // 2 + self.c_inferior, 2*(actual_node - self.c_inferior), 2*(actual_node - self.c_inferior) + 1)   


        new_node = random.choice(node_outcomes)
        self.node = new_node

        self.total_time += 1

        if (self.node == self.end_node):
            self.finish = True


#MAIN LOOP


"""
tree = binary_tree(2)
with open("hitting_times.txt", "w") as f:
    for num_simulations in range(0, 100000):
        tree.set_extreme_points(1, tree.total_nodes)
        while (not tree.finish):
            tree.random_step()
    
        f.write(f"{int(tree.total_time)} ")
"""

final_depth = 4
n_simulaciones = 1000
mean_times = np.empty(final_depth//2, dtype=np.float64)



for depth in range(2, final_depth + 1, 2):
    tree = binary_tree(depth)
    total_nodes = 2**(depth // 2 + 1) + 2**depth // 2 - 2
    for num_simulations in range(0, 100000):
        tree.set_extreme_points(1, tree.total_nodes)
        while (not tree.finish):
            tree.random_step()
    resultados = binary_tree_sim(depth, n_simulaciones, 1, total_nodes)
    mean_times[depth//2 - 1] = resultados.mean()

np.savetxt("mean_times.txt", mean_times, fmt='%d', newline=' ')

