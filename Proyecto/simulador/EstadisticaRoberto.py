from .estadistica import Estadistica,Trayectoria,add_metodo
import numpy as np
from .plots import *
class EstadisticaArea(Estadistica):
    def __init__(self):
        super().__init__()

    def inicializar_simulaciones(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.MatrizArea = self.modelo.espacio.areaMatrix(organismo.r_explotacion)
            add_metodo(organismo,plot_mapa_calor)
        
        self.areaRecorrida = None #TODO hacerlo para cada organismo??? Nuestro proyecto es solo para un organismo es indiferente
        self.areaRep = None #TODO hacerlo para cada organismo??? 

    def actualizar(self, t, n_simulacion):

        for organismo in self.modelo:
            pos = self.modelo.espacio.getFilaColumnaAreaMatrix(organismo.posicion,organismo.r_explotacion,organismo.MatrizArea.shape)
            #print(int(pos[0]))
            for p in pos:
                organismo.MatrizArea[p] +=1

    def finalizar(self, t, s):
        for organismo in self.modelo:
            [f,c] = np.shape(organismo.MatrizArea)
            area= np.sum(organismo.MatrizArea > 0)/(f*c)
            rep = np.sum(organismo.MatrizArea > 1)/(f*c)
            if self.ratioRepeticion is None:
                self.ratioRepeticion = np.array(np.sum(organismo.MatrizArea !=0)/np.sum(organismo.MatrizArea))
            if (self.areaRecorrida is None):
                self.areaRecorrida = np.array(area)
            else:
                self.areaRecorrida = np.hstack((self.areaRecorrida,area))
            if (self.areaRep is None):
                self.areaRep = np.array(rep)
            else:
                self.areaRep = np.hstack((self.areaRep,rep))
            




"""class CalcularVariarAreaConTiempo(VariacionParametroBloques):

    def __init__ (self):
        super().__init__("")
"""
