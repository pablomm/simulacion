
import matplotlib.pyplot as plt
import numpy as np

from .organismo import Organismo

### Graficas de la estadistica Distancia recorrida
def plot_distancias(organismo, ax=None, param=None, plot_ci=True):

    if ax is None:
        ax = plt.gca()

    times = range(len(organismo.medias_distancias))
    ax.plot(times, organismo.medias_distancias, label=param)
    ax.set_xlabel("Unidades de tiempo")
    ax.set_ylabel("Distancia recorrida")
    if plot_ci:
        y1 = organismo.medias_distancias + organismo.std_distancias
        y2 = organismo.medias_distancias - organismo.std_distancias
        ax.fill_between(times, y1, y2, where=y1>=y2, alpha=0.3)
        #ax.plot(times, y1, linestyle="dashed", color="red", linewidth=0.5)
        #ax.plot(times, y2, linestyle="dashed", color="red", linewidth=0.5)
    if param:
        ax.legend()
    return ax

### Graficas de el numero de objetivos explotados en funcion del tiempo
def plot_numero_explotados(organismo, modelo, ax=None, param=None, plot_ci=True):

    if ax is None:
        ax = plt.gca()

    #ax.set_ylim([0, modelo.objetivos.numero_objetivos_inicial]) #Numero de objetivos inicial

    times = range(len(organismo.medias_explotados))
    ax.plot(times, organismo.medias_explotados, label=param)
    ax.set_xlabel("Unidades de tiempo")
    ax.set_ylabel("Numero de objetivos explotados")
    if plot_ci:
        y1 = organismo.medias_explotados + organismo.std_explotados
        y2 = organismo.medias_explotados - organismo.std_explotados
        ax.fill_between(times, y1, y2, where=y1>=y2, alpha=0.3)
        #ax.plot(times, y1, linestyle="dashed", color="red", linewidth=0.5)
        #ax.plot(times, y2, linestyle="dashed", color="red", linewidth=0.5)
    if param:
        ax.legend()
    return ax

### Graficas de la estadistica Distancia recorrida
def plot_radio_difusion_tiempo(organismo, ax=None, param=None, plot_ci=True):

    if ax is None:
        ax = plt.gca()

    times = range(len(organismo.medias_radio))
    ax.plot(times, organismo.medias_radio, label=param)
    ax.set_xlabel("Unidades de tiempo")
    ax.set_ylabel("Radio de difusion")
    if plot_ci:
        y1 = organismo.medias_radio + organismo.std_radio
        y2 = organismo.medias_radio - organismo.std_radio
        ax.fill_between(times, y1, y2, where=y1>=y2, alpha=0.3)
        #ax.plot(times, y1, linestyle="dashed", color="red", linewidth=0.5)
        #ax.plot(times, y2, linestyle="dashed", color="red", linewidth=0.5)
    if param:
        ax.legend()
    return ax

### Graficas de medias a lo largo del tiempo
def plot_medias_tiempo(organismo, ax=None, param=None, plot_ci=True, **kwargs):
    
    if ax is None:
        ax = plt.gca()
    
    times = range(len(organismo.medias))
    ax.plot(times, organismo.medias, label=param)
    ax.set_xlabel("Unidades de tiempo")
    #ax.set_ylabel("Medias")
    if plot_ci:
        y1 = organismo.medias + organismo.std
        y2 = organismo.medias - organismo.std
        ax.fill_between(times, y1, y2, where=y1>=y2, alpha=0.3)
        #ax.plot(times, y1, linestyle="dashed", color="red", linewidth=0.5)
        #ax.plot(times, y2, linestyle="dashed", color="red", linewidth=0.5)
    if param:
            ax.legend()
    return ax
