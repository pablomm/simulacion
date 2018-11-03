

from abc import abstractmethod, ABCMeta

import numpy as np
import matplotlib.pyplot as plt


class Objetivos:
    """Clase para abstraer los objetivos en el sistema.
        Se encargara de manejar la obtencion de objetivos.
    """

    __metaclass__ = ABCMeta

    def __init__(self, numero_objetivos, espacio):


        self.espacio = espacio
        # Inicializamos objetivos del sistema
        self.__n = numero_objetivos
        self.inicializar()

    def inicializar(self):
            objetivos, libres, n = self.inicializar_objetivos(self.__n)
            self.lista_objetivos = objetivos
            self.libres  = libres
            self._numero_objetivos = n

    @property
    def numero_objetivos(self):
        """Devuelve el numero de objetivos actuales en el sistema"""
        return self._numero_objetivos

    @abstractmethod
    def inicializar_objetivos(self, numero_objetivos):
        """Funcion para inicializar la lista de objetivos

            Args:
                numero_objetivos: Numero de objetivos a generar

            Returns:
                Lista de coordenadas con posicion de objetivos
                Lista con
        """
        pass

    @abstractmethod
    def explotar_objetivo(self, coordenadas):
        """Funcion para intentar explotar una lista de objetivos

            Args:
                coordenadas: Lista de posiciones de objetivos a explotar

            Returns:
                Lista con objetivos explotados
        """
        pass

    def actualizar_objetivos(self):
        """Funcion para actualizar los objetivos en cada paso de la simulacion
            Por defecto no hace nada
        """
        pass

    def objetivos(self, *, r=None, coordenada=None, return_index=False):
        """Devuelve la lista de coordenadas con los objetivos.
            Si se especifica r devolvera los objetivos dentro del radio

            Args:
                r (numeric): Radio de objetivos a devolver
                coordenada (tuple): Tupla con posicion
                return_index (bool): Si es True devuelve los indices de los
                    objetivos en lugar de las coordenadas de estos.
        """

        if r is None:
            return self.lista_objetivos


        coordenadas = self.espacio.coordenadas_equivalentes(coordenada)

        objs = np.full(len(self.lista_objetivos), False)

        # Calculamos las distancias con cada una de las coordenadas equivalentes
        for coordenada in coordenadas:
            distancias = np.linalg.norm(self.lista_objetivos - coordenada,
                                        axis=1)
            cercanos = distancias <= r
            np.logical_or(objs, cercanos, out=objs)

        np.logical_and(objs, self.libres != 0, out=objs)

        if return_index:
            return np.argwhere(objs).flatten()

        return self.lista_objetivos[objs]

    def __call__(self, *, r=None, coordenada=None, return_index=False):

        return self.objetivos(r=r, coordenada=coordenada,
                              return_index=return_index)


    def plot(self, ax=None, **kwargs):
        """Plotea los objetivos"""

        if ax is None:
            ax = plt.gca()

        no_explotados = self.libres != 0

        ax.scatter(self.lista_objetivos[no_explotados][:,0],
                   self.lista_objetivos[no_explotados][:,1],
                   **kwargs)

        return ax


class ObjetivosDesechables(Objetivos):
    """Clase para manejar objetivos que se destruyen al obtenerse.
        Cada objetivo tiene un numero de usos finito y al explotarse se
        destruyen.

        Esta clase no es instanciable, no define un metodo para inicializar
        los objetivos, usar ObjetivosUniformes o ObjetivosAgrupados
        """

    def __init__(self, numero_objetivos, espacio, usos=1):

        self.usos = usos
        super().__init__(numero_objetivos*usos, espacio)


    def explotar_objetivo(self, indices):

        #Explota los enjetivos pasados en la lista de coordenadas.

        if len(indices) == 0:
            return np.empty((0,2))

        self.libres[indices] -= 1
        self._numero_objetivos -= len(indices)

        return self.lista_objetivos[indices]



