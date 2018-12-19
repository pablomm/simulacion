"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosAgrupados, EspacioToroidalFinito, Modelo
from simulador import VariacionParametroBloques
from simulador import LevyFlightActivo, RandomWalkerActivo, Organismo2Etapas

n_simulaciones = 100
n_variaciones = 10
n_alphas = 6

# Configuracion del espacio
n_puntos_grupo = 40
n_grupos = 1
grupos = [[50,50]]
std_grupos = np.linspace(3,50, n_variaciones) # Desviacion estandar de los grupos

size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3 # Radio de sensibilidad
t = 500 # Tiempo a simular

alphas = np.linspace(1,2, n_alphas)
maximo_levy = (min(size[0], size[1]))

# Configuracion Plot
plt.style.use("seaborn")

fig, ax = plt.subplots(1, 1)
ax.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.6, n_alphas)))
fig.suptitle("Numero de explotados Levy Flight Activo - Objetivos agrupados, 1 nucleo")
#ax.set_ylim([0,n_puntos_grupo])

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos[0], grupos=grupos)

for i, a in enumerate(alphas):
    modelo = Modelo(espacio, objetivos)
    estadistica = VariacionParametroBloques("n_explotados", std_grupos)
    modelo.add_estadistica(estadistica)
    for std in std_grupos:
        objetivos.std_grupos = std
        # LevyFlight Activo
        organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R, a=a, maximo=maximo_levy)
        
        modelo.add_organismo(organismo)

        modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)
        modelo.limpiar_organismos()

    estadistica.plot_medias()

labels = ["⍺={}".format(a) for a in alphas]
ax.legend(labels)
plt.show()
