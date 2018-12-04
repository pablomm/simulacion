import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioFinito, Modelo
from simulador import TargetEspacioOrganismo, VariacionParametroBloques
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import EstadisticaArea1Obj

n_simulaciones = 500
n_variaciones = 5

# Configuracion del espacio
n_objetivos = 1 # Numero de objetivos
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1. # Desviacion estandar del movimiento browniano
t = 200000 # Tiempo a simular
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

#Plots
fig, (area_recorrida_levy,area_recorrida_rw) = plt.subplots(1, 2)
area_recorrida_levy.set_title("Area explorada para encontrar un elemento en levy(r={}, R={})".format(r, R))
area_recorrida_rw.set_title("Area explorada para encontrar un elemento en rw(r={}, R={})".format(r, R))

fig, (area_repetida_levy,area_repetida_rw) = plt.subplots(1, 2)
area_repetida_levy.set_title("Area repetida para encontrar un elemento (r={}, R={})".format(r, R))

fig, (tiempo_levy,tiempo_rw) = plt.subplots(1, 2)
tiempo_levy.set_title("Tiempo para encontrar un elemento (r={}, R={})".format(r, R))
#Modelo
espacio = EspacioFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(EstadisticaArea1Obj())

#RandomWalker Activo
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                                 minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)
plt.figure(4)
organismo.plot()
modelo.plot()
plt.show()

modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)

area_recorrida_levy.hist(organismo.areaRecorrida)
area_repetida_levy.hist(organismo.areaRep)
tiempo_levy.hist(organismo.tiempo_hasta_objetivo)
DAT = np.c_[organismo.areaRecorrida,organismo.areaRep,organismo.tiempo_hasta_objetivo]
np.savetxt('areasLevy',DAT,delimiter=",",header="Recorrida,Repetida,Tiempo")

modelo.limpiar_organismos()

organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                               std=std, stop_eat=False, posicion=inicial)

modelo.add_organismo(organismo)

modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)

area_recorrida_rw.hist(organismo.areaRecorrida)
area_repetida_rw.hist(organismo.areaRep)
tiempo_rw.hist(organismo.tiempo_hasta_objetivo)
DAT = np.c_[organismo.areaRecorrida,organismo.areaRep,organismo.tiempo_hasta_objetivo]
np.savetxt('areasRW',DAT,delimiter=",",header="Recorrida,Repetida,Tiempo")

plt.show()