class ObjetivosUniformes(ObjetivosDesechables):
    """Clase para generar objetivos desechables uniformemente en el espacio.
        Para inicializar:
            numero_objetivos: Numero de objetivos a crear.
            espacio: Instancia de un espacio.
            usos: Numero de usos que tendra cada objetivo, por defecto 1.
    """

    def inicializar_objetivos(self, numero_objetivos):
        """Inicializa los objetivos en el espacio de manera uniforme"""

        # Genera objetivos distribuidos uniformemente en el espacio
        lista_objetivos = np.empty((numero_objetivos,2))

        lista_objetivos[:,0] = np.random.uniform(*self.espacio.ejex,
                                                  size=numero_objetivos)

        lista_objetivos[:,1] = np.random.uniform(*self.espacio.ejey,
                                                  size=numero_objetivos)

        libres = np.full(numero_objetivos, self.usos)


        return lista_objetivos, libres, self.usos*numero_objetivos


class ObjetivosAgrupados(ObjetivosDesechables):
    """Clase para generar objetivos desechables distribuidos en el espacio
        en nucleos con distribucion normal multivariante.

        Para inicializar:
            numero_objetivos: Numero de objetivos a crear.
            espacio: Instancia de un espacio.
            numero_grupos: Numero de grupos
            usos: Numero de usos que tendra cada objetivo, por defecto 1.
            std: Desviacion estandar de los grupos
            grupos: Coordenadas de los grupos, si no se generaran aleatoriamente
    """

    color_grupos = "skyblue"
    opacidad_grupos = .35

    def __init__(self, numero_objetivos_grupo, espacio, numero_grupos=1, std=1.,
                 usos=1, grupos = None):


        self.numero_grupos=numero_grupos
        self.std_grupos = std
        self.grupos = grupos

        super().__init__(numero_objetivos_grupo, espacio, usos)

    def inicializar_objetivos(self, numero_objetivos_grupo):
        """Inicializa los objetivos en el espacio de manera uniforme"""

        numero_objetivos = numero_objetivos_grupo * self.numero_grupos

        # Genera objetivos agrupados
        lista_objetivos = np.empty((numero_objetivos, 2))

        # Inicializamos los centros de los grupos
        if self.grupos is None:
            self.grupos = np.empty((self.numero_grupos, 2))

            self.grupos[:,0] = np.random.uniform(*self.espacio.ejex,
                                                  size=self.numero_grupos)

            self.grupos[:,1] = np.random.uniform(*self.espacio.ejey,
                                                      size=self.numero_grupos)
        else:
            self.grupos = np.array(self.grupos, dtype=float).reshape(
                (self.numero_grupos, 2))

        # Inicializamos cada uno de los grupos
        for i in range(self.numero_grupos):
            a = i*numero_objetivos_grupo
            b = a + numero_objetivos_grupo
            lista_objetivos[a:b, 0] = np.random.normal(loc=self.grupos[i,0],
                                                       scale=self.std_grupos,
                                                       size=numero_objetivos_grupo)


            lista_objetivos[a:b, 1] = np.random.normal(loc=self.grupos[i,1],
                                                        scale=self.std_grupos,
                                                        size=numero_objetivos_grupo)

        lista_objetivos[:,0] = np.mod(
            lista_objetivos[:,0] - self.espacio.ejex[0],
            self.espacio.size[0]) + self.espacio.ejex[0]

        lista_objetivos[:,1] = np.mod(
            lista_objetivos[:,1] - self.espacio.ejey[0],
            self.espacio.size[1]) + self.espacio.ejey[0]

        libres = np.full(numero_objetivos, self.usos)

        return lista_objetivos, libres, numero_objetivos

    def plot_grupos(self, ax=None, color=None, alpha=None, r=1.96):
        """Dibuja un sombreado centrados en los nucleos de puntos, con un radio
            de r*std

            Args:
                ax: Axis de matplotlib (opcional)
                color: Color de las zonas
                alpha: Opacidad
                r: Constante proporcional a los radios, por defecto 1.96 que
                    correspondiente al cuantil 95 de la normal.
        """

        if ax is None:
            ax = plt.gca()

        if color is None:
            color = ObjetivosAgrupados.color_grupos

        if alpha is None:
            alpha = ObjetivosAgrupados.opacidad_grupos


        for grupo in self.grupos:
            centros = self.espacio.coordenadas_equivalentes(grupo)

            for centro in centros:
                p = plt.Circle(centro, r*self.std_grupos, color=color,
                               alpha=alpha)
                ax.add_artist(p)

        return ax