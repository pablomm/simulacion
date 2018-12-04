"""
    Estudia el tiempo en encontrar un solo objetivo dependiendo de
    la distancia a la que se encuentre, para cada tipo de organismo.
    """

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito, Modelo
from simulador import RandomWalkerActivo, LevyFlightActivo, Organismo2Etapas
from simulador import TiempoEnExplotar

n_simulaciones = 50
n_organismos = 3 #Los que comparamos
n_variaciones = 50

# Configuracion de los objetivos
n_puntos_grupo = 1
n_grupos = 1
std_grupos = 0. # Desviacion estandar de los grupos
distancia = np.linspace(0, 50, n_variaciones)

# Configuracion del espacio
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
v = 1. # Velocidad del organismo
# Organismo RandomWalker
mu = 0. #Media del movimiento browniano
std = 1.5 # Desviacion estandar del movimiento browniano

t = 100000
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
ax.set_title("Tiempo en explotar frente a la distancia inicial a la presa (r={}, R={}, 1 objetivo)".format(r, R))

espacio = EspacioToroidalFinito(*size)

rw = np.empty(n_variaciones)
lf = np.empty(n_variaciones)
o2e = np.empty(n_variaciones)
rw_std = np.empty(n_variaciones)
lf_std = np.empty(n_variaciones)
o2e_std = np.empty(n_variaciones)

for i, d in enumerate(distancia):
    grupos = [[50, 50+d]]
    # RandomWalker Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 std=std, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    rw[i] = organismo.medias_tiempo_explotar
    rw_std[i] = organismo.std_tiempo_explotar

    #LevyFlight Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 a=a, b=b, loc=loc, scale=scale, maximo=maximo,
                                 minimo=minimo, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    lf[i] = organismo.medias_tiempo_explotar
    lf_std[i] = organismo.std_tiempo_explotar

    #Organismo2Etapas (random walker + levy flight pasivo)
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos,
                                   std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    modelo.add_estadistica(TiempoEnExplotar())
    organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, velocidad=v,
                                 mu=mu, std=std, a=a, b=b, loc=loc, scale=scale,
                                 maximo=maximo, minimo=minimo, stop_eat=False, posicion=inicial)
    modelo.add_organismo(organismo)

    modelo.simular(t, n_simulaciones, stop_empty=True, verbose=1)
    o2e[i] = organismo.medias_tiempo_explotar
    o2e_std[i] = organismo.std_tiempo_explotar

#Plot
ax.plot(distancia, rw, label="random_walker_activo", color="black")
y1 = rw + rw_std
y2 = rw - rw_std
ax.fill_between(distancia, y1, y2, where=y1>=y2, alpha=0.3, color="black")
ax.plot(distancia, lf, label="levy_flight_activo", color="brown")
y1 = lf + lf_std
y2 = lf - lf_std
ax.fill_between(distancia, y1, y2, where=y1>=y2, alpha=0.3, color="brown")
ax.plot(distancia, o2e, label="organismo_2_etapas", color="red")
y1 = o2e + o2e_std
y2 = o2e - o2e_std
ax.fill_between(distancia, y1, y2, where=y1>=y2, alpha=0.3, color="red")

plt.legend()
plt.show()

