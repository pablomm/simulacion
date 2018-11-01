"""
Script para probar la inicializacion de objetivos uniformes
"""

import os
import sys

import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from objetivos import ObjetivosUniformes
from espacio import EspacioToroidalFinito


# Configuracion del espacio
size = (100.,100.)

# Configuracion de los objetivos
n_puntos = 40

# Configuracion Plot
plt.style.use("seaborn")

# Generamos el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_puntos, espacio)

# Plot
espacio.plot()
objetivos.plot()

plt.show()
