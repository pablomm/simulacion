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

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea, EstadisticaAreaAcumulada
from simulador import LevyFlightActivo, RandomWalkerActivo, Organismo2Etapas

n_simulaciones=500

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos

size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
R = 3
t = 500 # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales (None para aleatorias)

maximo_levy = (min(size[0], size[1]))/2
tiempo_regen = 100

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)

# RandomWalker Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
organismo = RandomWalkerActivo(r_explotacion=r, r_sensibilidad=R)
modelo.add_organismo(organismo)
# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(EstadisticaAreaAcumulada())

plt.figure()
modelo.plot()

modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

plt.figure()
plt.title("Mapa calor acumulada Random Walker Activo - Objetivos uniformes")
organismo.plot_mapa_calor_acumulado()

np.save("rwa-ou", organismo.mapa_calor_acumulado)
print ("RandomWalkerActivo")
print (st.chisquare(organismo.mapa_calor_acumulado.flatten()))

# LevyFlight Activo
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
organismo = LevyFlightActivo(r_explotacion=r, r_sensibilidad=R)
modelo.add_organismo(organismo)
# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(EstadisticaAreaAcumulada())

modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

plt.figure()
plt.title("Mapa calor acumulada Levy Flight Activo - Objetivos uniformes")
organismo.plot_mapa_calor_acumulado()

np.save("lfa-ou", organismo.mapa_calor_acumulado)
print ("LevyFlightActivo")
print (st.chisquare(organismo.mapa_calor_acumulado.flatten()))

# Organismo2Etapas
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)
organismo = Organismo2Etapas(r_explotacion=r, r_sensibilidad=R, maximo=maximo_levy)
modelo.add_organismo(organismo)
# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(EstadisticaAreaAcumulada())

modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=False, verbose=1)

plt.figure()
plt.title("Mapa calor acumulada Organismo 2 Etapas - Objetivos uniformes")
organismo.plot_mapa_calor_acumulado()

#plt.show()

np.save("o2e-ou", organismo.mapa_calor_acumulado)
print ("Organismo2Etapas")
print (st.chisquare(organismo.mapa_calor_acumulado.flatten()))
