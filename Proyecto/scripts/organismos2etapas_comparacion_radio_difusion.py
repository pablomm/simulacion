"""
    Estudia  como varia el numero de targets/espacio recorrido y plotea el
    histograma de los valores obtenidos variando la desviacion estandar
    """

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import TargetEspacioOrganismo, VariacionParametroBloques
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import RadioDifusion

n_simulaciones = 1
n_variaciones = 2
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
std = 1.5 # Desviacion estandar del movimiento browniano

tiempo_maximo = 2000
tiempos = np.linspace(1,tiempo_maximo, n_variaciones) # Tiempo a simular
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
ax.set_title("Radio difusion")
ax.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.5, n_organismos)))

espacio = EspacioToroidalFinito(*size)

# RandomWalker Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(RadioDifusion())
estadistica = VariacionParametroBloques("radio_difusion", tiempos)
modelo.add_estadistica(estadistica)
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             std=std, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

for t in tiempos:
    modelo.simular(int(t), n_simulaciones=n_simulaciones, stop_empty=False, verbose=2)

estadistica.plot_medias(ax=ax)

#LevyFlight Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(RadioDifusion())
estadistica = VariacionParametroBloques("radio_difusion", tiempos)
modelo.add_estadistica(estadistica)
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                             minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

for t in tiempos:
    modelo.simular(int(t), n_simulaciones=n_simulaciones, stop_empty=False, verbose=2)

estadistica.plot_medias(ax=ax)


#Organismo2Etapas (random walker + levy flight pasivo)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(RadioDifusion())
estadistica = VariacionParametroBloques("radio_difusion", tiempos)
modelo.add_estadistica(estadistica)
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v, 
                             mu=mu, std=std, a=a, b=b, loc=loc, scale=scale, 
                             maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

for t in tiempos:
    modelo.simular(int(t), n_simulaciones=n_simulaciones, stop_empty=False, verbose=2)

estadistica.plot_medias(ax=ax)
x = np.linspace(1,tiempo_maximo,100)
c = estadistica.medias[-1]/np.sqrt(tiempo_maximo)
plt.plot(x,c*np.sqrt(x), color="red", linestyle="dashed")

plt.legend(['random_walker_activo', 'levy_activo', 'organismo_2_etapas'])

plt.show()

