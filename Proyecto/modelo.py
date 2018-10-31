


from abc import ABCMeta, abstractmethod

from queue import Queue

from espacio import *
from objetivos import *
from organismo import *




class Modelo:

    __metaclass__ = ABCMeta

    def __init__(self, espacio, objetivos):
        self.espacio = espacio
        self.objetivos = objetivos
        self.queue = Queue()
        self.n_organismos = 0


    def add_organismo(organismo):
        organismo.add_modelo(self)
        self.queue.put(organismo)
        self.n_organismos += 1

    def simular(closing_time=1e3):

        for t in range(closing_time):
            for _ in repeat(self.n_organismos):

                organismo = self.queue.get()
                organismo.step()
                self.queue.put(organismo)



    def plot(ax=None, **kwargs):

        if ax is None:
            ax = plt.gca()

        self.espacio.plot(ax)
        self.objetivos.plot(ax)

        for organismo in self.queue()

            organismo.plot(ax)


        return ax
