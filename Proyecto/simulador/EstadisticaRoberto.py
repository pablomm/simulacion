from .estadistica import Estadistica,Trayectoria
import numpy as np
from .plots import *
class EstadisticaArea(Estadistica):
    def __init__(self):
        super().__init__()

    def inicializar_simulaciones(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.MatrizArea = self.modelo.espacio.areaMatrix(organismo.r_explotacion)
        
        self.datos = None
    

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            pos = self.modelo.espacio.getFilaColumnaAreaMatrix(organismo.posicion,organismo.r_explotacion,organismo.MatrizArea.shape)
            #print(int(pos[0]))
            for p in pos:
                organismo.MatrizArea[p] +=1
    def finalizar(self, t, s):
        for organismo in self.modelo:
            [f,c] = np.shape(organismo.MatrizArea)
            valor=sum(sum(organismo.MatrizArea > 0))/(f*c)
            #print(self.datos)
            #print(s)
            if (self.datos is None):
                self.datos = np.array(valor)
            else:
                self.datos = np.hstack((self.datos,valor))


"""class CalcularVariarAreaConTiempo(VariacionParametroBloques):

    def __init__ (self):
        super().__init__("")
"""