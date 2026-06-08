import numpy as np
from numba import njit, prange
import time


@njit(parallel=True)
def binary_tree_sim(depth, num_simulations, start_node, end_node):
    middle_depth = depth // 2
    first_half_node = 2**middle_depth
    last_half_node = (2**(middle_depth + 1) - 1)
    total_nodes = 2**(depth//2 + 1) + 2**(depth//2) - 2
    c_inferior = 3 * 2**(middle_depth - 1)


    hitting_times = np.empty(num_simulations, dtype=np.int32)
    depth_times = np.zeros(depth + 1, dtype=np.int32)

    for i in prange(num_simulations):
        node = start_node
        tiempo = 0


        while node != end_node:               
            if node == 1:
                if np.random.randint(2) == 0:
                    node = 2
                else:
                    node = 3

            elif node < first_half_node:
                r = np.random.randint(3)
                if r == 0:
                    node = node // 2
                elif r == 1:
                    node = 2 * node
                else:
                    node = 2 * node + 1

            elif node <= last_half_node:
                if np.random.randint(2) == 0:
                    node = node // 2
                else:
                    node = node // 2 + c_inferior

            else:
                r = np.random.randint(3)
                if r == 0:
                    node = node // 2 + c_inferior
                elif r == 1:
                    node = 2 * (node - c_inferior)
                else:
                    node = 2 * (node - c_inferior) + 1
                    
            
            inverse_node = node - (total_nodes + 1)
            for k in range(0, depth//2 + 1):
                reduced_node = node/2**k
                reduced_inode = inverse_node/2**k
                if (reduced_node >= 0.999999 and  reduced_node < 1.999999):
                    depth_times[k] += 1
                    break
                elif (reduced_inode >= -1.999999 and  reduced_inode < -0.999999):
                    depth_times[depth - k] += 1
                    break

            tiempo += 1


        hitting_times[i] = tiempo
    return hitting_times, depth_times




depth = 6
n_simulaciones = 100000

print(f"Ejecutando {n_simulaciones} simulaciones a máxima velocidad...")
inicio = time.time()

total_nodes = 2**(depth//2 + 1) + 2**(depth//2) - 2
resultados, depth_times = binary_tree_sim(depth, n_simulaciones, 1, total_nodes)


fin = time.time()
print(f"Simulaciones terminadas en {fin - inicio:.2f} segundos.")

np.savetxt("hitting_times.txt", resultados, fmt='%d', newline=' ')
np.savetxt("depth_times.txt", depth_times, fmt='%d', newline=' ')
print("Datos guardados en 'hitting_times.txt', 'depth_times.txt'.")