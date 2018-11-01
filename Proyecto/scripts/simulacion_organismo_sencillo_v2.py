

import sys
sys.path.append("../")


import matplotlib.pyplot as plt


from objetivos import ObjetivosUniformes
from espacio import EspacioToroidalFinito
from modelo import Modelo
from organismo import OrganismoSencilloV2


# Configuracion del espacio
n_puntos = 100
size = (100.,100.)
r = 3 # Radio de explotacion
t = 500

# Configuracion Plot
plt.style.use("seaborn")


espacio = EspacioToroidalFinito(*size)
objetivos = ObjetivosUniformes(n_puntos, espacio)
modelo = Modelo(espacio, objetivos)

organismo = OrganismoSencilloV2(r)
modelo.add_organismo(organismo)


modelo.simular(t)


organismo.plot_area_explotada()
modelo.plot()
organismo.plot_trayectoria()
organismo.plot_explotados()

plt.show()
