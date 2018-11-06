

import os
import sys
import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioFinito, Modelo
from simulador import Trayectoria, Explotados
from simulador import RandomWalker


# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
n_organismos = 5
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = 500 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

for _ in range(n_organismos):
    organismo = RandomWalker(r, posicion=inicial)
    modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())

modelo.simular(t)

# Dibujamos el resultado de la simulacion
modelo.plot()

for organismo in modelo:
    organismo.plot_area_explotada(color=None)
    organismo.plot_trayectoria(color=None)
    organismo.plot_explotados()

plt.show()
