

import os
import sys
import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import Trayectoria, Explotados, RadioDifusion
from simulador import RandomWalker


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

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(Trayectoria())
modelo.add_estadistica(Explotados())
modelo.add_estadistica(RadioDifusion())

modelo.simular(t)

# Dibujamos el resultado de la simulacion
organismo.plot_radio_difusion()
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()

print("radio", organismo.radio_difusion)

plt.show()
