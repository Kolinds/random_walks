import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN GENERAL ---
N = 12  # Cambia esto según la dimensión que estés graficando
SIMULACIONES = "1.000.000"

# 1. Cargar los datos de los archivos

tiempos = np.loadtxt(f"tiempos_N={N}.txt")
media, desv = np.loadtxt(f"estadistica_N={N}.txt")


# Calcular la mediana directamente desde los datos cargados
mediana = np.median(tiempos)

# 2. Configurar el estilo oscuro de Matplotlib
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(9, 6), dpi=120)

# Ajustar el fondo del recuadro exterior e interior a un gris muy oscuro/negro
fig.patch.set_facecolor("#0d0d11")
ax.set_facecolor("#0d0d11")

# 3. Dibujar el histograma (Frecuencia Relativa)
# Usamos 'weights' para que el eje Y represente la proporción/frecuencia relativa (0 a 1)
pesos = np.ones(len(tiempos)) / len(tiempos)

# Puedes ajustar el número de 'bins' (barras) según cómo quieras que se vea de suavizado
counts, bins, patches = ax.hist(
    tiempos,
    bins=60,
    weights=pesos,
    color="#00cbd6",  # Color cian idéntico al de la imagen
    edgecolor="#0d0d11",  # Borde sutil para separar las barras
    alpha=0.9,
    rwidth=0.9,
)

# 4. Añadir las líneas estadísticas verticales
# Línea de la Media (Línea discontinua rosa/magenta)
ax.axvline(
    media,
    color="#ff1a75",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {media:.1f} ± {desv:.1f} steps",
)

# Línea de 1 Desviación Estándar (Línea punteada fina)
ax.axvline(
    media + desv,
    color="#ff1a75",
    linestyle=":",
    linewidth=1.2,
    label="1 Standard Deviation",
)
if media - desv > 0:
    ax.axvline(media - desv, color="#ff1a75", linestyle=":", linewidth=1.2)

# Línea de la Mediana (Línea punteada naranja/amarilla)
ax.axvline(
    mediana,
    color="#ffb703",
    linestyle=":",
    linewidth=2,
    label=f"Median: {mediana:.0f} steps",
)

# 5. Personalización de ejes, títulos y rejilla
ax.set_title(
    f"N = {N}\n{SIMULACIONES} Independent Simulations",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
ax.set_xlabel("Total time steps", fontsize=11, labelpad=10, color="#cfcfd4")
ax.set_ylabel("Relative frequency", fontsize=11, labelpad=10, color="#cfcfd4")

# Rejilla horizontal tenue
ax.grid(axis="y", linestyle="--", alpha=0.15, color="white")
ax.set_axisbelow(True)  # Pasa la rejilla por detrás de las barras

# Quitar las líneas del marco que no aportan
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#33333b")
ax.spines["bottom"].set_color("#33333b")
ax.tick_params(colors="#cfcfd4")

# 6. Configurar la Leyenda (Cuadro flotante)
legend = ax.legend(
    loc="upper right",
    facecolor="#16161a",
    edgecolor="#2a2a35",
    fontsize=10,
    framealpha=0.9,
)
plt.setp(legend.get_texts(), color="white")

# Optimizar espacio y mostrar/guardar
plt.tight_layout()
plt.show()