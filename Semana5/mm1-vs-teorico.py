

""" Script para comparar medidas MM1 con las esperadas de forma teorica
"""


import numpy as np
import scipy as sc
import scipy.stats
import matplotlib.pyplot as plt

from modelo import MMc


# Parametros de la simulacion de un M/M/1
arrival_lambda = 2. # Parametro tiempos exponenciales llegada
closing_time = 1000 # Tiempo a simular cada MM1

factores_carga = [.5,.7,.8,.9] # Distintos rhos con los que compara el MM1
#factores_carga = [.5,.7,.8,.9,.999] # Distintos rhos con los que compara el MM1

# Rampa se subida
tiempo_estacionario = 250

numero_simulaciones = 25 # Numero de simulacions a realizar por factor de carga

anteriores = 3 # Numero de anteriores a tener en cuenta en ultimo grafico


def main():

    plt.style.use("seaborn")

    # Creamos un array con todos los plots que haremos para mas facilidad
    nplots = 9
    plots = [plt.subplots(len(factores_carga), 1, sharex=True)[1] for _ in range(nplots)]

    # Titulos
    plots[0][0].title.set_text("Tiempo total en el sistema")
    plots[1][0].title.set_text("Tiempo total en el sistema (conjunto)")
    plots[2][0].title.set_text("Tamaño medio de la cola")
    plots[3][0].title.set_text("Tamaño medio de la cola no vacia")
    plots[4][0].title.set_text("Tiempo de espera / tiempo")
    plots[5][0].title.set_text("Tamaño de la cola / tiempo")
    plots[6][0].title.set_text("Tamaño de la cola / Tiempo de espera")
    plots[7][0].title.set_text("Tiempo de espera / Tiempo de espera anterior")
    plots[8][0].title.set_text("Tiempo de espera / media tiempos {} anteriores".format(anteriores))

    d = 0

    for j, rho in enumerate(factores_carga):

        server_lambda = arrival_lambda / rho

        for p in plots:
            p[j].set_ylabel("rho={}".format(rho))


        tiempos = np.array([])
        colas = np.empty(numero_simulaciones)
        colas_no_vacias = np.empty(numero_simulaciones)

        for i in range(numero_simulaciones):

            print("Simulando MM1 {}: {:02d}/{}"
                  .format(rho, i+1,numero_simulaciones), end="\r")


            m = MMc(arrival_lambda=arrival_lambda, server_lambda=server_lambda,
                    closing_time=closing_time).simulate()

            # Solo consideramos los tiempos a partir de la rampa de subida
            t_salidas_index = [m.departure_times > tiempo_estacionario]
            t_salidas_estacionario = m.tiempo_sistema[t_salidas_index]
            t_estacionario_index = [m.times > tiempo_estacionario]
            t_estacionario = m.times[t_estacionario_index]

            cola = m.lq_record[t_estacionario_index]
            colas[i] = np.mean(cola)
            colas_no_vacias[i] = np.mean(cola[cola != 0])
            tiempos = np.hstack((tiempos, t_salidas_estacionario))

            # Plots
            plots[0][j].hist(t_salidas_estacionario, density=True, alpha=.4)
            d = max(d, np.max(t_salidas_estacionario))

            plots[4][j].plot(m.departure_times, m.tiempo_sistema)
            plots[5][j].plot(m.times,m.lq_record)


            indices = np.in1d(m.times, m.departure_times)
            plots[6][j].scatter(m.lq_record[indices], m.tiempo_sistema)

            plots[7][j].scatter(m.tiempo_sistema[:-1], m.tiempo_sistema[1:])


            suma = m.tiempo_sistema[anteriores:] / anteriores
            for i in range(1,anteriores):
                suma += m.tiempo_sistema[i:-(anteriores-i)] / anteriores

            plots[8][j].scatter(m.tiempo_sistema[:-anteriores],
                                m.tiempo_sistema[anteriores:])





        # Dibujamos exnencial mu - lambda
        x = np.linspace(0, d)
        y = sc.stats.expon.pdf(x, scale=1./(server_lambda - arrival_lambda))
        plots[0][j].plot(x, y, color="red", linestyle="dashed")

        plots[1][j].hist(tiempos, density=True)
        plots[1][j].plot(x, y, color="red", linestyle="dashed")

        plots[2][j].hist(colas)
        plots[2][j].axvline(x=rho/(1-rho), linewidth=2.5, linestyle="dashed", c="red")

        plots[3][j].hist(colas_no_vacias)
        plots[3][j].axvline(x=1./(1-rho), linewidth=2.5, linestyle="dashed", c="red")




    # Distribucion exponencial


    plt.show()

if __name__ == '__main__':
    main()
