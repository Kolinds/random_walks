import numpy as np
import matplotlib.pyplot as plt

# Configuración de estilo visual "moderno"
plt.style.use('seaborn-v0_8-muted') 

def graficar_resultados(nombre_archivo):
    try:
        # 1. Leer datos en bruto del archivo
        with open(nombre_archivo, 'r') as f:
            datos = f.read().split()
            y_brutos = np.array([float(val) for val in datos])
        
        # --- NUEVO: CONVERSIÓN A FRECUENCIA RELATIVA ---
        # Dividimos cada valor por la suma total para que el área/suma sea 1
        suma_total = np.sum(y_brutos)
        y_datos = y_brutos / suma_total
        
        # 2. Preparar el dominio en el eje X (0, 1, ..., N-1)
        N = len(y_datos)
        x_datos = np.arange(0, N)
        
        # 3. Calcular la media (\mu) y la incertidumbre (\sigma)
        # Como y_datos ahora es frecuencia relativa (suma 1), 
        # las fórmulas actúan como la Esperanza Matemática estándar.
        suma_y = np.sum(y_datos) # Esto ahora vale 1.0
        mu = np.sum(x_datos * y_datos) / suma_y
        sigma = np.sqrt(np.sum(y_datos * (x_datos - mu)**2) / suma_y)
        
        # 4. Crear rango fino (mantenido de tu código original por si lo necesitas luego)
        x_fino = np.linspace(0, N - 1, 200)
  
        # 5. Crear figura con mejores dimensiones
        fig, ax = plt.subplots(figsize=(11, 7))
        
        # Graficar datos (Puntos concretos usando la frecuencia relativa)
        ax.scatter(x_datos, y_datos, color='#e74c3c', s=80, 
                   label='Simulation data', edgecolors='black', zorder=5)
        
        # --- MEJORAS VISUALES ---
        
        # Forzar eje X a números enteros (si N es muy grande, ajustamos el paso para no saturar)
        paso_x = max(1, N // 15)
        ax.set_xticks(np.arange(0, N, paso_x))
        
        # Añadir cuadrícula sutil
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Títulos y etiquetas actualizadas
        ax.set_title('Time steps accumulated per depth', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Depth ($k$)', fontsize=13)
        ax.set_ylabel('Relative frequency', fontsize=13) # <--- Eje Y actualizado
        
        # Ajustar leyenda
        ax.legend(frameon=True, fontsize=12, loc='upper right', shadow=True)
        
        # Eliminar bordes innecesarios (spines)
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
    graficar_resultados("depth_times.txt")