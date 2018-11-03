"""
Script para probar la inicializacion de objetivos agrupados
"""

import os
import sys

import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito

# Configuracion del espacio
size = (100.,100.)

# Configuracion de los objetivos
n_puntos_grupo = 10
n_grupos = 4
std_grupos = 4 # Desviacion estandar de los grupos

# Configuracion Plot
plt.style.use("seaborn")

# Generamos el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos)

# Plot
espacio.plot()
objetivos.plot()
objetivos.plot_grupos()

# Inicializamos los grupos en vez de aleatorios
n_grupos_ejemplo = 4
grupos = [[25, 25] ,[25, 75], [75, 25], [75, 75]]


plt.figure()

objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos_ejemplo,
                               std_grupos, grupos=grupos)


espacio.plot()
objetivos.plot()
objetivos.plot_grupos()



plt.show()
