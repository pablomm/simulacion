"""
Script para generar plots con radios del organismo

"""

import os
import sys

import matplotlib.pyplot as plt

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../")


import matplotlib.pyplot as plt


from objetivos import ObjetivosUniformes
from espacio import EspacioToroidalFinito
from modelo import Modelo
from organismo import OrganismoSencillo

# Configuracion del espacio
n_puntos = 100
size = (100.,100.)
r = 5 # Radio de explotacion
R = 15 # Radio de sensibilidad

# Configuracion Plot
plt.style.use("seaborn")

espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_puntos, espacio)
modelo = Modelo(espacio, objetivos)

organismo = OrganismoSencillo(r)

# Modificamos un radio de sensibilidad para mostrar en la figura
organismo.r_sensibilidad = R


modelo.add_organismo(organismo)

modelo.plot()
organismo.plot()



plt.show()
