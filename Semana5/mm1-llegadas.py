

""" Script simple para validar que los datos de llegada
    se generan y recogen correctamente en el caso mas sencillo
"""


import numpy as np
import scipy as sc
import scipy.stats
import matplotlib.pyplot as plt

from modelo import MMc


# Parametros de la simulacion de un M/M/1
arrival_lambda = 2. # Parametro tiempos exponenciales llegada
server_lambda = 1.5 # Parametro tiempos exponenciales servidor
closing_time = 100 # Tiempo a simular cada MM1


# Llegadas esperadas por simulacion
expected = closing_time * 1./arrival_lambda

numero_simulaciones = 250


def main():

    plt.style.use("seaborn")

    plt.title("Tiempos entre llegadas $\sim exp(\lambda={:1.2f})$".format(arrival_lambda))

    medias = np.empty(numero_simulaciones)
    tiempos = np.array([])


    for i in range(numero_simulaciones):
        print("Simulando MM1: {}/{}".format(i+1,numero_simulaciones),end="\r")
        m = MMc(arrival_lambda=arrival_lambda, server_lambda=server_lambda,
                closing_time=closing_time).simulate()

        times = np.diff(m.arrival_times)
        tiempos = np.hstack((tiempos, times))
        medias[i] = np.mean(times)
        maximo = np.max(times)
        plt.hist(times, density=True, alpha=.4)

    # Distribucion exponencial
    x = np.linspace(0, maximo, 100)
    y = sc.stats.expon.pdf(x, scale=1./arrival_lambda)
    plt.plot(x, y, color="red", linestyle="dashed")

    plt.figure()
    plt.title("Tiempos entre llegadas")
    plt.hist(tiempos, bins=15, density=True)
    plt.plot(x, y, color="red", linestyle="dashed")


    plt.figure()
    mean = np.mean(medias)
    d = np.max(np.abs(medias - mean))

    plt.title("Media de llegadas $(\mu={:1.2f},\sigma={:1.2f})$"
              .format(mean, np.std(medias)))

    plt.xlim((mean-d, mean + d))
    plt.hist(medias, density=True)

    # Dibujamos normal segun el TCL
    x = np.linspace(mean-d, mean+d, 100)
    mu = 1./arrival_lambda
    sigma = 1./(arrival_lambda**2*np.sqrt(expected)) # sqrt(n)*lambda

    plt.plot(x,sc.stats.norm.pdf(x,loc=mu, scale=sigma), color="maroon",
             linestyle="dashed")

    plt.show()

if __name__ == '__main__':
    main()
