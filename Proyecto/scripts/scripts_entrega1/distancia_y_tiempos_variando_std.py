"""
    Estudia  como varia el numero de targets/espacio recorrido y plotea el
    histograma de los valores obtenidos variando la desviacion estandar
    """

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import TargetEspacioOrganismo, VariacionParametroBloques
from simulador import RandomWalker, LevyFlight
from simulador import Explotados, Distancias

n_simulaciones = 100
n_variaciones = 5

# Configuracion del espacio
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = np.linspace(0.1, 12, n_variaciones) # Desviacion estandar del movimiento browniano
t = 2000 # Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Recolectamos explotados y distancias al final de cada bloque de simulacion
modelo.add_estadistica(Explotados())
modelo.add_estadistica(Distancias())

#Plots
fig, distancias = plt.subplots(1, 1)
distancias.set_title("Distancia recorrida frente al tiempo transcurrido")
distancias.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.5, n_variaciones)))

fig, explotados = plt.subplots(1, 1)
explotados.set_title("Numero de objetivos explotados frente al tiempo")
explotados.set_prop_cycle(color=plt.cm.gist_heat(np.linspace(0,0.5, n_variaciones)))

for desviacion in std:
    # Creamos un random walker y lo añadimos al modelo
    organismo = RandomWalker(r, std=desviacion, posicion=inicial)
    modelo.add_organismo(organismo)
    modelo.simular(t, n_simulaciones, stop_empty=False, verbose=1)
    
    organismo.plot_distancias(ax=distancias, param =f"std={round(desviacion,2)}")
    organismo.plot_numero_explotados(modelo, ax=explotados, param=f"std={round(desviacion,2)}")
    modelo.limpiar_organismos()

    #print(organismo.std_distancias[1])
    #print(organismo.std_distancias[-1])


plt.show()
