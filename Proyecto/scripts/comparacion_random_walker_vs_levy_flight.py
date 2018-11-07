

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import Trayectoria, Explotados
from simulador import RandomWalker, LevyFlight
from simulador import Distancias

n_simulaciones = 20

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = 500 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)
#Organismo LevyFlight
a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = RandomWalker(r, std=std, posicion=inicial)
organismo2 = LevyFlight(r, a, b, loc, scale, maximo, minimo, posicion=inicial)
modelo.add_organismo(organismo)
modelo.add_organismo(organismo2)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(Explotados())
modelo.add_estadistica(Distancias())

modelo.simular(t, n_simulaciones=n_simulaciones)

# Dibujamos el resultado de la simulacion
plt.figure()
organismo.plot_distancias(param="random_walker")
organismo2.plot_distancias(param="levy_flight")

plt.figure()
organismo.plot_numero_explotados(modelo, param="random_walker")
organismo2.plot_numero_explotados(modelo, param="levy_flight")

plt.show()
