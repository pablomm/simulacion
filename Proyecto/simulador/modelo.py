

import matplotlib.pyplot as plt

from queue import Queue

class Modelo:
    """Clase Modelo.
        Permite incluir en ella diferentes organismos y estadisticas y realizar
        la simulacion.
    """

    def __init__(self, espacio, objetivos):
        """Constructor de modelo.
            espacio: Espacio donde se realizara la simulacion
            objetivos: Objetivos de la simulacion
        """
        self.espacio = espacio
        self.objetivos = objetivos
        self.queue = Queue()
        self.estadisticas = []
        self.n_organismos = 0

    def add_organismo(self, organismo):
        """Incluir organismo al modelo  """
        organismo.add_modelo(self)
        self.queue.put(organismo)
        self.n_organismos += 1

    def add_estadistica(self, estadistica):
        """Incluye una estadistica en el modelo"""
        estadistica.add_modelo(self)
        self.estadisticas.append(estadistica)

    def _inicializar_estadisticas(self, closing_time, n_simulacion):
        """Inicializa las estadisticas antes de simular"""
        for estadistica in self.estadisticas:
            estadistica.inicializar(closing_time, n_simulacion)

    def _actualizar_estadisticas(self, t, n_simulacion):
        """Actualiza las estadisticas en cada paso de la simulacion"""
        for estadistica in self.estadisticas:
            estadistica.actualizar(t, n_simulacion)

    def _finalizar_estadisticas(self, end, n_simulacion):
        """Finaliza las estadisticas al cierre de la simulacion"""
        for estadistica in self.estadisticas:
            estadistica.finalizar(end, n_simulacion)

    def simular(self, closing_time=1e3, n_simulaciones=1, stop_empty=False,
                verbose=2):
        """Simula el modelo hasta alcanzar el tiempo closing_time.

            Args:
                closing_time: Tiempo Maximo a simular
                n_simulaciones: Veces a repetir la simulacion
                stop_empty: Detener la simulacion si no hay mas objetivos
                verbose: Imprimir tiempo

            Returns:
                Tiempo final de la simulacion
        """

        closing_time = int(closing_time)
        self.n_simulaciones = int(n_simulaciones)

        for estadistica in self.estadisticas:
            estadistica.inicializar_simulaciones(self.n_simulaciones)

        for s in range(n_simulaciones):

            if verbose > 0:
                print("Simulacion {}".format(s+1), end="\r")
            # Vaciamos organismos de simulaciones anteriores
            if s != 0:
                self.objetivos.inicializar()
                for organismo in self:
                    organismo.clear()

            self._inicializar_estadisticas(closing_time, s)

            for t in range(closing_time):

                if verbose > 1:
                    print("Simulacion {}: {}/{}".format(s+1, t+1,closing_time),
                          end="\r")

                self.objetivos.actualizar_objetivos()

                for organismo in self:
                    organismo.step()

                self._actualizar_estadisticas(t, s)

                # Parar si no quedan objetivos
                if stop_empty and self.objetivos.numero_objetivos == 0:
                    break

            self._finalizar_estadisticas(t, s)

        return t

    def plot(self, ax=None, **kwargs):
        """Plotea el espacio y los objetivos del modelo"""

        if ax is None:
            ax = plt.gca()

        self.espacio.plot(ax)
        self.objetivos.plot(ax, **kwargs)

        return ax

    def __iter__(self):
        """ Itera sobre los organismos"""

        for _ in range(self.n_organismos):
            organismo = self.queue.get()
            self.queue.put(organismo)
            yield organismo
