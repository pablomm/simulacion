"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea,Trayectoria
from simulador import LevyFlightActivo


# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r_explotacion = 1 # Radio de explotacion
r_sensibilidad = 3
t = 1000 # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = LevyFlightActivo(r_explotacion=r_explotacion,
                             r_sensibilidad=r_sensibilidad,
                             posicion=inicial)

modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(Trayectoria())

modelo.simular(t)


modelo.plot()
organismo.plot_area_explotada()
organismo.plot_trayectoria()

plt.figure()
plt.title("Mapa calor del area explotada por el organismo")
organismo.plot_mapa_calor()

plt.show()
