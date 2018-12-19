"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea, EstadisticaAreaAcumulada
from simulador import LevyFlightActivo, RandomWalkerActivo, Organismo2Etapas

n_simulaciones=250
n_variaciones=6

# Configuracion del espacio
n_puntos_grupo = 25
n_grupos = 4
std_grupos = 5 # Desviacion estandar de los grupos
grupos = [[50,50]]

size = (100.,100.) # Dimensiones del espacio
r = 1
Radios = np.linspace(1, 10, n_variaciones) # Radio de explotacion
t = 500 # Tiempo a simular

maximo_levy = (min(size[0], size[1]))
tiempo_regen = 100

# Configuracion Plot
plt.style.use("seaborn")

fig, ax = plt.subplots(2,3)
fig.suptitle("Mapa calor acumulada Levy Flight Activo - Objetivos agrupados")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)

for i, R in enumerate(Radios):
    print ("Radio de sensibilidad", R)
    # LevyFlight Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    #organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, maximo=maximo_levy)
    
    modelo.add_organismo(organismo)
    # Especificamos que estadisticas queremos recolectar
    modelo.add_estadistica(EstadisticaArea())
    modelo.add_estadistica(EstadisticaAreaAcumulada())

    modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

    x = ax[i//3,i%3]
    organismo.plot_mapa_calor_acumulado(ax=x)
    x.set_title("R={}".format(R))
    #np.save("volcado", organismo.mapa_calor_acumulado)

plt.show()
