

from abc import abstractmethod, ABCMeta
import numpy as np
import matplotlib.pyplot as plt


class Objetivos:
    """Clase para abstraer los objetivos en el sistema.
        Se encargara de manejar la obtencion de objetivos.
    """

    __metaclass__ = ABCMeta

    def __init__(self, numero_objetivos, tam_espacio):

        # Numero de objetivos actualmente
        self.__numero_objetivos = numero_objetivos

        # Lista con todos los objetivos
        self.lista_objetivos = self.inicializar_objetivos(numero_objetivos,
                                                            tam_espacio)

    @abstractmethod
    def inicializar_objetivos(self, numero_objetivos, tam_espacio):
        """Funcion para inicializar la lista de objetivos

            Args:
                numero_objetivos: Numero de objetivos a generar
                tam_espacio: Tupla (x,y) con tamaño del espacio

            Returns:
                Lista de coordenadas con posicion de objetivos
        """
        pass

    @abstractmethod
    def explotar_objetivo(self, coordenadas):
        """Funcion para destruir un objetivo

            Args:
                coordenadas: Posicion del objetivo a destruir

            Returns:
                True si ha conseguido obtener el objetivo o False en caso
                contrario
        """
        pass

    def objetivos(self, *, r=None, coordenadas=None, coordenada=None):
        """Devuelve la lista de coordenadas con los objetivos.
            Si se especifica r devolvera los objetidos dentro del radio"""



        if r is None:
            return self.lista_objetivos


        if coordenada is not None:
            coordenadas = [coordenada]

        objs = []


        for objetivo in self.lista_objetivos:
            for coordenada in coordenadas:
                if np.linalg.norm(objetivo - coordenada) <= r:
                    objs.append(objetivo)
                    break


        return np.array(objs)


    @property
    def numero_objetivos(self):
        """Devuelve el numero de objetivos actuales en el sistema"""
        return self.__numero_objetivos

    def plot(self, ax=None, **kwargs):
        """Plotea los objetivos"""

        if ax is None:
            ax = plt.gca()

        ax.scatter(self.lista_objetivos[:,0],
                   self.lista_objetivos[:,1],
                   **kwargs)

        return ax


class ObjetivosUniformes(Objetivos):
    """Clase para manejar objetivos que se destruyen al obtenerse y
    que se distribuyen de manera uniforme en el espacio"""

    def inicializar_objetivos(self, numero_objetivos, tam_espacio):

        # Genera objetivos distribuidos uniformemente en el espacio
        lista_objetivos = np.empty((numero_objetivos,2))

        lista_objetivos[:,0] = np.random.uniform(0, tam_espacio[0],
                                                  size=numero_objetivos)

        lista_objetivos[:,1] = np.random.uniform(0, tam_espacio[1],
                                                  size=numero_objetivos)


        return lista_objetivos

    def explotar_objetivo(self, coordenadas):

        for i, objetivo in enumerate(self.lista_objetivos):
            if np.equal(objetivo, coordenadas).all():
                self.lista_objetivos = np.delete(self.lista_objetivos, i, axis=0)
                self.__numero_objetivos -= 1
                return True


        return False