
import abc
import math

import numpy as np
import matplotlib.pyplot as plt



import itertools


class Espacio:
    """Clase general para el espacio de la simulacion.
    Contendra metodos para obtener las coordenadas transformadas en el
    espacio de busqueda, y en espacios modulares para obtener las coordenadas
    equivalentes.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, x, y, name="Espacio"):
        """Constructor del espacio.
            Args:
                x: limites del eje x del espacio, si se pasa un numero se tomara
                    (0,x) como limite
                y: limites del eje y del espacio, si se pasa un numero se tomara
                    (0,y) como limite
                name: Nombre del espacio.
        """

        if np.isscalar(x):
            x = np.array((0, x))

        if np.isscalar(y):
            y = np.array((0, y))

        self.__x = x
        self.__y = y
        self.__tipo = name

    @property
    def ejex(self):
        return self.__x

    @property
    def ejey(self):
        return self.__y

    @property
    def size(self):
        return [(self.__x[1] - self.__x[0]), (self.__y[1] - self.__y[0])]

    def __str__(self):
        return(self.__tipo + "\n" + np.zeros((*self.size)))

    @abc.abstractmethod
    def coordenadas_equivalentes(self, coordenada):
        pass

    @abc.abstractmethod
    def coordenadas(self, iniciales, finales):
        pass

    @abc.abstractmethod
    def plot_trayectoria(self, trayectoria, trayectoria_real, ax=None, c=None):
        pass

    def calcular_angulo_mov(self, inicial, final):

        y = final[1]-inicial[1]
        x = final[0]-inicial[0]

        return math.atan2(y, x)

    def plot(self, ax=None):

        if ax is None:
            ax = plt.gca()

        ax.set_xlim(self.__x)
        ax.set_ylim(self.__y)
        size = self.size
        #ax.set_aspect(size[0]/size[1])
        ax.set_aspect(1.)

class EspacioToroidalFinito(Espacio):

    def __init__(self, x, y):
        super().__init__(x, y, "Espacio toroidal finito")

    def _estabilizar_en_rango(self, objetivo, rango, posiciones):
        res = objetivo
        if objetivo < posiciones[0]:
            res = posiciones[1] - abs(objetivo) % rango
        elif objetivo > posiciones[1]:
            res = posiciones[0] + abs(objetivo) % rango
        return res

    def coordenadas_equivalentes(self, coordenada):

        size = self.size

        puntos_equivalentes = itertools.product((0, -size[0], size[0]),
                                                (0, -size[1], size[1]))

        puntos = np.array(list(puntos_equivalentes))

        puntos += np.array(coordenada)

        return puntos

    def coordenadas(self, iniciales, finales):

        X, Y = self.size

        return np.array((self._estabilizar_en_rango(finales[0], X, self.ejex),
                         self._estabilizar_en_rango(finales[1], Y, self.ejey)))

    def plot_trayectoria(self, trayectoria, trayectoria_real, ax=None, c=None):
        """Dibuja una trayectoria en el espacio"""

        if ax is None:
            ax = plt.gca()

        trayectoria_real = trayectoria_real.copy()
        x = self.ejex
        y = self.ejey
        s = self.size

        j = 0
        for i in range(len(trayectoria)):
            if np.equal(trayectoria[i], trayectoria_real[i]).all(): continue

            ax.plot(trayectoria_real[j:i+1,0], trayectoria_real[j:i+1,1], c=c)

            if i > 1:

                j = i - 1
                if trayectoria_real[i,0] < x[0]:
                    trayectoria_real[j,0] += s[0]
                elif trayectoria_real[i,0] > x[1]:
                    trayectoria_real[j,0] -= s[0]

                if trayectoria_real[i,1] < y[0]:
                    trayectoria_real[j,1] += s[1]
                elif trayectoria_real[i,1] > y[1]:
                    trayectoria_real[j,1] -= s[1]
            else:

                j = i

            trayectoria_real[i] = trayectoria[i]


        ax.plot(trayectoria_real[j:i+1,0], trayectoria_real[j:i+1,1], c=c)

        return ax


class EspacioFinito(Espacio):

    def __init__(self, x, y):
        super().__init__(x, y, "Espacio finito")


    def coordenadas_equivalentes(self, coordenada):

        return np.array([coordenada])

    def coordenadas(self, iniciales, finales):

        x = min(max(finales[0], self.ejex[0]), self.ejex[1])
        y = min(max(finales[1], self.ejey[0]), self.ejey[1])

        return np.array((x,y))

    def plot_trayectoria(self, trayectoria, trayectoria_real, ax=None, c=None):
        """Dibuja una trayectoria en el espacio"""

        if ax is None:
            ax = plt.gca()


        ax.plot(trayectoria[:,0], trayectoria[:,1], c=c)

        return ax
