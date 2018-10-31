import numpy as np
import abc
import matplotlib.pyplot as plt
import math

class Espacio:

  __metaclass__ = abc.ABCMeta

  def __init__(self,x,y,name):
    self.__x = x
    self.__y = y
    self.__tipo = name
    
  @property
  def ejex(self):
    return self.__x
  
  @property
  def ejey(self):
    return self.__y
  @property
  def size(self):
    return [(self.__x[1] - self.__x[0]), (self.__y[1] - self.__y[0])]

  def __str__(self):
    return(self.__tipo + "\n" + np.zeros((*self.size)))

  @abc.abstractmethod
  def coordenadas(self,iniciales,finales):
    pass
  @abc.abstractmethod
  def objetivos_a_la_vista(self,posicion,Lojetivos,radio):
    pass
  @abc.abstractmethod
  def estabilizar_en_rango(self,objetivo,rango, posiciones):
    pass
  @abc.abstractmethod    
  def calcular_angulo_mov(self,inicial,final):
    pass

class EspacioToroidalFinito(Espacio):
  def __init__(self,x,y):
    super().__init__(x,y,"Espacio toroidal finito")
  
  def coordenadas(self,iniciales,finales):
    [X,Y] = self.size
    return [estabilizar_en_rango(finales[0],X,self.ejex),
            estabilizar_en_rango(finales[1],Y,self.ejey)]

  def objetivos_a_la_vista(self,posicion,Lojetivos,radio):
    vista = []
    for i in [-1,0,1]:
      for j in [-1,0,1]:
        vista.extend([(posicion[0]-(objetivo[0] + i*(self.ejex[1] - self.ejex[0])))** 2 + (posicion[1] -(objetivo[1] + j*(self.ejey[1] - self.ejey[0])))**2 < radio 
                  for objetivo in Lobjetivos.objetivos])
    return vista

  def estabilizar_en_rango(self,objetivo,rango, posiciones):
    res = objetivo
    if objetivo < posiciones[0]:
      res = posiciones[1] - abs(objetivo)%rango
    elif objetivo > posiciones[1]:
      res = posiciones[0] + abs(objetivo)%rango
    return res

  def calcular_angulo_mov(self,inicial,final):
    y = final[1]-inicial[1]
    x = final[0]-inicial[0]
    return angle = math.atan2(y, x) * (180.0 / math.pi)