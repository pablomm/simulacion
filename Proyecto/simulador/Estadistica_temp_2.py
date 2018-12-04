from abc import ABCMeta, abstractmethod

import numpy as np
import types

from .plots import *
from .plots_temp import *
from .estadistica import *
from .objetivos import ObjetivosUniformes

class EstadisticaArea1Obj(Estadistica):
    def __init__(self, dx=None, dy=None, r=None):
        """ Estadistica para calcular la matriz de areas.

            dx: Tamaño de discretizacion la malla en el eje x. Por defecto 0.1
            dy: Tamaño de discreatizacion en el eje y. Por defecto 0.1
            r: Radio del area a contar en cada paso.
        """
        super().__init__()

        self.dx = dx
        self.dy = dy
        self.radio_area = r

    def inicializar_simulaciones(self, n_simulacion, closing_time):
        """ Inicializa el organismo antes de las simulaciones"""

        for organismo in self.modelo:
            add_metodo(organismo, plot_mapa_calor)

            # Guardamos el radio con el que estamos mirando el area
            if self.radio_area is None:
                organismo.radio_area  = organismo.r_explotacion
            else:
                organismo.radio_area = self.radio_area

            organismo.areaRecorrida = np.ones(n_simulacion)
            organismo.areaRep = np.ones(n_simulacion)
            organismo.ratioRepeticion = np.ones(n_simulacion)
            organismo.tiempo_hasta_objetivo = np.ones(n_simulacion)
            

    def inicializar(self, closing_time, n_simulacion):
        """ Inicializa el organismo antes de cada simulacion """
        for organismo in self.modelo:
            # Crea la matriz de discretizacion del espacio
            organismo.MatrizArea = self.modelo.espacio.area_matrix(dx=self.dx,
                                                                   dy=self.dy)
            organismo.flag = True

    def actualizar(self, t, n_simulacion):

        # En cada paso actualiza la matriz de area

        for organismo in self.modelo:
            if organismo.n_explotados == 0:
                self.modelo.espacio.actualizar_matriz(organismo.posicion,
                                                  organismo.radio_area,
                                                  organismo.MatrizArea)
          

    def finalizar(self, t, s):
        """ Al final de cada simulacion guarda en la matriz"""
        for organismo in self.modelo:

            f, c = organismo.MatrizArea.shape

            # Tam malla
            tam_malla = f*c
            # Area explorada por el individuo
            area= np.sum(organismo.MatrizArea > 0)/tam_malla
            # Area repetida
            rep = np.sum(organismo.MatrizArea > 2)/tam_malla

            organismo.areaRecorrida[s] = area
            organismo.areaRep[s] = rep

            # Ratio area entre area recorrida ponderando repeticion
            organismo.ratioRepeticion[s] = area/np.sum(organismo.MatrizArea)
            organismo.tiempo_hasta_objetivo[s] =  t
        #self.modelo.objetivos = ObjetivosUniformes(1, self.modelo.espacio)
           
