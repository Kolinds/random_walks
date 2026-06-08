import numpy as np
import matplotlib.pyplot as plt

# Configuración de estilo visual "moderno"
plt.style.use('seaborn-v0_8-muted') 

def formula_analitica(N):
    """Implementación de la fórmula derivada."""
    """return 2**(N/2 + 3) + 2**(3 - N/2) - 16"""
    #return 16*(np.cosh((N/2)*np.log(2)) - 1)
    return None

def graficar_resultados(nombre_archivo):
    try:
        # 1. Leer datos
        with open(nombre_archivo, 'r') as f:
            datos = f.read().split()
            tiempos_medios = [float(x) for x in datos]
        
        # 2. Preparar ejes
        n_puntos = len(tiempos_medios)
        valores_N = np.arange(0, n_puntos * 2, 2)
        
        # Curva suave para la teoría
        n_fino = np.linspace(0, valores_N[-1], 200)
        tiempos_teoricos = formula_analitica(n_fino)
        
        # 3. Crear figura con mejores dimensiones
        fig, ax = plt.subplots(figsize=(11, 7))
        
        # Graficar datos (Puntos con borde para que resalten)
        ax.scatter(valores_N, tiempos_medios, color='#e74c3c', s=80, 
                   label='Simulation values', edgecolors='black', zorder=5)
        
        # Graficar línea analítica (Línea suave y elegante)
        ax.plot(n_fino, tiempos_teoricos, color='#2c3e50', linewidth=2.5, 
                label=r'Theory: $y = 16[cosh(N/2 * ln(2)) - 1]$', alpha=0.9)
        
        # --- MEJORAS VISUALES SOLICITADAS ---
        
        # Forzar eje X a intervalos de 2
        ax.set_xticks(np.arange(0, valores_N[-1] + 2, 2))
        
        # Añadir cuadrícula sutil
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Títulos y etiquetas (usando tipografía más clara)
        ax.set_title('GBT Mean Hitting Time', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Graph dimension ($N$)', fontsize=13)
        ax.set_ylabel('Mean hitting time ($y_0$)', fontsize=13)
        
        # Ajustar leyenda (ubicación óptima)
        ax.legend(frameon=True, fontsize=12, loc='upper left', shadow=True)
        
        # Eliminar bordes innecesarios (spines) para un look más limpio
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: Crea el archivo '{nombre_archivo}' con tus datos primero.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Nombre del archivo donde guardas tus datos
    graficar_resultados("mean_node_separation2.txt")