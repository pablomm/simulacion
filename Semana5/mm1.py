
import numpy as np
import scipy as sc
import scipy.stats
import matplotlib.pyplot as plt

from modelo import MMc


if __name__ == '__main__':


    arrival_lambda = 1.
    server_lambda = 1.5
    closing_time = 1000

    m = MMc(arrival_lambda = arrival_lambda, server_lambda=server_lambda,
            closing_time=closing_time).simulate()

    """
    print(m.times) # Tiempos donde se guarda la cola y estado de servidores
    print("cola",m.lq_record) # Estado de la cola en el tiempo
    print(m.ls_record) # Arrays con estado de los servidores

    print("tiempos salida",m.departure_times )
    print("tiempos en el sistema",m.tiempo_sistema )


    """

"""
IDEAS
MM1 fijando un rate y haciendo medias y ver si siguen o no tcl
En funcion de lo ajustado que sea el rate



Graficas colas y tiempos de servicio con distintas rates

Grafica de correlacion con lo dicho en clase
Cosas del paper


"""

    plt.figure()
    d = np.diff(m.arrival_times)
    c = np.linspace(0, max(d),200)
    plt.hist(d, density=True)
    plt.plot(c, sc.stats.expon.pdf(c, scale=1./arrival_lambda))

    fig, ax = plt.subplots(2,1, sharex=True)

    ax[0].bar(m.departure_times, m.tiempo_sistema)
    ax[1].bar(m.times, m.lq_record)



    plt.show()
