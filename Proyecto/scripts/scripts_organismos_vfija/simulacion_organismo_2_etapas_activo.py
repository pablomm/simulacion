
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import Trayectoria, Explotados, RadioDifusion
from simulador import RandomWalkerActivo, LevyFlightActivo


# Configuracion del espacio
n_objetivos = 50 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 1. # Radio de explotacion
R = 5.

mu = 0.
std = 1. # Desviacion estandar del movimiento browniano

a = 1.5 # alpha de distribucion de levy
b = 1. # beta de distribucion de levy
maximo = np.inf # Maxima distancia en un salto
minimo = 0 # Minima distancia en un salto
loc = 0
scale = 1.

v = 1. #Velocidad del organismo
t = 200 # Tiempo a simular
inicial = (size[0]/2,size[0]/2) # Coordenadas iniciales (None para aleatorias)
# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
#organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v, mu=mu, std=std, stop_eat=False, posicion=inicial)
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                             a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                             minimo=minimo, stop_eat=False, posicion=inicial)
modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())
modelo.add_estadistica(RadioDifusion())

modelo.simular(t)

# Dibujamos el resultado de la simulacion
modelo.plot()
#organismo.plot_area_visualizada(color = "lightgreen")
#organismo.plot_area_explotada(alpha=0.01)
organismo.plot_trayectoria()
organismo.plot_explotados()

#print("radio", organismo.radio_difusion)
#print("espacio recorrido", organismo.espacio_recorrido)
#print("objetivos explotados", organismo.n_explotados)

plt.show()
