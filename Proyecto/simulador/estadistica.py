

from abc import ABCMeta, abstractmethod

import numpy as np
import types

from .plots import *
from .plots_temp import *

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

    def inicializar(self, closing_time, n_simulacion):
        """Prepara los objetos del modelo para recopilar los datos de la
            estadistica al inicio de cada simulacion"""
        pass

    def actualizar(self, t, n_simulacion):
        """Actualiza los datos de la estadistica en el modelo en un paso de
            una simulacion"""
        pass

    def finalizar(self, end, n_simulacion):
        """Finaliza las estadisticas al acabar una simulacion"""
        pass


    def inicializar_simulaciones(self, numero_simulaciones, closing_time):
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

    def inicializar_simulaciones(self, numero_simulaciones, closing_time):
        for organismo in self.modelo:
            organismo.medias_explotados = np.zeros(closing_time)
            organismo.std_explotados = np.zeros(closing_time)
            add_metodo(organismo, plot_numero_explotados)

    def inicializar(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.explotados = np.full(closing_time, None, dtype=object)
            organismo.numero_explotados_t = np.zeros(closing_time)
            add_metodo(organismo, plot_explotados)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            if len(organismo.explotados_step) > 0:
                organismo.explotados[t] = organismo.explotados_step
            organismo.numero_explotados_t[t]  = organismo.n_explotados

    def finalizar(self, t, n_simulacion):

        for organismo in self.modelo:
            organismo.medias_explotados += organismo.numero_explotados_t
            organismo.std_explotados += organismo.numero_explotados_t**2

    def finalizar_bloque(self):

        for organismo in self.modelo:
            organismo.medias_explotados /= self.modelo.n_simulaciones
            organismo.std_explotados /= self.modelo.n_simulaciones
            organismo.std_explotados -= organismo.medias_explotados**2
            organismo.std_explotados = np.sqrt(organismo.std_explotados)



class TargetEspacioOrganismo(Estadistica):
    """
    Estadistica simple que añade al organismo al final de cada simulacion el
    n objetivos explotados entre el espacio recorrido.
    """

    def finalizar(self, t, n_simulacion):
        for organismo in self.modelo:
            organismo.recorrido_targets = organismo.n_explotados / organismo.espacio_recorrido




class SimulacionHistograma(Estadistica):
    """Estadistica para calcular a lo largo de varias simulaciones la cantidad
        de Targets entre espacio recorrido
    """


    def __init__(self, name):
        self.name = name
        super().__init__()

    def inicializar_simulaciones(self, n_simulaciones, closing_time):

            self.histograma = np.empty((n_simulaciones, self.modelo.n_organismos))

            add_metodo(self, plot_histograma)


    def finalizar(self, t, s):

        for i, organismo in enumerate(self.modelo):
            self.histograma[s, i] = getattr(organismo, self.name)



class VariacionParametroBloques(Estadistica):
    """Estadistica para calcular a lo largo de varias simulaciones la media y la
    variacion estandar de un parametro.
    """

    def __init__(self, name, parametros, n_organismos=1):
        """
        name: Nombre del parametro
        parametros: Lista con las variaciones del parametro del plot
        n_organismo: Numero de organismos que habra en el sistema

        """
        self.parametros = parametros
        self.n_bloques = len(parametros)
        self.n_organismos = n_organismos
        self.bloque_actual = -1
        self.name = name


    def add_modelo(self, modelo):
        """Vincula la estadistica con un modelo. Inicializa el vector de medias"""
        self.modelo = modelo
        self.medias = np.zeros((self.n_bloques, self.n_organismos))
        self.desviaciones = np.zeros((self.n_bloques, self.n_organismos))
        add_metodo(self, plot_medias)


    def inicializar_simulaciones(self, n_simulaciones, closing_time):

        self.n_simulaciones = n_simulaciones
        self.bloque_actual += 1

    def inicializar(self, closing_time, n_simulacion):
        pass

    def actualizar(self, t, n_simulacion):
        pass

    def finalizar(self, t, s):

        for i, organismo in enumerate(self.modelo):
            self.medias[self.bloque_actual, i] += getattr(organismo, self.name)
            self.desviaciones[self.bloque_actual, i] += getattr(organismo, self.name)**2


    def finalizar_bloque(self):
        self.medias[self.bloque_actual] /= self.n_simulaciones
        self.desviaciones[self.bloque_actual] /= self.n_simulaciones
        self.desviaciones[self.bloque_actual] -= self.medias[self.bloque_actual]


class RadioDifusion(Estadistica):
    """Clase para recolectar el radio de difusion.
    """

    def inicializar(self, closing_time, n_simulacion):

        # Añade las variables donde guardara las trayectorias
        # Y las inicializa con la posicion inicial
        for organismo in self.modelo:
            organismo.radio_difusion = 0
            add_metodo(organismo, plot_radio_difusion)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:

            radio_actual = np.linalg.norm(organismo.posicion_inicial_simulacion - organismo.posicion_real)

            organismo.radio_difusion = max(organismo.radio_difusion, radio_actual)



class EstadisticaArea(Estadistica):
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

            organismo.areaRecorrida = np.zeros(n_simulacion)
            organismo.areaRep = np.zeros(n_simulacion)
            organismo.ratioRepeticion = np.zeros(n_simulacion)
            organismo.ratioExplotadosArea = np.zeros(n_simulacion)
            organismo.explotados = np.zeros(n_simulacion)
            organismo.ratioRepetidoRecorrido = np.zeros(n_simulacion)


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
            # Comido/Area explorada
            organismo.ratioExplotadosArea[s] = organismo.n_explotados/area

            organismo.ratioRepetidoRecorrido[s] = rep/area
