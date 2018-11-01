
from abc import ABCMeta, abstractmethod
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt


class Organismo:
    """Clase abstracta organismo de las que heredaran distintas clases
        organismo con distinta complejidad. Comparten los metodos:
        -movimiento
        -gen_coord_ini
    """

    # Colores de los plots
    color_vision = "green"
    color_explotacion = "red"
    color_organismo = "maroon"
    color_explotados = "black"
    color_area_explotada = "coral"
    color_area_visualizada = "peachpuff"

    opacidad_area = .02
    opacidad = .2

    # Clase abstracta
    __metaclass__ = ABCMeta

    def __init__(self, r_explotacion, r_sensibilidad=0, name="Organismo"):

        self.name = name
        self.r_sensibilidad = r_sensibilidad
        self.r_explotacion = r_explotacion
        self.modelo = None
        self.espacio = None
        self.objetivos = None

        self.posicion = (0,0)

        """if len(tam_espacio)!=2:
            raise ValueError("Se debe pasar una lista con el ancho y largo del espacio.")
        self.ancho = tam_espacio[0]
        self.largo = tam_espacio[1]
        self.gen_coord_ini() #Llamamos al generador de coordenadas iniciales"""

    @abstractmethod
    def movimiento(self):
        pass

    @abstractmethod
    def gen_coord_ini(self):
        pass

    @abstractmethod
    def inicializar(self):
        pass

    @abstractmethod
    def step(self):
        pass

    def add_modelo(self, modelo):

        self.modelo = modelo
        self.espacio = modelo.espacio
        self.objetivos = modelo.objetivos

        self.inicializar()


    def plot(self, ax=None):

        if ax is None:
            ax = plt.gca()

        puntos = self.espacio.coordenadas_equivalentes(self.posicion)

        # Dibujamos areas de las zonas
        for punto in puntos:
            zona = plt.Circle(punto, self.r_sensibilidad,
                              color=Organismo.color_vision,
                              alpha=Organismo.opacidad)
            ax.add_artist(zona)

            zona = plt.Circle(punto, self.r_explotacion,
                              color=Organismo.color_explotacion,
                              alpha=Organismo.opacidad)
            ax.add_artist(zona)


        zona_vision = self.objetivos.objetivos(r=self.r_sensibilidad,
                                               coordenada=self.posicion)

        if len(zona_vision) != 0:
            ax.scatter(zona_vision[:,0],zona_vision[:,1],
                       c=Organismo.color_vision)

        zona_explotacion = self.objetivos.objetivos(r=self.r_explotacion,
                                               coordenada=self.posicion)

        if len(zona_explotacion) != 0:
            ax.scatter(zona_explotacion[:,0],zona_explotacion[:,1],
                       c=Organismo.color_explotacion)


        ax.scatter(*self.posicion, c=Organismo.color_organismo)

        return ax


