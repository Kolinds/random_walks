import numpy as np
from numba import njit, prange
import time

@njit
def obtener_profundidad(node, middle_depth, last_half_node):
    """Calcula la profundidad de cualquier nodo en el grafo."""
    # Lado izquierdo del árbol (incluyendo el medio)
    if node <= last_half_node:
        temp_node = node
        current_depth = 0
        while temp_node > 1:
            temp_node = temp_node // 2
            current_depth += 1
        return current_depth
        
    # Lado derecho del árbol
    else:
        current_depth = middle_depth
        nodes_in_level = 2**(middle_depth - 1)
        level_start = 2**(middle_depth + 1)
        
        while node >= level_start + nodes_in_level:
            level_start += nodes_in_level
            nodes_in_level //= 2
            current_depth += 1
            
        return current_depth + 1

@njit(parallel=True)
def binary_tree_sim(depth, num_simulations, start_node, end_nodes):
    middle_depth = depth // 2
    first_half_node = 2**middle_depth
    last_half_node = (2**(middle_depth + 1) - 1)
    
    # Constante para los saltos
    c_inferior = 3 * 2**(middle_depth - 1)

    hitting_times = np.empty(num_simulations, dtype=np.int32)
    
    # Matriz 2D de tamaño (num_simulations, depth + 1)
    all_depth_times = np.zeros((num_simulations, depth + 1), dtype=np.int32)

    for i in prange(num_simulations):
        node = start_node
        tiempo = 0

        # 1. Contabilizar correctamente la profundidad del nodo inicial
        prof_inicial = obtener_profundidad(node, middle_depth, last_half_node)
        if 0 <= prof_inicial <= depth:
            all_depth_times[i, prof_inicial] += 1

        # El operador 'not in' funciona perfectamente en Numba si le pasamos un array de numpy
        while node not in end_nodes:              
            # --- Lógica de Movimiento del Caminante ---
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
                    
            # --- Lógica de Profundidad (Usando la función auxiliar) ---
            current_depth = obtener_profundidad(node, middle_depth, last_half_node)
                
            # Registrar el paso de tiempo
            if 0 <= current_depth <= depth:
                all_depth_times[i, current_depth] += 1

            tiempo += 1

        hitting_times[i] = tiempo
        
    # Colapsar de forma segura
    final_depth_times = np.zeros(depth + 1, dtype=np.int32)
    for i in range(num_simulations):
        for j in range(depth + 1):
            final_depth_times[j] += all_depth_times[i, j]

    return hitting_times, final_depth_times

# --- Ejecución ---
if __name__ == "__main__":
    depth = 10
    n_simulaciones = 100000

    print(f"Ejecutando {n_simulaciones} simulaciones...")
    inicio = time.time()

    # Cálculo del nodo final real del grafo
    total_nodes = 2**(depth//2 + 1) + 2**(depth//2) - 2
    first_half_node = 2**(depth//2)

    # 2. Nodo inicial (Ahora puedes poner el que quieras)
    nodo_inicial = total_nodes 
    
    # 3. CONVERTIR LA LISTA A UN ARRAY DE NUMPY (Crucial para que Numba compile bien el 'not in')
    end_nodes_array = np.array([1], dtype=np.int32)
    
    resultados, depth_times = binary_tree_sim(depth, n_simulaciones, nodo_inicial, end_nodes_array)

    fin = time.time()
    print(f"Simulaciones terminadas en {fin - inicio:.2f} segundos.")

    np.savetxt("hitting_times.txt", resultados, fmt='%d', newline=' ')
    np.savetxt("depth_times.txt", depth_times, fmt='%d', newline=' ')
    print(f"Los conteos por profundidad fueron: {depth_times}")
    print("Datos guardados.")