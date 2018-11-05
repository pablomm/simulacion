
import matplotlib.pyplot as plt

from .organismo import Organismo

### Graficas de las estadisticas de Trayectoria
def plot_trayectoria(organismo, ax=None, color="default"):
    """ Dibuja la trayectoria que ha recorrido el organismo"""

    if len(organismo.trayectoria) > 1:

        if color == "default":
            color = Organismo.color_organismo

        organismo.espacio.plot_trayectoria(organismo.trayectoria,
                                           organismo.trayectoria_real, ax,
                                           c=color)

    return ax

def plot_area_explotada(organismo, ax=None, color="default", alpha=None):
    if ax is None:
        ax = plt.gca()

    if color == "default":
        color = Organismo.color_area_explotada

    if alpha is None:
        alpha = Organismo.opacidad_area

    for p in organismo.trayectoria:
        zona = plt.Circle(p, organismo.r_explotacion, color=color, alpha=alpha)
        ax.add_artist(zona)

    return ax

def plot_area_visualizada(organismo, ax=None, color="default", alpha=None):
    if ax is None:
        ax = plt.gca()

    if color == "default":
        color = Organismo.color_area_visualizada

    if alpha is None:
        alpha = Organismo.opacidad_area

    for p in organismo.trayectoria:

        zona = plt.Circle(p, organismo.r_sensibilidad, color=color, alpha=alpha)
        ax.add_artist(zona)

    return ax

### Graficas de la estadistica Explotados
def plot_explotados(organismo, t=-1, ax=None, color="default"):

    if ax is None:
        ax = plt.gca()

    if color == "default":
        color = Organismo.color_explotados

    if t != -1 and organimos.explotados is not None:
        ax.scatter(organismo.explotados[t][:,0], organismo.explotados[t][:,1],
                   c=color)
    else:
        for explotados in organismo.explotados:
            if explotados is not None:
                ax.scatter(explotados[:,0], explotados[:,1], c=color)

    return ax

### Graficasde la estadistica Recorrido Targets
def plot_recorrido_targets(estadistica, ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    for i in range(estadistica.modelo.n_organismos):
        ax.hist(estadistica.recorrido_targets[:,i], density=True, **kwargs)

    return ax

### Grafica para estadistica

### Graficasde la estadistica Recorrido Targets Multiple
def plot_medias(estadistica, ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    for i in range(estadistica.n_organismos):
        ax.plot(estadistica.parametros, estadistica.medias[:,i])

    return ax