class OrganismoSencillo(Organismo):
    """Clase organismo sencillo con movimiento aleatorio
        y una unidad de tiempo por movimiento y sin radio de sensibilidad"""

    def __init__(self, r_explotacion=1):

        super().__init__(r_explotacion, name="Organismo Sencillo")

    def plot_trayectoria(self, ax=None):


        if len(self.trayectoria) > 1:
            trayectoria = np.array(self.trayectoria)
            trayectoria_real = np.array(self.trayectoria_real)

            self.espacio.plot_trayectoria(trayectoria, trayectoria_real, ax,
                                          Organismo.color_organismo)

        return ax

    def plot_explotados(self, ax=None):

        if ax is None:
            ax = plt.gca()

        ax.scatter(self.explotados[:,0], self.explotados[:,1],
                   c=Organismo.color_explotados)

        return ax

    def plot_area_explotada(self, ax=None):
        if ax is None:
            ax = plt.gca()

        for p in self.trayectoria:

            zona = plt.Circle(p, self.r_explotacion,
                              color=Organismo.color_area_explotada,
                              alpha=Organismo.opacidad_area)
            ax.add_artist(zona)

        return ax

    def plot_area_visualizada(self, ax=None):
        if ax is None:
            ax = plt.gca()

        for p in self.trayectoria:

            zona = plt.Circle(p, self.r_sensibilidad,
                              color=Organismo.color_area_visualizada,
                              alpha=Organismo.opacidad_area)
            ax.add_artist(zona)

        return ax


    def gen_coord_ini(self):

        x = np.random.uniform(*self.espacio.ejex)
        y = np.random.uniform(*self.espacio.ejey)

        return np.array((x,y))


    def inicializar(self):

        self.posicion = self.gen_coord_ini()
        self.explotados = np.empty((0,2))

        self.espacio_recorrido = 0
        self.objetivos_explotados = 0
        self.tiempo = 0
        self.trayectoria = [self.posicion.copy()]
        self.trayectoria_real = [self.posicion.copy()]


    def step(self):
        self.tiempo += 1

        x = self.movimiento()

        # Actualizamos distancia recorrida
        self.espacio_recorrido += np.linalg.norm(x - self.posicion)

        # Actualizamos posicion
        self.posicion = self.espacio.coordenadas(self.posicion, x)

        self.trayectoria.append(self.posicion)
        self.trayectoria_real.append(x)

        indices = self.objetivos(r=self.r_explotacion,
                                 coordenada=self.posicion, return_index=True)

        if len(indices) > 0:
            explotados = self.objetivos.explotar_objetivo(indices)
            self.objetivos_explotados += len(explotados)

            self.explotados = np.vstack((self.explotados,
                                         self.objetivos.lista_objetivos[indices]))


class OrganismoSencilloV2(OrganismoSencillo):
    """Variante de Organismo sencillo el cual en una unidad de tiempo o avanza
    o come pero no ambas
    """

    def step(self):
        self.tiempo += 1

        indices = self.objetivos(r=self.r_explotacion,
                                 coordenada=self.posicion, return_index=True)

        if len(indices) > 0:
            explotados = self.objetivos.explotar_objetivo(indices)
            self.objetivos_explotados += len(explotados)

            self.explotados = np.vstack((self.explotados,
                                         self.objetivos.lista_objetivos[indices]))

        else: # Si no hay comida se mueve
            x = self.movimiento()

            # Actualizamos distancia recorrida
            self.espacio_recorrido += np.linalg.norm(x - self.posicion)

            # Actualizamos posicion
            self.posicion = self.espacio.coordenadas(self.posicion, x)

            self.trayectoria.append(self.posicion)
            self.trayectoria_real.append(x)

class RandomWalker(OrganismoSencillo):

    def __init__(self, r_explotacion=1., std=1.):

        self.std = std

        super().__init__(r_explotacion)

    def movimiento(self):
        return  self.posicion + np.random.normal(scale=self.std, size=2)


class LevyFlight(OrganismoSencillo):

    def __init__(self, r_explotacion=1., a=.5, b=1.,loc=0., scale=1.):

        self.a = a
        self.b = b
        self.loc = loc
        self.scale = scale
        self.levy = st.levy_stable(a, b, loc, scale)

        super().__init__(r_explotacion)

    def movimiento(self):


        d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)
        angulo = np.random.uniform(0,2*np.pi)

        mov = d * np.array((np.cos(angulo), np.sin(angulo)))

        return  self.posicion + mov

class RandomWalkerV2(OrganismoSencilloV2):

    def __init__(self, r_explotacion=1., std=1.):

        self.std = std

        super().__init__(r_explotacion)

    def movimiento(self):
        return  self.posicion + np.random.normal(scale=self.std, size=2)


class LevyFlight(OrganismoSencilloV2):

    def __init__(self, r_explotacion=1., a=.5, b=1.,loc=0., scale=.1):

        self.a = a
        self.b = b
        self.loc = loc
        self.scale = scale
        self.levy = st.levy_stable(a, b, loc, scale)

        super().__init__(r_explotacion)

    def movimiento(self):


        d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)

        angulo = np.random.uniform(0,2*np.pi)

        mov = d * np.array((np.cos(angulo), np.sin(angulo)))

        return  self.posicion + mov
