"""
    Estudia el tiempo en encontrar un solo objetivo dependiendo de
    la distancia a la que se encuentre, para cada tipo de organismo.
    """

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito, Modelo
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import TiempoEnExplotar

n_simulaciones = 50
n_organismos = 3 #Los que comparamos
n_dist = 50

# Configuracion de los objetivos
n_puntos_grupo = 1
n_grupos = 1
std_grupos = 0. # Desviacion estandar de los grupos
distancia = np.linspace(1,50,n_dist)
          
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1.5 # Desviacion estandar del movimiento browniano

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
ax.set_title("Tiempo en explotar frente a la distancia inicial a la presa (r={}, R={}, 1 objetivo)".format(r, R))

espacio = EspacioToroidalFinito(*size)

rw = []
lf = []
o2e = []

for d in distancia:
    grupos = [[50, 50+d]]
    # RandomWalker Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 std=std, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    rw.append( organismo.medias_tiempo_explotar )

    #LevyFlight Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                                 minimo=minimo, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    lf.append( organismo.medias_tiempo_explotar )

    #Organismo2Etapas (random walker + levy flight pasivo)
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 mu=mu, std=std, a=a, b=b, loc=loc, scale=scale,
                                 maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    o2e.append( organismo.medias_tiempo_explotar )

ax.plot(distancia, rw, label="random_walker_activo", color="black")
ax.plot(distancia, lf, label="levy_flight_activo", color="brown")
ax.plot(distancia, o2e, label="organismo_2_etapas", color="red")

plt.legend()
plt.show()

