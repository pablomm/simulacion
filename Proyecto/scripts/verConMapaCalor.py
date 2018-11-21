"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
import statsmodels.api as sm

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea,Trayectoria
from simulador import RandomWalker


# Configuracion del espacio
n = 1
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = np.linspace(50,1000,n)# Tiempo a simular
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
modelo.add_estadistica(EstadisticaArea())
modelo.add_estadistica(Trayectoria())
valores = np.zeros(n)
IC0 = np.zeros(n)
IC1 = np.zeros(n)
rep = np.zeros(n)
ICrep = np.zeros(n)
ICrep1 = np.zeros(n)
modelo.simular(500,1)

estadistica = modelo.estadisticas[0]

print(estadistica.areaRecorrida)
organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
#plt.figure()
organismo.plot_mapa_calor()
#organismo.plot_explotados()

plt.show()

    #estadistica.inicializar(0,20)
#Vamos a suavizar la curva restando las frecuencias no importantes
lowess = sm.nonparametric.lowess(valores, t, frac=0.1)
