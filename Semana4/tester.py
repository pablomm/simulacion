import modelo as mod
import matplotlib.pyplot as plt
import numpy as np
posiciones = {"Cola": 0,"Servers":1,"Llegadas": 2, "TiempoSistema": 3,
                     "TiempoColas": 4, "TiempoServidoresSinUsar": 5,"salidas":6}

medias = [[],[],[],[],[]]

plt.figure(1)
reps = 50

def htmlcolor(r, g, b):
    def _chkarg(a):
        if isinstance(a, int): # clamp to range 0--255
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a*255))
        else:
            raise ValueError('Arguments must be integers or floats.')
        return a
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)
#Cada Fila es la cola iesima las diferentes lineas son variaciones de los parametros
colors = [htmlcolor(int(x[0]),int(x[1]),int(x[2])) for x in np.random.randint(0,255,(reps,3))]

for k in range(reps):
	times = None
	for i in range(5):
		plt.figure(1)
		j = i+1
		l1 = 0.3/(10*j)
		l2 = 0.2/j
		m = mod.Modelo(2,0.1+k/50,[l1,l2],5,times)
		m.simular()
		#print(m.dictEvents["Serviores tiempo sin usar"])
		medias[0].append(m.dictEvents["Tiempo en cola medio"])
		medias[1].append(m.dictEvents["Serviores tiempo sin usar"][0])
		medias[2].append(m.dictEvents["Serviores tiempo sin usar"][1])
		#Las keys del diccionario son los tiempos en los que se guardo el registro
		tiempos = list(m.statistics.keys())
		valores = list(m.statistics.values())
		valoresCola = [y[0] for y in valores]
		valoresServidores = [y[1] for y in valores]
		valoresMaxCola = [y[7] for y in valores]
		valoresTiempoSistemaMedio = [y[9] for y in valores]#miramos el tiempo medio para el valor maximo de la cola en cada tiempo 
		medias[3].append(np.mean(m.outQueue)) #Media de tiempo total en el sistema
		medias[4].append(np.mean(valoresMaxCola))#Media del tiempo total en la cola
		ax = plt.subplot(5,3,3*i+1)
		if i == 0:
			ax.set_title("tiempos vs valor cola")
		plt.plot(tiempos,valoresCola,label = "$Cola {i} repeticion {k}$".format(i=i,k=k),color = colors[k])
		ax = plt.subplot(5,3,3*i+2)
		if i == 0:
			ax.set_title("valor cola max vs valor medio tiempo en sistema")
		plt.plot(valoresMaxCola,valoresTiempoSistemaMedio,label = "$Cola {i} repeticion {k}$".format(i=i,k=k),color = colors[k])
		tiempoEntreSalidas = m.tiempoEntreSalidas
		ax = plt.subplot(5,3,3+3*i)
		if i == 0:
			ax.set_title("valor cola vs tiempo entre salidas")
		plt.scatter(m.valoresCola,tiempoEntreSalidas,label = "$Cola {i} repeticion {k}$".format(i=i,k=k),color = colors[k])
		times = m.salidas
		plt.figure(2)
		plt.subplot(1,5,i+1)
		plt.title("${l1},{l2}$".format(l1=l1,l2=l2))
		if(k <3 or reps-k < 3):
			plt.plot(tiempos,valoresCola,color = colors[k], label = "$experimento {k}$".format(k=k))
		else:
			plt.plot(tiempos,valoresCola,color = colors[k])
		plt.xlabel("Tiempo")
		plt.ylabel("n elementos en cola")
plt.legend(loc='best')
plt.show()
"""
fig, axs = plt.subplots(1, 2)
axs[0].hist(m.outQueue)
axs[1].hist(m.inQueue)
plt.show()
fig, axs = plt.subplots(1, 2)
axs[0].hist(m.ServersUnusedTime[0])
axs[1].hist(m.ServersUnusedTime[1])
plt.show()
"""
#print(medias)

#Como vemos ploteando los histogramas de estas muestras ninguno es minimamente simetrico, debido a que no son independientes el tcl no funciona
fig, axs = plt.subplots(2, 3)

ax = plt.subplot(2,3,1)
ax.set_title("Tiempo medio en cola")
plt.hist(medias[0])

ax = plt.subplot(2,3,2)
ax.set_title("Tiempo medio del servidor 1 sin usar")
plt.hist(medias[1])

ax = plt.subplot(2,3,3)
ax.set_title("Tiempo medio del servidor 2 sin usar")
plt.hist(medias[2])

ax = plt.subplot(2,3,4)
ax.set_title("Tiempo medio en el sistema")
plt.hist(medias[3])

ax = plt.subplot(2,3,5)
ax.set_title("Valor medio maximo de la cola")
plt.hist(medias[4])
plt.show()

#print(m.dictEvents)
