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
sys.path.append("../")

from simulador import ObjetivosUniformes, EspacioToroidalFinito, Modelo
from simulador import EstadisticaArea
from simulador import RandomWalkerVFija


# Configuracion del espacio
n = 100
n_objetivos = 100 # Numero de objetivos
size = (100.,100.) # Dimensiones del espacio
r = 3 # Radio de explotacion
std = 1. # Desviacion estandar del movimiento browniano
t = np.linspace(50,1000,n)# Tiempo a simular
inicial = (50,50) # Coordenadas iniciales (None para aleatorias)

# Configuracion Plot
plt.style.use("seaborn")

# Creamos el modelo, definiendo el espacio y los objetivos
espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_objetivos, espacio)
modelo = Modelo(espacio, objetivos)

# Creamos un random walker y lo añadimos al modelo
organismo = RandomWalkerVFija(r, std=std, posicion=inicial)
modelo.add_organismo(organismo)

# Especificamos que estadisticas queremos recolectar
modelo.add_estadistica(EstadisticaArea())
valores = np.zeros(n)
IC0 = np.zeros(n)
IC1 = np.zeros(n)
rep = np.zeros(n)
ICrep = np.zeros(n)
ICrep1 = np.zeros(n)
ratios = np.zeros(n)
for i,x in  enumerate(t):
  modelo.simular(x,100)
  for estadistica in modelo.estadisticas:
    rep[i] = np.mean(estadistica.areaRep)
    valores[i] = np.mean(estadistica.areaRecorrida) 
    IC0[i] = np.percentile(estadistica.areaRecorrida,5)
    IC1[i] = np.percentile(estadistica.areaRecorrida,95)
    ICrep[i] = np.percentile(estadistica.areaRep,5)
    ICrep1[i] = np.percentile(estadistica.areaRep,95) 
    ratios[i] = np.median(estadistica.ratioRepeticion)
    #estadistica.inicializar(0,20)
#Vamos a suavizar la curva restando las frecuencias no importantes
lowess = sm.nonparametric.lowess(valores, t, frac=0.1) 
"""
w = scipy.fftpack.rfft(valores)
f = scipy.fftpack.rfftfreq(n, t[1]-t[0])
spectrum = w**2
cutoff_idx = spectrum < (spectrum.max()/10)
w2 = w.copy()
w2[cutoff_idx] = 0
suavizada = scipy.fftpack.irfft(w2)
"""
plt.figure()
plt.plot(t,valores,label="media",color="k")
plt.plot(t,IC0,'-',label="0.05%",color="r")
plt.plot(t,IC1,'-',label="0.95%",color="r")
plt.plot(lowess[:,0],lowess[:,1],'-',color = 'c',label="Suavizada")
plt.legend(loc='best')
lowess = sm.nonparametric.lowess(rep, t, frac=0.1) 
plt.figure()
plt.plot(t,rep,label="media",color="k")
plt.plot(t,ICrep,label="0.05%",color="r")
plt.plot(t,ICrep1,label="0.95%",color="r")
plt.plot(lowess[:,0],lowess[:,1],'-',color = 'c',label="Suavizada")
plt.show()