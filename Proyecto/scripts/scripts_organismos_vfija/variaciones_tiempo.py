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
from simulador import TargetEspacioOrganismo, VariacionParametroBloques
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import EstadisticaTiempo

n_simulaciones = 10
n_variaciones = 5

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
densidad = n_objetivos/(size[0]*size[1])
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1. # Desviacion estandar del movimiento browniano
t = 2000 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)
# Organismo LevyFlight
a = np.linspace(1,2,n_variaciones) # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

# Configuracion Plot
plt.style.use("seaborn")

#Modelo
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
modelo.add_estadistica(EstadisticaTiempo("n_explotados"))

#LevyFlight Activo variando a
for param in a:
    # Creamos un random walker y lo añadimos al modelo
    organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 a=param, b=b, loc=loc, scale=scale, maximo=maximo,
                                 minimo=minimo, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)
    modelo.simular(t, n_simulaciones, stop_empty=False, verbose=1)

    organismo.plot_medias_tiempo(param="levy_flight(a={})".format(param))
    modelo.limpiar_organismos()

ax = plt.gca()
ax.set_title("Numero explotados")
plt.show()
