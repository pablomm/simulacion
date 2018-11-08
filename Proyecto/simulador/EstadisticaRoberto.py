from .estadistica import Estadistica,Trayectoria
import numpy as np
from .plots import *
class EstadisticaArea(Estadistica):
    def __init__(self):
        super().__init__()

    def inicializar(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.MatrizArea = self.modelo.espacio.areaMatrix(organismo.r_explotacion)
        
        self.datos = np.empty(n_simulacion)

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            pos = self.modelo.espacio.getFilaColumnaAreaMatrix(organismo.posicion,organismo.r_explotacion)
            #print(int(pos[0]))
            organismo.MatrizArea[int(pos[0]), int(pos[1])] +=1
    def finalizar(self, t, s):
        for organismo in self.modelo:
            [f,c] = np.shape(organismo.MatrizArea)
            valor=sum(sum(organismo.MatrizArea > 0))/(f*c)
            self.datos[s] = valor


"""class CalcularVariarAreaConTiempo(VariacionParametroBloques):

    def __init__ (self):
        super().__init__("")
"""