"""
Estudia  como varia el numero de targets/espacio recorrido y plotea el
histograma de los valores obtenidos

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
from simulador import TargetEspacioOrganismo, SimulacionHistograma
from simulador import RandomWalker


n_simulaciones = 200
# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = 500 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = RandomWalker(r, std=std, posicion=inicial)
modelo.add_organismo(organismo)

modelo.add_estadistica(TargetEspacioOrganismo())

# Especificamos que estadisticas queremos recolectar
histograma = SimulacionHistograma("recorrido_targets")
modelo.add_estadistica(histograma)


modelo.simular(t, n_simulaciones, verbose=1)

histograma.plot_histograma()

print("Media", np.mean(histograma.histograma))
print("Desviacion", np.std(histograma.histograma))

plt.show()
