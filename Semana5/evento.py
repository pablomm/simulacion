

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
        self.created = clocktime

    @property
    def clock_time(self):
        return self.__clocktime

    @property
    def tipo(self):
        return self.__tipo

    def __str__(self):
        return (self.__tipo + " " + str(self.__clocktime) + "("+str(self.created)+")")

    def __lt__(self, other):
        return self.__clocktime < other.__clocktime

    def __gt__(self, other):
        return self.__clocktime > other.__clocktime

    def __call__(self):
        raise NotImplemented


class ServerEndEvent(Evento):

    def __init__(self, clocktime, modelo):
        super().__init__("Server End Event", clocktime)
        self.created = 0
        self.modelo = modelo

    def __call__(self):

        self.modelo.end_simulation()

        return self.clock_time


class ArrivalEvent(Evento):

    def __init__(self, clocktime,rate, modelo):
        self.modelo = modelo
        self.rate = rate

        super().__init__("Arrival Event", clocktime)

    def _generate_time(self):
        r"""Distribucion te tiempos del evento de llegada"""

        return np.random.exponential(scale=self.rate)


    def __call__(self):
        r"""
        Procesado de un evento de llegada. Si hay servidores vacios usa uno de
        ellos, en otro caso se incluye en la cola.

        Encadena un evento de llegada.
        """

        if self.modelo.lq != 0: # Caso elementos en cola
            self.modelo.lq += 1
        else:
            # Obtenemos servidor y lo ocupamos si esta libre
            s = self.modelo.get_server(self.clock_time)

            if s == -1: # Caso todos los servidores ocupados
                self.modelo.lq += 1 # Lo incluimos en la cola

            else: # Lo incluimos en el servidor libre
                s_time = self.modelo.generate_server_time(s)
                t = self.clock_time + s_time
                e = DepartureEvent(t, self.modelo, s)
                self.modelo.add_event(e)

        # Encadenamos un evento de llegada en tiempo T+S
        s = self._generate_time()
        t = self.clock_time + s
        e = ArrivalEvent(t, self.rate, self.modelo)
        self.modelo.add_event(e) # Anadimos el evento de llegada

        #Añadimos el tiempo de este evento en la lista de llegadas:
        self.modelo.add_arrival(self.clock_time)


        return self.clock_time

class DepartureEvent(Evento):

    def __init__(self, clocktime, modelo, server):

        self.modelo = modelo
        self.server = server


        super().__init__("Departure Event server:"+ str(server), clocktime)
        self.created = -1

    def __call__(self):
        r"""Si no hay elementos en la cola libera el servidor correspondiente
        En otro caso decrementa el numero de elementos de la cola y genera otro
        evento de Departure.
        """
        #Sacamos el ultimo tiempo en la cola
        self.created = self.modelo.get_arrival()

        if self.modelo.lq != 0:

            self.modelo.lq -= 1

            # Generar otro Departure para el elemento sacado de la cola
            s = self.modelo.generate_server_time(self.server)
            t = self.clock_time + s
            e = DepartureEvent(t , self.modelo, self.server)
            self.modelo.add_event(e)

        else:
             # Liberamos el servidor que estabamos ocupando
            self.modelo.free_server(self.server)

        self.modelo.add_departure(self.clock_time, self.created)

        return self.clock_time
