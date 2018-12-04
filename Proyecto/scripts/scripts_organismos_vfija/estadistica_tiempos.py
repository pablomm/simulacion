"""
    Estudia el tiempo en encontrar un solo objetivo para cada tipo de organismo.
    Se representa un histograma.
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
from simulador import TiempoEnExplotar

n_simulaciones = 200
n_organismos = 3 #Los que comparamos

# Configuracion del espacio
n_objetivos = 1 # Numero de objetivos
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1.5 # Desviacion estandar del movimiento browniano

densidad = n_objetivos/(size[0]*size[1])

t = 100000
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)
# Organismo LevyFlight
a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

# Configuracion Plot
plt.style.use("seaborn")

#Plots
fig, ax = plt.subplots(1, 1)
ax.set_title("Tiempo en explotar (r={}, R={}, 1 objetivo)".format(r, R))
ax.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.7, n_organismos)))

espacio = EspacioToroidalFinito(*size)

# RandomWalker Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(TiempoEnExplotar())
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             std=std, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
ax.hist(organismo.tiempos_explotar, alpha=0.3, label="random_walker_activo")

#LevyFlight Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(TiempoEnExplotar())
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                             minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
ax.hist(organismo.tiempos_explotar, alpha=0.3, label="levy_flight_activo")

#Organismo2Etapas (random walker + levy flight pasivo)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(TiempoEnExplotar())
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v, 
                             mu=mu, std=std, a=a, b=b, loc=loc, scale=scale, 
                             maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
ax.hist(organismo.tiempos_explotar, alpha=0.3, label="organismo_2_etapas")

plt.legend()
plt.show()

