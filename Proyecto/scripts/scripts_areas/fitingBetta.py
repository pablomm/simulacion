import scipy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

data_levy = np.loadtxt('areasLevy',delimiter=",")
data_rw = np.loadtxt('areasRW',delimiter=",")
area_levy = data_levy[:,0]
area_rw = data_rw[:,0]

x = np.linspace(0,1,500)
#Ploteamos la informacion para el area levy
plt.figure(1)
plt.hist(area_levy,bins="auto")

plt.title("Area recorrida por un levy para encontrar un objetivo")
plt.savefig("areaL.jpg")
#Ploteamos la informacion para el area del rw
plt.figure(2)

plt.hist(area_rw,bins="auto")

plt.title("Area recorrida por un RW para encontrar un objetivo")
plt.savefig("areaRW.jpg")
#Ploteamos las cdf del rw frente levy
plt.figure(3)
hist, bin_edges = np.histogram(area_levy,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist),'r', label="Levy")

hist, bin_edges = np.histogram(area_rw,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist),'b', label="RW")
plt.legend(loc='best')

plt.title("CDF del area recorrida de  Levy vs RW")
plt.savefig("CDFarea.jpg")
#boxplots para levy vs rw
plt.figure(4)

boxplot_area = [area_levy,area_rw]
plt.boxplot(boxplot_area)
plt.title("Area recorrida por un levy vs un RW")
plt.savefig("boxplotArea.jpg")

area_levy_rep = data_levy[:,1]
area_rw_rep = data_rw[:,1]

#Ploteamos la informacion para el area levy
plt.figure(5)
plt.hist(area_levy_rep,bins="auto")
plt.title("Area repetida por un levy para encontrar un objetivo")
plt.savefig("areaLrep.jpg")
#Ploteamos la informacion para el area del rw
plt.figure(6)

plt.hist(area_rw_rep,bins="auto")


plt.title("Area repetida por un RW para encontrar un objetivo")
plt.savefig("areaRWrep.jpg")

#Ploteamos las cdf del rw frente levy
plt.figure(7)
hist, bin_edges = np.histogram(area_levy_rep,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist), 'r', label="Levy")

hist, bin_edges = np.histogram(area_rw_rep,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist),'b', label="RW")

plt.legend(loc='best')
plt.title("CDF del area repetida de  Levy vs RW")

plt.savefig("CDFareaRep.jpg")

plt.figure(8)

boxplot_area_rep = [area_levy_rep,area_rw_rep]
plt.boxplot(boxplot_area_rep)
plt.title("Area repetida por un levy vs un RW")

plt.savefig("boxplotRep.jpg")
#Tiempos
tiempo_levy = data_levy[:,2]
tiempo_rw = data_rw[:,2]
def exponenial_func(x, a, b, c):
    return a*np.exp(-b*x)+c

minimo = np.min(tiempo_levy)
maximo = np.max(tiempo_levy)
#x = np.linspace(minimo,maximo,1000) 
#popt, pcov = curve_fit(exponenial_func, , hist, p0=(1, 1e-6, 1))

plt.figure(9)


plt.hist(tiempo_levy,bins="auto")
#plt.plot(x,exponenial_func(x, *popt))

plt.title("Tiempo por un levy para encontrar un objetivo")

plt.savefig("tiempoL.jpg")

plt.figure(10)
plt.hist(tiempo_rw,bins="auto")
#plt.plot(x,exponenial_func(x, *popt))

plt.title("Tiempo por un RW para encontrar un objetivo")

plt.savefig("tiempoRW.jpg")

plt.figure(11)

hist, bin_edges = np.histogram(tiempo_levy,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist), 'r', label="Levy")

hist, bin_edges = np.histogram(tiempo_rw,bins="auto")
hist = np.hstack((0,hist))
plt.plot(bin_edges,np.cumsum(hist),'b', label="RW")

plt.legend(loc='best')
plt.title("CDF del tiempo de Levy vs RW")

plt.savefig("CDFtiempo.jpg")

plt.figure(12)

boxplot_rw = [tiempo_levy,tiempo_rw]
plt.boxplot(boxplot_rw)
plt.title("Tiempo para encontrar un objetivo de un levy vs un RW")

plt.savefig("boxplotTiempo.jpg")
plt.show()