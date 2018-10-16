

import matplotlib.pyplot as plt
import numpy as np

from modelo import Modelo


n_simulaciones = 1
numero_servidores = 1
arrival_rate = .1
server_rates = .8
serv_time_max = 5


mod = Modelo(numero_servidores,arrival_rate, server_rates, serv_time_max, None )


mod.simular()

print(mod.statistics[999.8608045038472])
print("njnjn")
