

import numpy as np
from collections import deque
import evento as ev
import heapq as hp


class MMc:

    def __init__(self, n_servers = 1, arrival_lambda = 1,
                 server_lambda = 1., closing_time = 1e3):

        # Numero de servidores
        self.n_servers = n_servers

        # Tasa de servicio
        if np.isscalar(server_lambda):
            self.server_rate = np.full(n_servers, (1.*n_servers)/server_lambda)
        elif len(server_lambda) != n_servers:
            raise ValueError("server_rate debe ser una lista de tam n_servers")
        else:
            self.server_rate = 1./np.array(server_lambda)

        # Tasa de llegadas
        self.arrival_rate = 1./arrival_lambda

        # Tiempo en el que acabar al simulacion
        self.closing_time = closing_time

        # Lista de estados de servidores
        self.ls = np.zeros(n_servers)
        # Clientes en al cola
        self.lq = 0
        # Lista con heap de eventos
        self.event_list = []

        # Cola interna para el seguimiento de los tiempo totales
        self.arrival_queue = deque()

        # Lista donde almacenar eventos
        self.times = []
        self.lq_record = []
        self.ls_record = []

        self.departure_times = []
        self.tiempo_sistema = []

        self.arrival_times = []



    def get_server(self,time):
        # Indices libres
        r = np.where(self.ls == 0)[0]
        if len(r) == 0:
            return -1

        else:
            pos = np.random.choice(r)
            self.ls[pos] = 1;

            return pos;



    def add_event(self,e):
        if e.clock_time <= self.closing_time:
            hp.heappush(self.event_list, e)

    def pop_event(self):
        return hp.heappop(self.event_list)

    @property
    def empty(self):
        return len(self.event_list) == 0

    def free_server(self,s):

        self.ls[s] = 0

    def generate_server_time(self,index):
        # Devuelve tiempo distribuido con la tasa del servidor index
        return np.random.exponential(self.server_rate[index]);


    def add_event_time(self, time):

        self.times.append(time)
        self.lq_record.append(self.lq)
        self.ls_record.append(np.array(self.ls))



    def add_arrival(self, time):
        self.add_event_time(time)

        self.arrival_times.append(time)

        # Incluimos tiempo para extraerlo en
        self.arrival_queue.appendleft(time)
        # Aqui irian todas las estadisticas a modificar con una llegada




    def add_departure(self, time, arrival_time):
        self.add_event_time(time)
        self.departure_times.append(time)
        self.tiempo_sistema.append(time - arrival_time)

    def end_simulation(self):
        self.times = np.array(self.times)
        self.lq_record = np.array(self.lq_record)
        self.ls_record = np.array(self.ls_record)
        self.departure_times = np.array(self.departure_times)
        self.arrival_times = np.array(self.arrival_times)
        self.tiempo_sistema = np.array(self.tiempo_sistema)

        # No necesario
        self.event_list = []

        # aqui iria las estadisticas al ejecutarse un arrival

    def get_arrival(self):
        # Devuelve el tiempo de llegada del primer elemento en la cola de espera
        return self.arrival_queue.pop()



    def simulate(self, InitialEvent=ev.ArrivalEvent, EndEvent=ev.ServerEndEvent):

        # Creamos el evento inicial en tiempo 0
        initial = InitialEvent(0, self.arrival_rate, self)
        self.add_event(initial)

        # Evento final
        final = EndEvent(self.closing_time, self)
        self.add_event(final)

        # Hasta quedarnos sin eventos
        while not self.empty:
            # Extraemos eventos y los ejecutamos
            e = self.pop_event()
            e()
            #print(e)


        return self
