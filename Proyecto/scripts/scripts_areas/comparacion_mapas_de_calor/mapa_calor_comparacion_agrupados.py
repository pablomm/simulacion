"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea,Trayectoria
from simulador import LevyFlightActivo, RandomWalkerActivo, Organismo2Etapas


# Configuracion del espacio
n_puntos_grupo = 25
n_grupos = 4
std_grupos = 4 # Desviacion estandar de los grupos

size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3
t = 10000 # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)

maximo_levy = (min(size[0], size[1]))/2

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)

# RandomWalker Activo
objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos)
modelo = Modelo(espacio, objetivos)
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R,
                               posicion=inicial)
modelo.add_organismo(organismo)
# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(Trayectoria())

modelo.simular(t, stop_empty=False, verbose=1)
plt.figure()
modelo.plot()
organismo.plot_area_explotada()
organismo.plot_trayectoria()
plt.figure()
plt.title("Mapa calor del area explotada por el Random Walker Activo - Argupados")
organismo.plot_mapa_calor()

# Levy flight activo
objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos)
modelo = Modelo(espacio, objetivos)
organismo = LevyFlightActivo(r_explotacion=r,
                             r_sensibilidad=R,
                             posicion=inicial)

modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(Trayectoria())

modelo.simular(t, stop_empty=False, verbose=1)
plt.figure()
modelo.plot()
organismo.plot_area_explotada()
organismo.plot_trayectoria()
plt.figure()
plt.title("Mapa calor del area explotada por el Levy Flight Activo - Argupados")
organismo.plot_mapa_calor()

# Organismo2Etapas
objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos)
modelo = Modelo(espacio, objetivos)
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R,
                             maximo=maximo_levy, posicion=inicial)

modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(Trayectoria())

modelo.simular(t, stop_empty=False, verbose=1)
plt.figure()
modelo.plot()
organismo.plot_area_explotada()
organismo.plot_trayectoria()
plt.figure()
plt.title("Mapa calor del area explotada por el Organismo 2 Etapas - Argupados")
organismo.plot_mapa_calor()

plt.show()
