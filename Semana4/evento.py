

import numpy as np


class Evento:

    def __init__(self, tipo, clocktime):
        """ Constructor
        Args:
            tipo ('str') Event type.
            clocktime (int): Event time.

        Returns: An event
        """

        self.__tipo = tipo
        self.__clocktime = clocktime

    @property
    def clock_time(self,v):
        return self.__clocktime

    @property
    def tipo(self):
        return self.__tipo

    def __str__(self):
        return (self.__tipo + " " + str(self.__clocktime))

    def __lt__(self, other):
        return self.__clocktime < other.__clocktime

    def __gt__(self, other):
        return self.__clocktime > other.__clocktime

    def __call__(self):
        raise NotImplementedError


class ServerEndEvent(Evento):

    def __init__(self, clocktime):
        super().__init__("Server End Event", clocktime)

    def __call__(self):
        return self.clock_time

class ArrivalEvent(Evento):

    def __init__(self, clocktime,rate, modelo):
        self.modelo = modelo
        self.rate = rate

        super().__init__("Arrival Event", clocktime)

    def _generate_time(self):
        r"""Distribucion te tiempos del evento de llegada"""

        return numpy.random.exponential(scale=self.rate)


    def __call__(self):
        r"""
        Procesado de un evento de llegada. Si hay servidores vacios usa uno de
        ellos, en otro caso se incluye en la cola.

        Encadena un evento de llegada.
        """
        # Caso elementos en cola
        if self.modelo.lq != 0:
            self.modelo.lq += 1
        else: # Caso elementos
            s = self.modelo.get_server() # Obtenemos servidor y lo ocupamos is libre

            if s == -1: # Caso todos los servidores ocupados
                self.modelo.lq += 1
            else: # Lo incluimos en el servidor libre
                s_time = self.modelo.generate_server_time(s)
                t = self.clock_time + s_time

                # Estaria vien meter esta comprobacion en add_event y ahorranosla aqui
                if t < self.modelo.closingtime:
                    e = DepartureEvent(t, modelo, s)
                    self.modelo.add_event(e)

        # Encadenamos un evento de llegada en tiempo T+S
        s = self._generate_time()
        t = self.clock_time + s
        # Estaria vien meter esta comprobacion en add_event y ahorranosla aqui
        if t < self.modelo.closingtime:
            e = ArrivalEvent(t, self.rate, self.modelo)
            self.modelo.add_event(e) # Anadimos el evento de llegada

        return self.clock_time


class DepartureEvent(Evento):

    def __init__(self, clocktime, modelo, server):

        self.modelo = modelo
        self.server = server

        super().__init__("Departure Event server "+ str(server), clocktime)

    def __call__(self):
        r"""Si no hay elementos en la cola libera el servidor correspondiente
        En otro caso decrementa el numero de elementos de la cola y genera otro
        evento de Departure.
        """

        if self.modelo.lq != 0:
            self.modelo.lq -= 1
            # Generar otro Departure para el elemento sacado de la cola
            s = self.modelo.generate_server_time(self.server)
            t = self.clock_time + s

            # Estaria vien meter esta comprobacion en add_event y ahorranosla aqui
            if t < self.modelo.closingtime:
                e = DepartureEvent(t + s, modelo, self.server)
                self.modelo.add_event(e)

        else:
            self.modelo.free_server(self.server) # Liberamos el servidor

        return self.clock_time
