

from abc import ABCMeta, abstractmethod

from .estadistica import *

import numpy as np
import types

from .plots import *
from .plots_temp import *

class Distancias(Estadistica):
    """Estadistica para almacenar los elementos explotados en cada paso"""

    def inicializar_simulaciones(self, numero_simulaciones, closing_time):
        for organismo in self.modelo:
            organismo.medias_distancias = np.zeros(closing_time)
            organismo.std_distancias = np.zeros(closing_time)
            add_metodo(organismo, plot_distancias)

    def inicializar(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.distancias = np.empty(closing_time)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.distancias[t] = organismo.espacio_recorrido

    def finalizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.medias_distancias += organismo.distancias
            organismo.std_distancias += organismo.distancias**2

    def finalizar_bloque(self):

        for organismo in self.modelo:
            organismo.medias_distancias /= self.modelo.n_simulaciones
            organismo.std_distancias /= self.modelo.n_simulaciones
            organismo.std_distancias -= organismo.medias_distancias**2
            organismo.std_distancias = np.sqrt(organismo.std_distancias)

class RadioDifusionTiempo(Estadistica):
    """Clase para recolectar el radio de difusion a lo largo del tiempo.
    """

    def inicializar_simulaciones(self, numero_simulaciones, closing_time):
        
        for organismo in self.modelo:
            organismo.medias_radio = np.zeros(closing_time)
            organismo.std_radio = np.zeros(closing_time)
            add_metodo(organismo, plot_radio_difusion_tiempo)

    def inicializar(self, closing_time, n_simulacion):
        
        for organismo in self.modelo:
            organismo.radio_difusion = np.zeros(closing_time)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            radio_actual = np.linalg.norm(organismo.posicion_inicial_simulacion - organismo.posicion_real)
            organismo.radio_difusion[t] = max(organismo.radio_difusion[t-1], radio_actual)

    def finalizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.medias_radio += organismo.radio_difusion
            organismo.std_radio += organismo.radio_difusion**2

    def finalizar_bloque(self):

        for organismo in self.modelo:
            organismo.medias_radio /= self.modelo.n_simulaciones
            organismo.std_radio /= self.modelo.n_simulaciones
            organismo.std_radio -= organismo.medias_radio**2
            organismo.std_radio = np.sqrt(organismo.std_radio)

class EstadisticaTiempo(Estadistica):
    """Estadistica para calcular a lo largo del tiempo la media y la desviacion
        estandar de un parametro.
        """
    
    def __init__(self, name):
        """
            name: Nombre del parametro
            parametros: Lista con las variaciones del parametro del plot
            n_organismo: Numero de organismos que habra en el sistema
            
            """
        self.name = name
    
    def inicializar_simulaciones(self, numero_simulaciones, closing_time):

        for organismo in self.modelo:
            organismo.medias_param = np.zeros(closing_time)
            organismo.stds_param = np.zeros(closing_time)
            add_metodo(organismo, plot_medias_tiempo)

    def inicializar(self, closing_time, n_simulacion):

        for organismo in self.modelo:
            organismo.parametro = np.zeros(closing_time)

    def actualizar(self, t, n_simulacion):
        
        for organismo in self.modelo:
            organismo.parametro[t] = getattr(organismo, self.name)

    def finalizar(self, t, n_simulacion):
        
        for organismo in self.modelo:
            organismo.medias_param += organismo.parametro
            organismo.stds_param += organismo.parametro**2

    def finalizar_bloque(self):
        
        for organismo in self.modelo:
            organismo.medias_param /= self.modelo.n_simulaciones
            organismo.stds_param /= self.modelo.n_simulaciones
            organismo.stds_param -= organismo.medias_param**2
            organismo.stds_param = np.sqrt(organismo.stds_param)

class EstadisticaAreaTemp(Estadistica):
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


    def inicializar(self, closing_time, n_simulacion):
        """ Inicializa el organismo antes de cada simulacion """
        for organismo in self.modelo:
            # Crea la matriz de discretizacion del espacio
            organismo.MatrizArea = self.modelo.espacio.area_matrix(dx=self.dx,
                                                                   dy=self.dy)
                
    def actualizar(self, t, n_simulacion):
        
        # En cada paso actualiza la matriz de area
        for organismo in self.modelo:
            self.modelo.espacio.actualizar_matriz(organismo.posicion,
                                  organismo.radio_area,
                                  organismo.MatrizArea)
            f, c = organismo.MatrizArea.shape
            tam_malla = f*c
            area= np.sum(organismo.MatrizArea > 0)/tam_malla
            organismo.ratioExplotadosArea = organismo.n_explotados/area
            rep = np.sum(organismo.MatrizArea > 2)/tam_malla
            
            organismo.areaRecorrida = area
            organismo.areaRep = rep
            
            # Ratio area entre area recorrida ponderando repeticion
            organismo.ratioRepeticion = area/np.sum(organismo.MatrizArea)
            # Comido/Area explorada
            organismo.ratioExplotadosArea = organismo.n_explotados/area
            
            organismo.ratioRepetidoRecorrido = rep/area
    
    def finalizar(self, t, s):
        pass

class TiempoEnExplotar(Estadistica):
    def __init__(self, dx=None, dy=None, r=None):
        
        super().__init__()
    
    def inicializar_simulaciones(self, n_simulacion, closing_time):
        """ Inicializa el organismo antes de las simulaciones"""
        
        for organismo in self.modelo:
            organismo.medias_tiempo_explotar = 0
            organismo.tiempos_explotar = np.zeros(n_simulacion)
    
    def finalizar(self, t, s):
        for organismo in self.modelo:
            organismo.tiempos_explotar[s] = t

    def finalizar_bloque(self):
    
        for organismo in self.modelo:
            organismo.medias_tiempo_explotar = np.mean(organismo.tiempos_explotar)
