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
sys.path.append("../../")

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
organismo = LevyFlightActivo(r_explotacion=10, r_sensibilidad=3)
modelo.add_organismo(organismo)


# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())

modelo.simular(500, 1)
for estadistica in modelo.estadisticas:
  plt.figure()
  plt.hist(estadistica.areaRep,density=False,bins='auto')
  plt.title('Area repetida')
  plt.figure()
  plt.hist(estadistica.areaRecorrida,density=False,bins='auto')
  plt.title('Area recorrida')
  plt.figure()
  plt.hist(estadistica.ratioRepeticion,density=False,bins='auto')
  plt.title('Ratio de repeticion')
  plt.figure()
  plt.hist(estadistica.ratioExplotadosArea,density=False,bins='auto')
  plt.title('Ratio explotados/area recorrida')  
  #plt.figure()
  #plt.hist(estadistica.ratioRepetidoRecorrido,density=False,bins='auto')
  #plt.title('Ratio area repetida/area recorrida')
  #plt.figure()
  #organismo.plot_mapa_calor()
  plt.show()

plt.figure()
organismo.plot_mapa_calor()
plt.show()

# Guardar datos de las simulaciones
#np.savetxt('../datos/area_repetida.txt', estadistica.areaRep, delimiter="\t")
#np.savetxt('../datos/area_recorrida.txt', estadistica.areaRecorrida, delimiter="\t")
#np.savetxt('../datos/ratio_repeticion.txt', estadistica.ratioRepeticion, delimiter="\t")
#np.savetxt('../datos/ratio_explotados_area.txt', estadistica.ratioExplotadosArea, delimiter="\t")
#np.savetxt('../datos/ratio_repetidos_recorridos.txt', estadistica.ratioRepetidoRecorrido, delimiter="\t")


