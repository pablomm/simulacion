

from abc import ABCMeta, abstractmethod

from .estadistica import *

import numpy as np
import types

from .plots import *
from .plots_jari import *

class Distancias(Estadistica):
    """Estadistica para almacenar los elementos explotados en cada paso"""

    def inicializar_simulaciones(self, numero_simulaciones, closing_time):
        for organismo in self.modelo:
            organismo.medias_distancias = np.zeros(closing_time)
            add_metodo(organismo, plot_distancias)

    def inicializar(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.distancias = np.empty(closing_time)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.distancias[t:] = organismo.espacio_recorrido

    def finalizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.medias_distancias += organismo.distancias

    def finalizar_bloque(self):

        for organismo in self.modelo:
            organismo.medias_distancias /= self.modelo.n_simulaciones
