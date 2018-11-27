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
sys.path.append("../../")

# Configuracion Plot
plt.style.use("seaborn")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import RadioDifusion, VariacionParametroBloques
from simulador import RandomWalker


n_simulaciones = 250
n_variaciones = 40

# Configuracion del espacio
n_objetivos = 0 # Numero de objetivos
size = (100000.,100000.) # Dimensiones del espacio
tiempo_maximo = 1000
r = 1 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
tiempos = np.linspace(1,tiempo_maximo, n_variaciones) # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)


# Creamos un random walker y lo añadimos al modelo
organismo = RandomWalker(r, std=std, posicion=inicial)
modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(RadioDifusion())

# Recolectamos medias y desviaciones al final de cada bloque de simulacion
estadistica = VariacionParametroBloques("radio_difusion", tiempos)
modelo.add_estadistica(estadistica)

for t in tiempos:
    modelo.simular(int(t), n_simulaciones=n_simulaciones, stop_empty=False, verbose=2)



plt.figure()
estadistica.plot_medias()

x = np.linspace(1,tiempo_maximo,100)
c = estadistica.medias[-1]/np.sqrt(tiempo_maximo)
plt.plot(x,c*np.sqrt(x), color="red", linestyle="dashed")

plt.show()
