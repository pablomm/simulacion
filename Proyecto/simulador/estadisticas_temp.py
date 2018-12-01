

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
            organismo.medias = np.zeros(closing_time)
            organismo.std = np.zeros(closing_time)
            add_metodo(organismo, plot_medias_tiempo)

    def inicializar(self, closing_time, n_simulacion):

        for organismo in self.modelo:
            organismo.parametro = np.zeros(closing_time)

    def actualizar(self, t, n_simulacion):
        
        for organismo in self.modelo:
            organismo.parametro[t] = getattr(organismo, self.name)

    def finalizar(self, t, n_simulacion):
        
        for organismo in self.modelo:
            organismo.medias += organismo.parametro
            organismo.std += organismo.parametro**2

    def finalizar_bloque(self):
        
        for organismo in self.modelo:
            organismo.medias /= self.modelo.n_simulaciones
            organismo.std /= self.modelo.n_simulaciones
            organismo.std -= organismo.medias**2
            organismo.std = np.sqrt(organismo.std)
