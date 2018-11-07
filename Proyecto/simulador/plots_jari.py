
import matplotlib.pyplot as plt
import numpy as np

from .organismo import Organismo

### Graficas de la estadistica Distancia recorrida
def plot_distancias(organismo, ax=None, param=None):

    if ax is None:
        ax = plt.gca()

    times = range(len(organismo.medias_distancias))
    ax.plot(times, organismo.medias_distancias, label=param)
    if param:
        ax.legend()
    return ax

### Graficas de el numero de objetivos explotados en funcion del tiempo
def plot_numero_explotados(organismo, modelo, ax=None, param=None):

    if ax is None:
        ax = plt.gca()

    ax.set_ylim([0, modelo.objetivos.numero_objetivos_inicial]) #Numero de objetivos inicial

    times = range(len(organismo.medias_explotados))
    ax.plot(times, organismo.medias_explotados, label=param)
    if param:
        ax.legend()
    return ax
