"""
Estudia las diferencias de tiempos entre objetivos comidos
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Añadimos al path la raiz para poder importar la libreria local
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")
sys.path.append("./")
filename = os.path.basename(__file__).split(".")[0]

from simulador import ObjetivosUniformes, EspacioToroidalFinito
from simulador import RandomWalkerActivo

from simulacion_tiempos import simular_tiempos


# Variables de la simulacion
n_simulaciones = 100
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 1 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = 10000 # Tiempo a simular
inicial = (size[0]/2,size[1]/2) # Coordenadas iniciales en el centro del espacio


espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
organismo = RandomWalkerActivo(1,r_sensibilidad=3, posicion=inicial)

simular_tiempos(organismo, espacio, objetivos, n_objetivos, filename)
