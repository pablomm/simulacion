"""
Script para probar la inicializacion de objetivos uniformes
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import Explotados, Distancias, Trayectoria

n_simulaciones = 1

# Configuracion de los objetivos
n_objetivos = 100
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1. # Desviacion estandar del movimiento browniano
t = 500 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)
# Organismo LevyFlight
a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

densidad = n_objetivos/(size[0]*size[1])

# Configuracion Plot
plt.style.use("seaborn")

# Generamos el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)

# RandomWalker Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                               std=std, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=False, verbose=1)
# Plot
plt.figure()
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()
plt.title("Random Walker Activo")
organismo.plot()

#LevyFlight Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                             minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=False, verbose=1)
# Plot
plt.figure()
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()
plt.title("Levy Flight Activo")
organismo.plot()

#Organismo2Etapas (random walker + levy flight pasivo)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             mu=mu, std=std, a=a, b=b, loc=loc, scale=scale,
                             maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=False, verbose=1)
# Plot
plt.figure()
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()
plt.title("Organismo 2 Etapas")
organismo.plot()

plt.show()
