import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# ==============================================================================
# 1. GENERACIÓN DE DATOS DE PRUEBA (IGNORA ESTO SI YA TIENES camino.txt)
# ==============================================================================
# Esto es solo para que el código funcione directamente si no tienes el archivo.
import random
try:
    with open("camino.txt", "r") as f: f.read()
except FileNotFoundError:
    print("Generando camino.txt de prueba...")
    # Generamos un camino aleatorio simple N=10 Raíz a Salida (aprox)
    test_path = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 1278, 1279, 1280] # N=10 Raiz a Salida directa
    with open("camino.txt", "w") as f:
        for node in test_path: f.write(f"{node} ")
# ==============================================================================

# 1. Leer los datos
with open("camino.txt", "r") as f:
    # Convertimos a float primero por seguridad, luego a int
    data = f.read().split()
    if not data:
        print("Error: camino.txt está vacío.")
        exit()
    path = [int(float(x)) for x in data]

# 2. Reconstruir la estructura del grafo
N = 10  # Profundidad (Debe ser par)
d = N // 2
first_half_node = int(2**d)
total_nodes = int(2**(d + 1) + 2**d - 2)
c_inferior = int(3 * 2**(d - 1))

G = nx.Graph()

for i in range(1, total_nodes):
    if i < first_half_node:
        G.add_edge(i, 2*i)
        G.add_edge(i, 2*i + 1)
    else:
        G.add_edge(i, i // 2 + c_inferior)

# 3. Diseño Visual (Layout)
capas = nx.single_source_shortest_path_length(G, 1)
nx.set_node_attributes(G, capas, 'layer')
pos_horizontal = nx.multipartite_layout(G, subset_key='layer')
pos = {nodo: (coords[0], coords[1]) for nodo, coords in pos_horizontal.items()}
# --- ESCALADO DINÁMICO ---
tamaño_nodo = max(5, 3000 / total_nodes)
tamaño_caminante = tamaño_nodo * 6
mostrar_etiquetas = N <= 6 

# ==============================================================================
# 4. CONFIGURAR VISUALIZACIÓN DE ALTO CONTRASTE
# ==============================================================================
# Definimos figsize y frameon=False ayuda a quitar bordes externos
fig, ax = plt.subplots(figsize=(12, 12), frameon=False)

# --- QUITAR FONDO ---
# Establecemos el fondo de la figura y del eje a NEGRO PURO para máximo contraste
fig.patch.set_facecolor('#000000') 
ax.set_facecolor('#000000')

# Eliminamos por completo los ejes visibles y recuadros
ax.axis('off')
# Forzamos la eliminación de cualquier 'espina' (borde) remanente
for spine in ax.spines.values():
    spine.set_visible(False)

print("Dibujando esqueleto del grafo (Alto Contraste)...")

# --- DIBUJAR GRAFO (MÁXIMO CONTRASTE) ---
# Usamos alpha=1.0 (opacidad total) para colores neón sólidos contra negro
nx.draw(G, pos, ax=ax, with_labels=mostrar_etiquetas, 
        node_color='#b026ff',   # Morado Neón Sólido
        edge_color='#00e5ff',   # Cyan Neón Sólido
        alpha=1.0,              # <--- OPACIDAD TOTAL para contraste
        width=1.2,              # Un poco más grueso para que destaque
        node_size=tamaño_nodo, 
        edgecolors='#ffffff',   # Añadimos anillo blanco fino a nodos para que 'brillen'
        linewidths=0.5,
        font_weight='bold', 
        font_size=10,
        font_color='white')     # Etiquetas en blanco puro

# --- DIBUJAR CAMINANTE ---
# Magenta brillante contra negro puro es contraste extremo
caminante_plot = ax.scatter([], [], c='#ff0055', s=tamaño_caminante, 
                            zorder=20,          # Encima de todo
                            edgecolors='white', # Borde blanco para pop extra
                            linewidths=1.5)

# Título en blanco puro
title_text = ax.set_title("", fontsize=18, color='white', pad=20, fontweight='bold')

# 5. Funciones de Animación
def init():
    caminante_plot.set_offsets(np.empty((0, 2)))
    title_text.set_text("")
    return caminante_plot, title_text

def update(frame):
    nodo_actual = path[frame]
    x, y = pos[nodo_actual]
    caminante_plot.set_offsets([[x, y]]) 
    title_text.set_text(f"Caminante Aleatorio | Paso Reales: {frame} | Nodo: {nodo_actual}")
    return caminante_plot, title_text

# --- CONFIGURAR VELOCIDAD ---
SALTOS_POR_FOTOGRAMA = 1 # Pon 50 para N grandes
frames_a_dibujar = range(0, len(path), SALTOS_POR_FOTOGRAMA)

# Crear la animación
ani = FuncAnimation(fig, update, frames=frames_a_dibujar, 
                    init_func=init, interval=50, blit=True, repeat=False)

plt.tight_layout(pad=0) # pad=0 quita márgenes blancos

# ==============================================================================
# OPCIONES PARA GUARDAR O MOSTRAR
# ==============================================================================

# OPCIÓN A: MOSTRAR EN PANTALLA
print("Mostrando animación...")
#plt.show()

# OPCIÓN B: GUARDAR (Descomenta estas líneas y comenta plt.show() si quieres guardar)
# print("Guardando animación de alto contraste como GIF...")
#  fps=30 para fluidez, writer='pillow' para GIFs
ani.save('caminante_alto_contraste.mp4', writer='ffmpeg', fps=5, dpi=150)
# print("¡Guardado!")