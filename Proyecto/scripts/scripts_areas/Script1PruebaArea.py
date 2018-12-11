"""Script para probar area recorrida como medida"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
import statsmodels.api as sm

# Nos movemos al fichero del script para evitar problemas
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea
from simulador import LevyFlightActivo


# Configuracion del espacio
n = 100
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
t = np.linspace(500,10000,n)# Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = LevyFlightActivo(1,3)
modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
#Variables para las areas totales
area = np.zeros(n)
IC0 = np.zeros(n)
IC1 = np.zeros(n)
#Variables para las areas repetidas
repetida = np.zeros(n)
ICrep = np.zeros(n)
ICrep1 = np.zeros(n)

#Variables para el ratio de comidos y area.
comida = np.zeros(n)
ICcomida = np.zeros(n)
ICcomida1 = np.zeros(n)
for i,x in  enumerate(t):
  
    modelo.simular(x,100)

    # Porque no hacer estadistica para intervalos de confianza
    repetida[i] = np.mean(organismo.areaRep)
    area[i] = np.mean(organismo.areaRecorrida)
    comida[i] = np.mean(organismo.ratioExplotadosArea)


    IC0[i] = np.percentile(organismo.areaRecorrida,5)
    IC1[i] = np.percentile(organismo.areaRecorrida,95)

    ICrep[i] = np.percentile(organismo.areaRep,5)
    ICrep1[i] = np.percentile(organismo.areaRep,95)

    

    ICcomida[i] = np.percentile(organismo.ratioExplotadosArea,5)
    ICcomida[i] = np.percentile(organismo.ratioExplotadosArea,95)


    #estadistica.inicializar(0,20)
#Vamos a suavizar la curva restando las frecuencias no importantes
lowess = sm.nonparametric.lowess(area, t, frac=0.1)

plt.figure()
plt.plot(t,area,label="media",color="k")
plt.plot(t,IC0,'-',label="0.05%",color="r")
plt.plot(t,IC1,'-',label="0.95%",color="r")
plt.plot(lowess[:,0],lowess[:,1],'-',color = 'c',label="Suavizada")
plt.legend(loc='best')
plt.title('Area')
lowess = sm.nonparametric.lowess(repetida, t, frac=0.1)

plt.figure()
plt.plot(t,repetida,label="media",color="k")
plt.plot(t,ICrep,label="0.05%",color="r")
plt.plot(t,ICrep1,label="0.95%",color="r")
plt.plot(lowess[:,0],lowess[:,1],'-',color = 'c',label="Suavizada")
plt.title('repetida')

lowess = sm.nonparametric.lowess(comida, t, frac=0.1)
plt.figure()
plt.plot(t,comida,label="media",color="k")
plt.plot(t,ICcomida,label="0.05%",color="r")
plt.plot(t,ICcomida1,label="0.95%",color="r")
plt.plot(lowess[:,0],lowess[:,1],'-',color = 'c',label="Suavizada")
plt.title('Ratio de objetivos encontrados')
plt.show()

## Guardar todo en el mismo vector ???
DAT = np.stack((t,area,IC0,IC1,repetida,ICrep,ICrep1,comida,ICcomida,ICcomida1))
np.savetxt('./datos/areas',DAT,delimiter="\t")
