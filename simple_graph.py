import numpy as np
import matplotlib.pyplot as plt

# Configuración de estilo visual "moderno"
plt.style.use('seaborn-v0_8-muted') 

def graficar_resultados(nombre_archivo):
    try:
        # 1. Leer datos (separando por líneas)
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines()
            
            if len(lineas) < 2:
                raise ValueError("El archivo debe contener al menos dos líneas: la primera para medias y la segunda para incertidumbres.")
            
            # Primera fila: valores medios
            tiempos_medios = [float(x) for x in lineas[0].split()]
            
            # Segunda fila: incertidumbres
            incertidumbres = [float(x) for x in lineas[1].split()]
            
        # Comprobar que hay el mismo número de medias que de incertidumbres
        if len(tiempos_medios) != len(incertidumbres):
            raise ValueError("El número de valores medios no coincide con el número de incertidumbres.")
        
        # 2. Preparar ejes (CAMBIO: Separación de 1 en 1)
        n_puntos = len(tiempos_medios)
        # Asumimos que la separación empieza en 0 y avanza de 1 en 1.
        # (Si empieza en 1, cambia esto a: np.arange(1, n_puntos + 1, 1))
        valores_N = np.arange(0, n_puntos, 1)
        
        # 3. Crear figura con mejores dimensiones
        fig, ax = plt.subplots(figsize=(11, 7))
        
        # Graficar datos con BARRAS DE ERROR
        ax.errorbar(valores_N, tiempos_medios, yerr=incertidumbres, fmt='o', 
                    color='#e74c3c', markersize=9, markeredgecolor='black', 
                    ecolor='black', elinewidth=1.5, capsize=4, capthick=1.5,
                    label='Simulation values', zorder=5)
        
        
        # --- MEJORAS VISUALES ---
        
        # Forzar eje X a intervalos de 1 para que coincida con tus datos (CAMBIO)
        ax.set_xticks(np.arange(0, valores_N[-1] + 1, 1))
        
        # Añadir cuadrícula sutil
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Títulos y etiquetas
        ax.set_title('GBT Mean Hitting Time', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Node separation ($n$)', fontsize=13)
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
    except ValueError as ve:
        print(f"Error con los datos del archivo: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Nombre del archivo donde guardas tus datos
    graficar_resultados("mean_node_separation2.txt")