import modelo as mod
import matplotlib.pyplot as plt
import numpy as np
posiciones = {"Cola": 0,"Servers":1,"Llegadas": 2, "TiempoSistema": 3,
                     "TiempoColas": 4, "TiempoServidoresSinUsar": 5,"salidas":6}

medias = [[],[],[],[],[]]
fig, axs = plt.subplots(5, 3)
for i in range(5):
	j = i+1
	m = mod.Modelo(2,0.1/j,[30*j,2*j],5)
	m.simular()
	#print(m.dictEvents["Serviores tiempo sin usar"])
	medias[0].append(m.dictEvents["Tiempo en cola medio"])
	medias[1].append(m.dictEvents["Serviores tiempo sin usar"][0])
	medias[2].append(m.dictEvents["Serviores tiempo sin usar"][1])
	tiempos = list(m.statistics.keys())
	valores = list(m.statistics.values())
	valoresCola = [y[0] for y in valores]
	valoresServidores = [y[1] for y in valores]
	valoresMaxCola = [y[7] for y in valores]
	valoresTiempoSistemaMedio = [y[9] for y in valores]
	medias[3].append(np.mean(m.outQueue))
	medias[4].append(np.mean(m.inServerQueue))
	ax = plt.subplot(5,3,3*i+1)
	ax.set_title("tiempos vs valor cola")
	plt.plot(tiempos,valoresCola)
	ax = plt.subplot(5,3,3*i+2)
	ax.set_title("valor cola max vs valor medio tiempo en sistema")
	plt.plot(valoresMaxCola,valoresTiempoSistemaMedio)
	tiempoEntreSalidas = m.tiempoEntreSalidas
	ax = plt.subplot(5,3,3+3*i)
	ax.set_title("valor cola vs tiempo entre salidas")
	plt.plot(m.valoresCola,tiempoEntreSalidas,'o')
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
fig, axs = plt.subplots(1, 3)

axs[0].hist(medias[0])
axs[1].hist(medias[1])
axs[2].hist(medias[2])
plt.show()

#print(m.dictEvents)
