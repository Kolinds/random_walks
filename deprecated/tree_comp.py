import numpy


class binary_tree:
    def __init__(self, depth):
        self.depth = depth
        self.graph ={}
    
    def create_branch(self, prefix):
        for node_number in range (1, 2**(self.depth/2 + 1) - 1):
            node_id = f"{prefix}_{node_number}"
            self.graph[node_id] = []
            
            if (node_number > 1):
                parent_node = node_number // 2 
                self.graph[node_id].append(f"{prefix}_{parent_node}")
        
            if 