

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import Trayectoria, Explotados
from simulador import LevyFlight


# Configuracion del espacio
n_objetivos = 100
size = (100.,100.)
r = 3 # Radio de explotacion
t = 500 # Tiempo de simulacion
a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = LevyFlight(r, a, b, loc, scale, maximo, minimo, posicion=inicial)
modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())

modelo.simular(t)

# Dibujamos el resultado de la simulacion
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()

plt.show()
