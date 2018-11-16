
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
    __metaclass__ = ABCMeta

    # Colores de los plots
    color_vision = "green"
    color_explotacion = "red"
    color_organismo = "maroon"
    color_explotados = "black"
    color_area_explotada = "coral"
    color_area_visualizada = "peachpuff"
    opacidad_area = .05
    opacidad = .2


    def __init__(self, r_explotacion, r_sensibilidad=0, posicion=None,
                 name="Organismo"):

        self.name = name
        self.r_sensibilidad = r_sensibilidad
        self.r_explotacion = r_explotacion
        self.modelo = None
        self.espacio = None
        self.objetivos = None
        self.posicion_inicial = posicion
        self.posicion = posicion
        self.posicion_real = posicion

        # Datos basicos para las estadisticas
        self.explotados_step = None
        self.n_explotados = 0
        self.espacio_recorrido = 0
        self.tiempo = 0

    @abstractmethod
    def movimiento(self):
        pass

    @abstractmethod
    def inicializar(self):
        pass

    @abstractmethod
    def step(self):
        pass

    def gen_coord_ini(self):
        """Genera coordenadas inicialies si no se han fijado al inicializarse.
        Seran un punto aleatorio (uniforme) en el espacio"""

        if self.posicion_inicial is not None:
            return np.asarray(self.posicion_inicial)

        x = np.random.uniform(*self.espacio.ejex)
        y = np.random.uniform(*self.espacio.ejey)

        return np.array((x,y))

    def add_modelo(self, modelo):
        """ Incluir un modelo en el organismo"""
        self.modelo = modelo
        self.espacio = modelo.espacio
        self.objetivos = modelo.objetivos
        self.posicion = self.gen_coord_ini()
        self.posicion_inicial_simulacion = self.posicion
        self.posicion_real = self.posicion

    def clear(self):

        self.posicion = self.gen_coord_ini()
        self.posicion_inicial_simulacion = self.posicion
        self.posicion_real = self.posicion
        self.explotados_step = None
        self.n_explotados = 0
        self.espacio_recorrido = 0
        self.tiempo = 0


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

    def __init__(self, r_explotacion=1, posicion=None, stop_eat=False,
                 name="Organismo Sencillo"):

        self.stop_eat = stop_eat

        super().__init__(r_explotacion, posicion=posicion, name=name)


    def step(self):

        indices = self.objetivos(r=self.r_explotacion,
                                 coordenada=self.posicion, return_index=True)


        self.explotados_step = np.empty((0,2))

        if len(indices) > 0:
            explotados = self.objetivos.explotar_objetivo(indices)

            self.n_explotados += len(explotados)
            self.explotados_step = self.objetivos.lista_objetivos[indices]

        # Solo se mueve si no hay comida o si se ha definido que por
        # comer no pierde un turno
        if not self.stop_eat or len(indices) == 0:
            x = self.movimiento()
            self.posicion_real = x

            # Actualizamos distancia recorrida
            self.espacio_recorrido += np.linalg.norm(x - self.posicion)
            # Actualizamos posicion
            self.posicion = self.espacio.coordenadas(self.posicion, x)

            #self.trayectoria.append(self.posicion)
            #self.trayectoria_real.append(x)


class RandomWalker(OrganismoSencillo):

    def __init__(self, r_explotacion=1., std=1., stop_eat=False, posicion=None):

        self.std = std

        super().__init__(r_explotacion, stop_eat=stop_eat, posicion=posicion,
                         name="Random Walker")

    def movimiento(self):
        return  self.posicion + np.random.normal(scale=self.std, size=2)



