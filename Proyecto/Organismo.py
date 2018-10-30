
from abc import ABCMeta, abstractmethod
import numpy as np
import scipy.stats as st
import math

class Organismo:
    """Clase abstracta organismo de las que heredaran distintas clases
        organismo con distinta complejidad. Comparten los metodos:
        -movimiento
        -gen_coord_ini
    """ 
    
    # Clase abstracta
    __metaclass__ = ABCMeta

    def __init__(self, tam_espacio):
        if len(tam_espacio)!=2:
            raise ValueError("Se debe pasar una lista con el ancho y largo del espacio.")
        self.ancho = tam_espacio[0]
        self.largo = tam_espacio[1]
        self.gen_coord_ini() #Llamamos al generador de coordenadas iniciales
    
    @abstractmethod
    def movimiento(self):
        pass
    
    @abstractmethod
    def gen_coord_ini(self):
        pass

########

class OrganismoSencillo(Organismo):
    """Clase organismo sencillo con movimiento aleatorio gaussiano
        y una unidad de tiempo por movimiento"""

    def __init__(self, tam_espacio, velocidad=1, r_sensibilidad=1):
        super().__init__(tam_espacio)
        self.velocidad = velocidad
        self.r_sensibilidad = r_sensibilidad
        #Estadisticas        
        self.espacio_recorrido = 0
        self.targets_encontrados = 0
    
    def movimiento(self):
        epsilon = 0.00001
        #Angulo de movimiento
        u1 = st.uniform().rvs()
        angulo =  2 * math.pi * u1 
        #Radio
        u2 = st.uniform().rvs()
        r = self.velocidad * math.sqrt(-2 * np.log(u2 + epsilon))
        #Nuevas coordenadas
        mov_x = r*np.cos(angulo)
        mov_y = r*np.sin(angulo)
        #Nuevas coordenadas
        nueva_coord_x = self.coord_x + mov_x
        nueva_coord_y = self.coord_y + mov_y
        #Guardo la distancia recorrida
        self.espacio_recorrido += r
        
        return [ nueva_coord_x, nueva_coord_y]

    def gen_coord_ini(self):
        #Generamos las coordenadas iniciales con una uniforme
        self.coord_x = self.ancho * st.uniform().rvs()
        self.coord_y = self.largo * st.uniform().rvs()
        
########

