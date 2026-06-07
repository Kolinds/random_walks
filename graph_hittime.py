import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 0. CONFIGURACIÓN DEL BOCETO (SIMÉTRICO)
# ==========================================
PROFUNDIDAD_BOCETO = 10

def dibujar_arbol_rombo_boceto(ax_inset, depth):
    """Dibuja un boceto minimalista de un Árbol Rombo Simétrico."""
    ax_inset.set_axis_off()
    
    left_nodes = {}
    right_nodes = {}
    offset = 2 * depth + 1
    
    # Construir el árbol izquierdo (Entrada)
    for d in range(depth + 1):
        ys = [0.0] if d == 0 else np.linspace(1, -1, 2**d)
        for i, y in enumerate(ys):
            left_nodes[(d, i)] = (d, y)
            if d > 0:
                px, py = left_nodes[(d-1, i // 2)]
                ax_inset.plot([px, d], [py, y], color='#00e5ff', alpha=0.7, lw=1.5)
                
    # Construir el árbol derecho (Salida)
    for d in range(depth + 1):
        ys = [0.0] if d == 0 else np.linspace(1, -1, 2**d)
        for i, y in enumerate(ys):
            right_nodes[(d, i)] = (offset - d, y)
            if d > 0:
                px, py = right_nodes[(d-1, i // 2)]
                ax_inset.plot([px, offset - d], [py, y], color='#ff0055', alpha=0.7, lw=1.5)
                
    # --- MODIFICACIÓN: "Pegar" los árboles de forma simétrica ---
    for i in range(2**depth):
        lx, ly = left_nodes[(depth, i)]
        rx, ry = right_nodes[(depth, i)]
        # Conexión directa y simétrica (hoja i con hoja i)
        ax_inset.plot([lx, rx], [ly, ry], color='#ffbb00', alpha=0.6, lw=1.5, linestyle='--')
        
    # Dibujar los vértices opuestos (Entrada y Salida)
    ax_inset.scatter([0], [0], color='white', s=50, zorder=5) # Raíz inicio
    ax_inset.scatter([offset], [0], color='white', s=50, zorder=5) # Raíz destino

# ==========================================
# 1. LEER LOS DATOS (HIT PASADO)
# ==========================================
nombre_archivo = "hitting_times.txt"

try:
    with open(nombre_archivo, "r") as archivo:
        tiempos_de_escape = [int(float(x)) for x in archivo.read().split()]
except FileNotFoundError:
    print(f"Error Crítico: No se encontró el archivo '{nombre_archivo}'.")
    print("Asegúrate de ejecutar primero 'simulacion.py' para generar los datos.")
    exit()

if not tiempos_de_escape:
    print(f"Error: El archivo '{nombre_archivo}' está vacío.")
    exit()

# ==========================================
# 2. CALCULAR ESTADÍSTICAS
# ==========================================
total_intentos = len(tiempos_de_escape)
promedio = np.mean(tiempos_de_escape)
mediana = np.median(tiempos_de_escape)
desviacion_estandar = np.std(tiempos_de_escape)  # <--- NEW: Calculate Standard Deviation

# ==========================================
# 3. DIBUJAR EL HISTOGRAMA
# ==========================================
fig, ax = plt.subplots(figsize=(12, 8))
plt.style.use('dark_background')
fig.patch.set_facecolor('#0d1117') 
ax.set_facecolor('#0d1117')

pesos = np.ones_like(tiempos_de_escape) / total_intentos

plt.hist(tiempos_de_escape, bins=50, weights=pesos, color='#00e5ff', edgecolor='black', alpha=0.8)

# <--- MODIFIED: Update Mean label to include ± SD
plt.axvline(promedio, color='#ff0055', linestyle='dashed', linewidth=2.5, 
            label=f'Mean: {promedio:.0f} ± {desviacion_estandar:.0f} steps')

# <--- NEW: Plot bounds for +1 and -1 Standard Deviation
plt.axvline(promedio - desviacion_estandar, color='#ff0055', linestyle=':', linewidth=1.5, alpha=0.6,
            label='1 Standard deviation')
plt.axvline(promedio + desviacion_estandar, color='#ff0055', linestyle=':', linewidth=1.5, alpha=0.6)

plt.axvline(mediana, color='#ffbb00', linestyle='dotted', linewidth=2.5, 
            label=f'Median: {mediana:.0f} steps')

# Textos y Etiquetas
plt.title(f'N = {PROFUNDIDAD_BOCETO}\n {total_intentos:,} Independent Simulations'.replace(",", "."), 
          fontsize=16, fontweight='bold', color='white', pad=25)
plt.xlabel('Total time steps', 
           fontsize=14, fontweight='bold', color='white', labelpad=15)
plt.ylabel('Relative frequency', 
           fontsize=14, fontweight='bold', color='white', labelpad=15)

plt.legend(fontsize=12, loc='upper right')
plt.tick_params(axis='both', which='major', labelsize=12, labelcolor='white')
plt.grid(True, axis='y', alpha=0.2, linestyle='--', color='white')

# ==========================================
# 4. INSERTAR EL BOCETO DEL ÁRBOL ROMBO
# ==========================================
ax_boceto = ax.inset_axes([0.35, 0.1, 0.57, 0.75])
dibujar_arbol_rombo_boceto(ax_boceto, PROFUNDIDAD_BOCETO//2)

plt.savefig(f'./hitting_graphs/depth{PROFUNDIDAD_BOCETO}.png')

plt.tight_layout()
plt.show()