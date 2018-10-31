

import sys
sys.path.append("../")

import numpy as np
import matplotlib.pyplot as plt

import itertools


from Objetivos import ObjetivosUniformes

# Configuracion del espacio
n_puntos = 300
size = (100,100)

coordenadas = np.array((10,10))
R = 20 # Radio de vision
r = 5 # Radio de explotacion

t = np.linspace(0,2*np.pi,100)

# Configuracion Plot
plt.style.use("seaborn")
plt.xlim(0, size[0])
plt.ylim(0, size[1])
ax = plt.gca()
color_vision = "blue"
color_explotacion = "red"
color_fuera = "green"
color_organismo = "orange"




# Modelo con targets distribuidos uniformes
objetivos = ObjetivosUniformes(n_puntos, size)
objetivos.plot(c=color_fuera)

puntos_equivalentes =  itertools.product((0,-size[0],size[0]),(0,-size[1],size[1]))



puntos = np.array(list(puntos_equivalentes)) + coordenadas

# Dibujamos areas de las zonas
for punto in puntos:
    zona = plt.Circle(punto, R, color=color_vision, alpha=.2)
    ax.add_artist(zona)
    zona = plt.Circle(punto, r, color=color_explotacion, alpha=.2)
    ax.add_artist(zona)


zona_vision = objetivos.objetivos(r=R, coordenadas=puntos)
zona_explotacion = objetivos.objetivos(r=r, coordenadas=puntos)

if len(zona_vision) != 0:
    plt.scatter(zona_vision[:,0],zona_vision[:,1], c=color_vision)

if len(zona_explotacion) != 0:
    plt.scatter(zona_explotacion[:,0],zona_explotacion[:,1], c=color_explotacion)



# Pintamos el punto del organismo
plt.scatter(*coordenadas, c=color_organismo)

plt.show()
