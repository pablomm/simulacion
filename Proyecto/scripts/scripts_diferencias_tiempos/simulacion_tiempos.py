

import os
import sys
import matplotlib.pyplot as plt
import numpy as np


# Configuracion Plot
plt.style.use("seaborn")



# Añadimos al path la raiz para poder importar la libreria local
script_path = os.path.dirname(os.path.abspath( __file__ ))
os.chdir(script_path)
sys.path.append("../../")

from simulador import Trayectoria, DiferenciasTiempos, Modelo, Explotados


def simular_tiempos(organismo, espacio, objetivos, n_objetivos, filename):
    ### Plotea grafica con condiciones iniciales #################################

    n_simulaciones = 100
    t = 500

    plt.figure()
    plt.title("{}, {} objetivos {}, t={}".format(type(organismo).__name__, n_objetivos,
                                                 type(objetivos).__name__, t))


    modelo = Modelo(espacio, objetivos)

    modelo.add_organismo(organismo)
    modelo.add_estadistica(Trayectoria())
    modelo.add_estadistica(Explotados())
    # Organismo en su posicion inicial
    organismo.plot()

    modelo.simular(t) # Realiza una simulacion para plotar la trayectoria
    modelo.plot()
    organismo.plot()
    organismo.plot_trayectoria()
    organismo.plot_explotados()

    plt.savefig("./graficas/ejemplo_{}_{}.png".format(filename,t))

    ##############################################################################

    ###### Simulacion diferencias de tiempos
    modelo = Modelo(espacio, objetivos)

    modelo.add_organismo(organismo)

    # Especificamos que estadisticas queremos recolectar
    estadistica = DiferenciasTiempos()
    modelo.add_estadistica(estadistica)


    modelo.simular(t, n_simulaciones=n_simulaciones, stop_empty=True, verbose=1)

    # Histograma de los resultados
    plt.figure()
    plt.title("Diferencias de tiempos en encontrar objetivos")
    plt.xlabel("Tiempo")
    plt.hist(estadistica.diferencias_tiempos, density=True)

    plt.savefig("./graficas/{}_{}.png".format(filename,t))

    print("Media", np.mean(estadistica.diferencias_tiempos))
    print("SD", np.std(estadistica.diferencias_tiempos))


    np.savetxt("./datos/{}_{}.csv".format(filename,t), estadistica.diferencias_tiempos)

    plt.show()
