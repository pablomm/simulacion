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
from simulador import RandomWalker


n_simulaciones = 50
n_variaciones = 30

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = np.linspace(0.1, 15, n_variaciones) # Desviacion estandar del movimiento browniano
t = 500 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(TargetEspacioOrganismo())

# Recolectamos medias y desviaciones al final de cada bloque de simulacion
estadistica = VariacionParametroBloques("recorrido_targets", std)
modelo.add_estadistica(estadistica)

for desviacion in std:
    # Creamos un random walker y lo añadimos al modelo
    organismo = RandomWalker(r, std=desviacion, posicion=inicial)
    modelo.add_organismo(organismo)
    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    modelo.limpiar_organismos()


plt.figure()
estadistica.plot_medias()

plt.show()
