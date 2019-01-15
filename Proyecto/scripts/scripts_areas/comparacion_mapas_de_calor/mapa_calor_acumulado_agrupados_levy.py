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
from simulador import LevyFlightActivo, RandomWalkerActivo, Organismo2Organismo2Etapas

n_simulaciones=500

# Configuracion del espacio
n_puntos_grupo = 25
n_grupos = 4
std_grupos = 5 # Desviacion estandar de los grupos
grupos = [[25, 25] ,[25, 75], [75, 25], [75, 75]]

size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 5
t = 500 # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)

maximo_levy = 100

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)

#alphas = [2,1.8,1.6,1.5,1.4,1.2,1.,0.8]

Rs = [0, 0.5, 1, 1.5, 2, 3, 4, 10]

fig, ax = plt.subplots(2, len(Rs)//2)

plt.suptitle("Random Walker activo")
for i, R in enumerate(Rs):
    # LevyFlight Activo
    objetivos = ObjetivosAgrupados(n_puntos_grupo, espacio, n_grupos, std_grupos, grupos=grupos)
    modelo = Modelo(espacio, objetivos)
    organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R)
    #organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R,
    #                             maximo=maximo_levy, minimo=-maximo_levy, a=alpha)
    modelo.add_organismo(organismo)
    # Especificamos que estadisticas queremos recolectar
    modelo.add_estadistica(EstadisticaArea())
    modelo.add_estadistica(EstadisticaAreaAcumulada())

    modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

    ax[i%2][i//2].title.set_text("$R={}$".format(R))

    organismo.plot_mapa_calor_acumulado(ax[i%2][i//2])
    #np.save("lfa-oa", organismo.mapa_calor_acumulado)

    #print ("LevyFlightActivo")
    #print (st.chisquare(organismo.mapa_calor_acumulado.flatten()))
plt.show()
