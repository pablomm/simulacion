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
r_explotacion = 3
r_sensibilidad = 1
t = 500 # Tiempo a simular
n_simulaciones = 50
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un organismo y lo añadimos al modelo
organismo = LevyFlightActivo(r_explotacion=r_explotacion,
                             r_sensibilidad=r_sensibilidad)
modelo.add_organismo(organismo)


# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())

modelo.simular(t, n_simulaciones=n_simulaciones)

plt.figure()
plt.hist(organismo.areaRep,density=False,bins='auto')
plt.title('Area repetida')

plt.figure()
plt.hist(organismo.areaRecorrida,density=False,bins='auto')
plt.title('Area recorrida')

plt.figure()
plt.hist(organismo.ratioRepeticion,density=False,bins='auto')
plt.title('Ratio de repeticion')

plt.figure()
plt.hist(organismo.ratioExplotadosArea,density=False,bins='auto')
plt.title('Ratio explotados/area recorrida')

plt.figure()
plt.hist(organismo.ratioRepetidoRecorrido,density=False,bins='auto')
plt.title('Ratio area repetida/area recorrida')

plt.figure()
plt.title("Mapa de calor")
organismo.plot_mapa_calor()

plt.show()


# Guardar datos de las simulaciones
#np.savetxt('./datos/area_repetida.txt', organismo.areaRep, delimiter="\t")
#np.savetxt('./datos/area_recorrida.txt', organismo.areaRecorrida, delimiter="\t")
#np.savetxt('./datos/ratio_repeticion.txt', organismo.ratioRepeticion, delimiter="\t")
#np.savetxt('./datos/ratio_explotados_area.txt', organismo.ratioExplotadosArea, delimiter="\t")
#np.savetxt('./datos/ratio_repetidos_recorridos.txt', organismo.ratioRepetidoRecorrido, delimiter="\t")
