

from abc import ABCMeta, abstractmethod

import numpy as np
import types

from .plots import *

def add_metodo(instancia, funcion):
    """Añade un metodo a una instancia de una clase
        podra ser llamado como instancia.nombre_funcion() y recibira como
        primer argumento la instancia"""

    setattr(instancia, funcion.__name__, types.MethodType(funcion, instancia))

class Estadistica:
    """Clase para definir una estadistica que recopile datos del modelo
    durante la simulacion.

    Añaden metodos y variables a los organismo y otros objetos del modelo y
    recolectan en estas estructuras estadisticas durante la simulacion.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.modelo = None


    def add_modelo(self, modelo):
        """Vincula la estadistica con un modelo"""
        self.modelo = modelo

    @abstractmethod
    def inicializar(self, closing_time, n_simulacion):
        """Prepara los objetos del modelo para recopilar los datos de la
            estadistica al inicio de cada simulacion"""
        pass

    @abstractmethod
    def actualizar(self, t, n_simulacion):
        """Actualiza los datos de la estadistica en el modelo en un paso de
            una simulacion"""
        pass

    @abstractmethod
    def finalizar(self, end, n_simulacion):
        """Finaliza las estadisticas al acabar una simulacion"""
        pass


    def inicializar_simulaciones(self, numero_simulaciones):
        """Llamado al principio de las simulaciones para preparar la
        estadistica"""
        pass

    def finalizar_bloque(self):
        pass

class Trayectoria(Estadistica):
    """Clase para guardar las trayectorias.

        En cada organismo almacena la posicion real y en coordenadas del espacio
        por cada paso de la simulacion.

        Añade en los organismos los metodos plot_trayectoria, plot_step,
        plot_area_explorada y plot_area_visualizada
    """

    def inicializar(self, closing_time, n_simulacion):

        # Añade las variables donde guardara las trayectorias
        # Y las inicializa con la posicion inicial
        for organismo in self.modelo:
            organismo.trayectoria = np.zeros((closing_time + 1, 2))
            organismo.trayectoria_real = np.zeros((closing_time + 1, 2))
            organismo.trayectoria[0] = organismo.posicion
            organismo.trayectoria_real[0] = organismo.posicion

            # Metodos nuevos en organismo
            add_metodo(organismo, plot_trayectoria)
            add_metodo(organismo, plot_area_explotada)
            add_metodo(organismo, plot_area_visualizada)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.trayectoria[t+1] = organismo.posicion
            organismo.trayectoria_real[t+1] = organismo.posicion_real

    def finalizar(self, t, n_simulacion):

        # Si la simulacion acaba antes del closing time rellena todo lo sobrante
        # Con la posicion final
        for organismo in self.modelo:
            organismo.trayectoria[t+1:,:] = organismo.trayectoria[t+1]
            organismo.trayectoria_real[t+1:,:] = organismo.trayectoria_real[t+1]

class Explotados(Estadistica):
    """Estadistica para almacenar los elementos explotados en cada paso"""

    def inicializar(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.explotados = np.full(closing_time, None, dtype=object)
            add_metodo(organismo, plot_explotados)


    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            if len(organismo.explotados_step) > 0:
                organismo.explotados[t] = organismo.explotados_step

    def finalizar(self, t, n_simulacion):
        pass




class RecorridoTargets(Estadistica):
    """Estadistica para calcular a lo largo de varias simulaciones la cantidad
        de Targets entre espacio recorrido
    """

    def inicializar_simulaciones(self, n_simulaciones):

            self.recorrido_targets = np.empty((n_simulaciones,
                                               self.modelo.n_organismos))

            add_metodo(self, plot_recorrido_targets)

    def inicializar(self, closing_time, n_simulacion):
        pass

    def actualizar(self, t, n_simulacion):
        pass

    def finalizar(self, t, s):

        for i, organismo in enumerate(self.modelo):
            self.recorrido_targets[s, i] = (organismo.n_explotados /
                                            organismo.espacio_recorrido)


class RecorridoTargetsMultiple(Estadistica):
    """Estadistica para calcular a lo largo de varias simulaciones la cantidad
        de Targets entre espacio recorrido cambiando el parametro por cada estadistica

        Solo valido con 1 organismo
    """

    def __init__(self, parametros, n_organismos=1):
        self.parametros = parametros
        self.n_bloques = len(parametros)
        self.bloque_actual = -1
        self.n_organismos = n_organismos



    def add_modelo(self, modelo):
        """Vincula la estadistica con un modelo. Inicializa el vector de medias"""
        self.modelo = modelo
        self.medias = np.zeros((self.n_bloques, self.n_organismos))
        add_metodo(self, plot_medias)


    def inicializar_simulaciones(self, n_simulaciones):

        self.n_simulaciones = n_simulaciones
        self.bloque_actual += 1

    def inicializar(self, closing_time, n_simulacion):
        pass

    def actualizar(self, t, n_simulacion):
        pass

    def finalizar(self, t, s):

        for i, organismo in enumerate(self.modelo):
            self.medias[self.bloque_actual, i] += (organismo.n_explotados /
                                            organismo.espacio_recorrido)

    def finalizar_bloque(self):
            self.medias[self.bloque_actual] /= self.n_simulaciones
