


from abc import ABCMeta, abstractmethod

from queue import Queue
import matplotlib.pyplot as plt


class Modelo:

    __metaclass__ = ABCMeta

    def __init__(self, espacio, objetivos):
        self.espacio = espacio
        self.objetivos = objetivos
        self.queue = Queue()
        self.n_organismos = 0


    def add_organismo(self, organismo):
        """Incluir organismo al modelo  """
        organismo.add_modelo(self)
        self.queue.put(organismo)
        self.n_organismos += 1

    def simular(self, closing_time=1e3, stop_empty=True):
        """Simula el modelo hasta alcanzar el tiempo closing_time.

            Args:
                closing_time: Tiempo Maximo a simular
                stop_empty: Detener la simulacion si no hay mas objetivos

            Returns:
                Tiempo final de la simulacion
        """

        closing_time = int(closing_time)

        for t in range(closing_time):

            print(f"Simulando {t+1}/{closing_time}", end="\r")

            for organismo in self:

                organismo.step()

            # Parar si no quedan objetivos
            if stop_empty and self.objetivos.numero_objetivos == 0:
                break

        return t

    def plot(self, ax=None, **kwargs):

        if ax is None:
            ax = plt.gca()

        self.espacio.plot(ax)
        self.objetivos.plot(ax)

        return ax

    def __iter__(self):
        """ Itera sobre los organismos"""

        for _ in range(self.n_organismos):
            organismo = self.queue.get()
            self.queue.put(organismo)
            yield organismo
