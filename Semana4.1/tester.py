

import matplotlib.pyplot as plt
import numpy as np

import modelo as mod


posiciones = {"Cola": 0,"Servers":1,"Llegadas": 2, "TiempoSistema": 3,
                     "TiempoColas": 4, "TiempoServidoresSinUsar": 5,"salidas":6}

medias = [[],[],[],[],[]]

n_simulaciones = 5
numero_servidores = 1
arrival_rate = .1
server_rates = [.8]
serv_time_max = 5

plt.figure(1)

#Cada Fila es la cola iesima las diferentes lineas son variaciones de los parametros
colors = ['red', 'black', 'blue', 'brown', 'green']

for k in range(5):
	times = None
	for i in range(n_simulaciones):
		plt.figure(1)

		j = i+1
		l1 = 0.3/(10*j)
		l2 = 0.2/j

		m = mod.Modelo(numero_servidores,arrival_rate, server_rates,
                 serv_time_max, times)

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
		plt.plot(tiempos,valoresCola,color = colors[k], label = "$experimento {k}$".format(k=k))
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
