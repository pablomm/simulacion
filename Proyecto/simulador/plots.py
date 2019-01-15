
import matplotlib.pyplot as plt
import numpy as np

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

def plot_trayectoria_parcial(organismo, t0, t1, ax=None, color="default"):
    """ Dibuja la trayectoria que ha recorrido el organismo"""

    if len(organismo.trayectoria) > 1:

        if color == "default":
            color = Organismo.color_organismo

        organismo.espacio.plot_trayectoria(organismo.trayectoria[t0:t1],
                                           organismo.trayectoria_real[t0:t1], ax,
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
def plot_explotados(organismo, t=-1, ax=None, color="default", t1=-1):

    if ax is None:
        ax = plt.gca()

    if color == "default":
        color = Organismo.color_explotados

    if t != -1 and organismo.explotados is not None:
        for tiempo in range(t, t1):
             if organismo.explotados[tiempo] is not None:
                ax.scatter(organismo.explotados[tiempo][:,0],
                           organismo.explotados[tiempo][:,1],
                           c=color)
    else:
        for explotados in organismo.explotados:
            if explotados is not None:
                ax.scatter(explotados[:,0], explotados[:,1], c=color)

    return ax

### Graficasde la estadistica Recorrido Targets
def plot_histograma(estadistica, ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    for i in range(estadistica.modelo.n_organismos):
        ax.hist(estadistica.histograma[:,i], density=True, **kwargs)

    return ax

### Graficasde la estadistica Recorrido Targets Multiple
def plot_medias(estadistica, ax=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    for i in range(estadistica.n_organismos):
        ax.plot(estadistica.parametros, estadistica.medias[:,i])

    return ax


def plot_radio_difusion(organismo, ax=None, color="default", alpha=None):
    if ax is None:
        ax = plt.gca()

    if color == "default":
        color = Organismo.color_area_visualizada

    if alpha is None:
        alpha = 0.5


    for p in organismo.espacio.coordenadas_equivalentes(organismo.posicion_inicial_simulacion):
        zona = plt.Circle(p, organismo.radio_difusion,
                      color=color, alpha=alpha)
        ax.add_artist(zona)

    return ax


def plot_mapa_calor(organismo, ax=None, color="YlOrBr"):
    if ax is None:
        ax = plt.gca()

    ax.imshow(organismo.MatrizArea.T, cmap="YlOrBr", origin="lower", interpolation='none', extent=[*organismo.espacio.ejex, *organismo.espacio.ejey])


def plot_gif(modelo, tiempo, save=None, nframes=100):

    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()
    #fig.set_tight_layout(True)


    modelo.espacio.plot()
    modelo.objetivos.plot(all=True)

    def update(i):

        t0 =int((i) * tiempo / nframes)
        t1 = int((i+1) * tiempo / nframes)

        label = 'Tiempo {0}'.format(t1)
        if save is not None:
            label = save + " " + label

        plt.title(label)
        print(label)


        for j,organismo in enumerate(modelo):
            #organismo.plot_area_explotada()



            plot_trayectoria_parcial(organismo, max(t0-1, 0), t1, color="C{}".format(j))

            organismo.plot_explotados(t=t0, t1=t1)

        return

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 200ms between frames.
    anim = FuncAnimation(fig, update, frames=np.arange(0, nframes), interval=100)

    if save is not None:
        anim.save(save + '.gif', dpi=80, writer='imagemagick')


    plt.show()

    return anim
