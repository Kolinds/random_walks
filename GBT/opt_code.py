import numpy as np
from numba import njit, prange

@njit(parallel=True)
def binary_tree_sim(depth, num_simulations, start_node, end_node):
    middle_depth = depth // 2
    first_half_node = 2**middle_depth
    last_half_node = 2**(middle_depth + 1) - 1
    total_nodes = 2**(depth // 2 + 1) + 2**(depth // 2) - 2
    c_inferior = 3 * 2**(middle_depth - 1)

    hitting_time_array = np.empty(num_simulations, dtype=np.int64)

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

            elif first_half_node <= node <= last_half_node:
                if np.random.randint(2) == 0:
                    node = node // 2
                else:
                    node = node // 2 + c_inferior

            elif node == total_nodes:
                if np.random.randint(2) == 0:
                    node = total_nodes - 1
                else:
                    node = total_nodes - 2

            else:
                r = np.random.randint(3)
                if r == 0:
                    node = node // 2 + c_inferior
                elif r == 1:
                    node = 2 * (node - c_inferior)
                else:
                    node = 2 * (node - c_inferior) + 1
                    
            tiempo += 1
        hitting_time_array[i] = tiempo
    return hitting_time_array


final_depth = 6
n_simulaciones = 1000000
mean_times = np.empty(final_depth//2 + 1, dtype=np.float64)
std_times = np.empty(final_depth//2 + 1, dtype=np.float64)  # NUEVO: Array para la incertidumbre (desviación estándar)


if __name__ == "__main__":
    for depth in range(2, final_depth + 1, 2):
        total_nodes = 2**(depth // 2 + 1) + 2**(depth // 2) - 2
        resultados = binary_tree_sim(depth, n_simulaciones, 1, total_nodes)
        
        # Calculamos la media y la desviación estándar para esta profundidad
        mean_times[depth//2] = resultados.mean()
        std_times[depth//2] = resultados.std() / np.sqrt(n_simulaciones)

    # Guardamos ambos arrays en sus respectivos archivos .txt
    np.savetxt("mean_times.txt", mean_times, fmt='%0.4f', newline=' ')
    np.savetxt("incertidumbre_times.txt", std_times, fmt='%0.4f', newline=' ') # NUEVO: Guardado del archivo
    
    print("Datos guardados en 'mean_times.txt' e 'incertidumbre_times.txt'.")