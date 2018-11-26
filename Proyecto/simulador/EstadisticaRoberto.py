from .estadistica import Estadistica,Trayectoria,add_metodo
import numpy as np
from .plots import *
class EstadisticaArea(Estadistica):
    def __init__(self):
        super().__init__()
        self.areaRecorrida = None #TODO hacerlo para cada organismo??? Nuestro proyecto es solo para un organismo es indiferente
        self.areaRep = None #TODO hacerlo para cada organismo??? 
        self.ratioRepeticion = None
        self.ratioExplotadosArea = None
        self.explotados = None

    def inicializar_simulaciones(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.MatrizArea = self.modelo.espacio.areaMatrix(organismo.r_explotacion)
            add_metodo(organismo,plot_mapa_calor)
        
        
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
            ratio = area*1./np.sum(organismo.MatrizArea)
            comidosVSArea = organismo.n_explotados*1./area
            if self.ratioRepeticion is None:
                self.ratioRepeticion = np.array(ratio)
            else:
                self.ratioRepeticion = np.hstack((self.ratioRepeticion,ratio))

            if self.ratioExplotadosArea is None:
                self.ratioExplotadosArea = np.array(comidosVSArea)
            else:
                self.ratioExplotadosArea = np.hstack((self.ratioExplotadosArea,comidosVSArea)) 

            if (self.areaRecorrida is None):
                self.areaRecorrida = np.array(area)
            else:
                self.areaRecorrida = np.hstack((self.areaRecorrida,area))

            if (self.areaRep is None):
                self.areaRep = np.array(rep)
            else:
                self.areaRep = np.hstack((self.areaRep,rep))
            if (self.explotados is None):
                self.explotados = np.array(organismo.n_explotados)
            else:
                self.explotados = np.hstack((self.explotados,organismo.n_explotados))
class EstadisticaAreaVariosOrganismos(Estadistica):
    def __init__(self):
        super().__init__()

    def inicializar_simulaciones(self, closing_time, n_simulacion):
        for organismo in self.modelo:
            organismo.MatrizArea = self.modelo.espacio.areaMatrix(organismo.r_explotacion)
            add_metodo(organismo,plot_mapa_calor)
            organismo.areaRecorrida = None #TODO hacerlo para cada organismo??? Nuestro proyecto es solo para un organismo es indiferente
            organismo.areaRep = None #TODO hacerlo para cada organismo??? 
            organismo.ratioRepeticion = None
            organismo.ratioExplotadosArea = None
        self.areaRecorrida = None #TODO hacerlo para cada organismo??? Nuestro proyecto es solo para un organismo es indiferente
        self.areaRep = None #TODO hacerlo para cada organismo??? 
        self.ratioRepeticion = None
        self.ratioExplotadosArea = None

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
            ratio = area*1./np.sum(organismo.MatrizArea)
            comidosVSArea = organismo.n_explotados*1./area
            if organismo.ratioRepeticion is None:
                organismo.ratioRepeticion = np.array(ratio)
            else:
                organismo.ratioRepeticion = np.hstack((organismo.ratioRepeticion,ratio))

            if organismo.ratioExplotadosArea is None:
                organismo.ratioExplotadosArea = np.array(comidosVSArea)
            else:
                organismo.ratioExplotadosArea = np.hstack((organismo.ratioExplotadosArea,comidosVSArea)) 

            if (organismo.areaRecorrida is None):
                organismo.areaRecorrida = np.array(area)
            else:
                organismo.areaRecorrida = np.hstack((organismo.areaRecorrida,area))
                
            if (organismo.areaRep is None):
                organismo.areaRep = np.array(rep)
            else:
                organismo.areaRep = np.hstack((organismo.areaRep,rep))


    
