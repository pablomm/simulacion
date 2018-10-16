

import matplotlib.pyplot as plt
import numpy as np

from modelo import Modelo


n_simulaciones = 1
numero_servidores = 1
arrival_rate = .1
server_rates = [.8]
closingtime = 10


mod = Modelo(numero_servidores,arrival_rate, server_rates, closingtime )

mod.simular()

#print(mod.statistics)
