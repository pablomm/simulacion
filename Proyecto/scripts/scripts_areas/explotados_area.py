"""
    Ejemplo de como variar un parametro y recoger la estadistica de otro a lo largo del tiempo
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
from simulador import EstadisticaTiempo, EstadisticaAreaTemp

n_simulaciones = 100
n_organismos = 3 #Los que comparamos

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1. # Desviacion estandar del movimiento browniano
t = 200 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)
# Organismo LevyFlight
a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

# Configuracion Plot
plt.style.use("seaborn")

fig, ax = plt.subplots(1, 1)
ax.set_title("Ratio objetivos explotados/area recorrida")
ax.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.5, n_organismos)))

#Modelo
espacio = EspacioToroidalFinito(*size)

#LevyFlight Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(EstadisticaAreaTemp())
modelo.add_estadistica(EstadisticaTiempo("ratioExplotadosArea"))
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                             minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)
modelo.simular(closing_time=t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

organismo.plot_medias_tiempo(ax=ax, param="levy_flight_activo")

# RandomWalker Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(EstadisticaAreaTemp())
modelo.add_estadistica(EstadisticaTiempo("ratioExplotadosArea"))
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                               std=std, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)
modelo.simular(closing_time=t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

organismo.plot_medias_tiempo(ax=ax, param="random_walker_activo")

#Organismo2Etapas (random walker + levy flight pasivo)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(EstadisticaAreaTemp())
modelo.add_estadistica(EstadisticaTiempo("ratioExplotadosArea"))
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             mu=mu, std=std, a=a, b=b, loc=loc, scale=scale,
                             maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)
modelo.simular(closing_time=t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

organismo.plot_medias_tiempo(ax=ax, param="organismo_2_etapas")

plt.show()
