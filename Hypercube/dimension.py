# Program that plots the mean hitting time of a random walk in a hypercube as a function of dimension, given the file dimension.txt

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

archivo = 'dimension.txt' 
datos = np.loadtxt(archivo)

N_discreto = datos[:, 0]     
sim_mean = datos[:, 1]        
sim_error = datos[:, 2]      
teo_mean = datos[:, 3]        

# Interpolation
N_continuo = np.linspace(N_discreto.min(), N_discreto.max(), 500)
spline = make_interp_spline(N_discreto, teo_mean, k=3)
teo_continuo = spline(N_continuo)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


mascara_linea_baja = N_continuo <= 6
mascara_puntos_baja = N_discreto <= 6

ax1.plot(N_continuo[mascara_linea_baja], teo_continuo[mascara_linea_baja], 
         color='#34495e', label='Theory', zorder=1)

ax1.errorbar(N_discreto[mascara_puntos_baja], sim_mean[mascara_puntos_baja], 
             yerr=sim_error[mascara_puntos_baja], 
             fmt='o', markerfacecolor='#e74c3c', markeredgecolor='black', 
             color='black', ecolor='black', capsize=4, label='Simulation values', zorder=2)

ax1.set_title('Hypercube Hitting Time (Low Dimensions)', pad=15)
ax1.set_xlabel('Graph dimension (N)')
ax1.set_ylabel(r'Mean hitting time ($\tau(v_0)$)')

ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend()

ax2.plot(N_continuo, teo_continuo, color='#34495e', label='Theory', zorder=1)

ax2.errorbar(N_discreto, sim_mean, yerr=sim_error, 
             fmt='o', markerfacecolor='#e74c3c', markeredgecolor='black', 
             color='black', ecolor='black', capsize=4, label='Simulation values', zorder=2)

ax2.set_title(r'$\log_2$ Hypercube Mean Hitting Time', pad=15)
ax2.set_xlabel('Graph dimension (N)')
ax2.set_ylabel(r'$\log_2$ Mean hitting time ($\tau(v_0)$)')


ax2.set_xticks(np.arange(0, 21, 2))

ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend()
ax2.set_yscale('log', base=2) # To plot the high dimension graph in log_2 scale

plt.tight_layout()
plt.show()