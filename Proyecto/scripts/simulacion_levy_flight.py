

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
from organismo import LevyFlight


# Configuracion del espacio
n_puntos = 100
size = (100.,100.)
r = 3 # Radio de explotacion
t = 50
a = .5
b = 1.
loc = 0
scale = .05 

# Configuracion Plot
plt.style.use("seaborn")


espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_puntos, espacio)
modelo = Modelo(espacio, objetivos)

organismo = LevyFlight(r, a,b,loc,scale)
modelo.add_organismo(organismo)


modelo.simular(t)


organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()

plt.show()
