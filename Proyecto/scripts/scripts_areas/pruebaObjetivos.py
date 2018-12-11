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

from simulador import ObjetivosDiTuComo, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea
from simulador import LevyFlightActivo
size = (100.,100.) # Dimensiones del espacio
nobjetivos = np.array([100,100,50,100,0,0,0,0,100,100])
division = np.array([1,1,0,2,0,0,0,0,2,2])

espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosDiTuComo(nobjetivos, espacio,division)
modelo = Modelo(espacio, objetivos)
espacio.plot()
objetivos.plot()
objetivos.plot_grupos()
plt.show()