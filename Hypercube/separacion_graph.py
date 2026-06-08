import numpy as np
import matplotlib.pyplot as plt

archivo_datos = "separacion.txt"

datos = np.loadtxt(archivo_datos)
s_sim = datos[:, 0]
tiempo_sim = datos[:, 1]

N = int(np.max(s_sim))
separacion = N - s_sim

indices_ordenados = np.argsort(separacion)
separacion_ordenada = separacion[indices_ordenados]
tiempo_ordenado = tiempo_sim[indices_ordenados]

plt.figure(figsize=(10, 6), dpi=100)
    
plt.plot(separacion_ordenada, tiempo_ordenado, 
             marker='o', 
             linestyle='-', 
             linewidth=2, 
             color='#1f77b4',     
             label='Computational simulation data')

plt.title(f'Mean Hitting Time vs Node Separation (Hypercube $N={14}$)', fontsize=14, pad=15)
plt.xlabel('Node Separation (S)', fontsize=12)
plt.ylabel(r'Mean Hitting Time ($\tau$)', fontsize=12)

plt.xticks(np.arange(0, N + 1, 1 if N <= 15 else 2))
    
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)

plt.tight_layout()

    
plt.show()
