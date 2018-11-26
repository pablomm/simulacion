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
from simulador import EstadisticaArea
from simulador import LevyFlightActivo

"""
Script para ver el area repetida (Distribucion) por el organismo
"""
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = LevyFlightActivo(1,3)
modelo.add_organismo(organismo)


# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())

modelo.simular(500,500)
for estadistica in modelo.estadisticas:
  plt.figure()
  plt.hist(estadistica.areaRep,density=False,bins='auto')
  plt.title('Area repetida')
  plt.figure()
  plt.hist(estadistica.areaRecorrida,density=False,bins='auto')
  plt.title('Area')
  plt.figure()
  plt.hist(estadistica.ratioRepeticion,density=False,bins='auto')
  plt.title('Ratio')
  plt.figure()
  plt.hist(estadistica.ratioExplotadosArea,density=False,bins='auto')
  plt.title('explotados')
  #plt.figure()
  #organismo.plot_mapa_calor()
  plt.show()