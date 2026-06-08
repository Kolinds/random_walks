# Program that plots the relative frequency of time steps accumulated per depth given the file tiempo_acumulado.txt or tiempo_acumulado_mitad.txt

import numpy as np
import matplotlib.pyplot as plt

# CHANGE NAME ACCORDING TO THE FILE YOU WANT TO PLOT
nombre_archivo = "tiempo_acumulado_mitad_N=10.txt"

tiempos_absolutos = np.loadtxt(nombre_archivo)

tiempo_total = np.sum(tiempos_absolutos)
frecuencia_relativa = tiempos_absolutos / tiempo_total

profundidades = np.arange(len(tiempos_absolutos))

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(profundidades, frecuencia_relativa, marker='o', linestyle='', 
        markerfacecolor='#ea4335', markeredgecolor='black', markersize=8, 
        label='Simulation data')

ax.set_title("Time steps accumulated per depth", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Depth ($k$)", fontsize=12)
ax.set_ylabel("Relative frequency", fontsize=12)

ax.grid(True, linestyle='--', alpha=0.5)

ax.legend(loc='upper right', shadow=True, fancybox=True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.spines['left'].set_color('gray')
ax.spines['bottom'].set_color('gray')

plt.xticks(profundidades)

# Ajustar márgenes y mostrar
plt.tight_layout()
plt.show()