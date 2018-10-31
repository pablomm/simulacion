

""" Script para comparar medidas MM1 con las esperadas de forma teorica
"""


import numpy as np
import scipy as sc
import scipy.stats
import matplotlib.pyplot as plt

# Libreria en github
from fda.grid import FDataGrid
import fda.kernel_smoothers
import fda
from modelo import MMc


# Parametros de la simulacion de un M/M/c

c = 1
arrival_lambda = 1. # Parametro tiempos exponenciales llegada
closing_time = 4000 # Tiempo a simular cada MM1

factores_carga = [.5,.7,.8,.9] # Distintos rhos con los que compara el MM1


# Rampa se subida
tiempo_estacionario = 250

numero_simulaciones = 25 # Numero de simulacions a realizar por factor de carga

sample_points = np.linspace(10, closing_time - 10, closing_time -20)

H = fda.kernel_smoothers.knn(sample_points)


def main():

    plt.style.use("seaborn")

    # Creamos un array con todos los plots que haremos para mas facilidad
    nplots = 4
    plots = [plt.subplots(len(factores_carga), 1, sharex=True, sharey=True)[1] for _ in range(nplots)]

    # Titulos
    plots[0][0].title.set_text("Tiempo de espera / tiempo")




    for j, rho in enumerate(factores_carga):

        simulaciones = []

        server_lambda = arrival_lambda / rho

        for p in plots:
            p[j].set_ylabel("rho={}".format(rho))


        tiempos = np.array([])
        colas = np.empty(numero_simulaciones)
        colas_no_vacias = np.empty(numero_simulaciones)

        for i in range(numero_simulaciones):

            print("Simulando MM1 {}: {:02d}/{}"
                  .format(rho, i+1,numero_simulaciones), end="\r")


            m = MMc(c, arrival_lambda=arrival_lambda, server_lambda=server_lambda,
                    closing_time=closing_time).simulate()

            # Guardamos las simulaciones
            fd = FDataGrid([m.tiempo_sistema], m.departure_times)
            simulaciones.append(fd(sample_points))



        tiempos = np.empty((numero_simulaciones, closing_time - 20))

        for i in range(numero_simulaciones):
            tiempos[i] = simulaciones[i]



        fdgrid = FDataGrid(tiempos, sample_points, dataset_label=None)
        fdgrid_s = FDataGrid((H @ tiempos.T).T, sample_points, dataset_label=None)
        fdgrid.plot(ax=plots[0][j])


        sd = fda.sqrt(fdgrid.var())
        fd = fdgrid.mean()
        (fd + sd).plot(ax=plots[1][j], c='red', linestyle="dashed")
        (fd - sd).plot(ax=plots[1][j], c='red', linestyle="dashed")
        fd.plot(ax=plots[1][j])

        fdgrid_s.plot(ax=plots[2][j])
        sd = fda.sqrt(fdgrid_s.var())
        fd = fdgrid_s.mean()
        (fd + sd).plot(ax=plots[3][j], c='red', linestyle="dashed")
        (fd - sd).plot(ax=plots[3][j], c='red', linestyle="dashed")
        fd.plot(ax=plots[3][j])




    plt.show()

if __name__ == '__main__':
    main()