class LevyFlight(OrganismoSencillo):

    def __init__(self, r_explotacion=1., a=1.5, b=0., loc=0., scale=1.,
                 maximo=np.Inf, minimo=0, stop_eat=False, posicion=None):

        self.a = a
        self.b = b
        self.loc = loc
        self.scale = scale
        self.maximo = maximo
        self.minimo = minimo
        self.levy = st.levy_stable(a, b, loc, scale)

        super().__init__(r_explotacion, stop_eat=stop_eat, posicion=posicion,
                         name="Levy Flight")

    def movimiento(self):

        d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)
        absd = abs(d)
        while absd > self.maximo or absd <  self.minimo:
            d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)
            absd = abs(d)

        angulo = np.random.uniform(0,2*np.pi)

        mov = d * np.array((np.cos(angulo), np.sin(angulo)))

        return  self.posicion + mov


class OrganismoVFija(Organismo):
    """Clase organismo sencillo con movimiento aleatorio
        y una unidad de tiempo por movimiento y sin radio de sensibilidad"""

    def __init__(self, velocidad=1., r_explotacion=1, posicion=None,
                 stop_eat=False, name="Organismo Velocidad Fija"):

        self.stop_eat = stop_eat
        self.theta = 0
        self.remaining = 0
        self.velocidad = velocidad

        super().__init__(r_explotacion, posicion=posicion, name=name)


    def step(self):

        indices = self.objetivos(r=self.r_explotacion,
                                 coordenada=self.posicion, return_index=True)


        self.explotados_step = np.empty((0,2))

        if len(indices) > 0:
            explotados = self.objetivos.explotar_objetivo(indices)

            self.n_explotados += len(explotados)
            self.explotados_step = self.objetivos.lista_objetivos[indices]

        # Solo se mueve si no hay comida o si se ha definido que por
        # comer no pierde un turno
        if not self.stop_eat or len(indices) == 0:

            self.espacio_recorrido += self.velocidad
            v = self.velocidad
            while v > 0:

                if self.remaining <= 0:
                    self.generar_movimiento()

                if v <= self.remaining:

                    x = self.posicion + v*np.array((np.cos(self.theta),
                                                    np.sin(self.theta)))
                    self.remaining -= v
                    self.posicion_real = x
                    self.posicion = self.espacio.coordenadas(self.posicion, x)
                    v = 0

                else:
                    x = self.posicion + self.remaining*np.array(
                                    (np.cos(self.theta),np.sin(self.theta)))
                    v -= self.remaining
                    self.remaining = 0
                    self.posicion_real = x
                    self.posicion = self.espacio.coordenadas(self.posicion, x)


class RandomWalkerVFija(OrganismoVFija):

    def __init__(self, r_explotacion=1., velocidad=1., mu=0., std=1.,
                 stop_eat=False, posicion=None):

        self.std = std
        self.mu = mu

        super().__init__(r_explotacion=r_explotacion, velocidad=velocidad, stop_eat=stop_eat,
                         posicion=posicion, name="Random Walker V Fija")

    def generar_movimiento(self):

        self.theta = np.random.uniform(0,2*np.pi)
        self.remaining = np.linalg.norm(np.random.normal(scale=self.std,
                                                         loc=self.mu, size=2))

class LevyFlightVFija(OrganismoVFija):
    
    def __init__(self, r_explotacion=1., velocidad=1., a=1.5, b=0., loc=0., scale=1.,
                 maximo=np.Inf, minimo=0, stop_eat=False, posicion=None):
        
        self.a = a
        self.b = b
        self.loc = loc
        self.scale = scale
        self.maximo = maximo
        self.minimo = minimo
        self.levy = st.levy_stable(a, b, loc, scale)
        
        super().__init__(r_explotacion=r_explotacion, velocidad=velocidad, stop_eat=stop_eat,
                         posicion=posicion, name="Levy Flight")
    
    def generar_movimiento(self):
        
        self.theta = np.random.uniform(0,2*np.pi)
        d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)
        absd = abs(d)
        d = st.levy_stable.rvs(self.a, self.b, self.loc, self.scale)
        d = abs(d)
        
        self.remaining = min(max(d,self.minimo), self.maximo)

