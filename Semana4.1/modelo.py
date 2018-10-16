""" This example is a demo of the use of discrete event simulation

A M/M/1 queue is simulated, i.e.:
    - one server,
    - Poisson arrival (exponentially distributed interarrival times),
    - exponentially distributed service time,
    - FIFO queue organization.


import the modules:
    main :
    numpy : For generating the random events
    heapq : Gestiona las cola de priridad de los eventos

import the following classes:
    Evento : Define y gestiona el tipo de eventos

"""

import numpy as np
from collections import deque
import random as rn
import evento as ev
import heapq as hp

class Modelo:

    def __init__(self, nservers = 1, arrivalrate = 1,
                 serverrate = 1, closingtime = 1e3):

        if(nservers != len(serverrate)):
            raise ValueError('nservers')

        # state variables:
        self.ls = np.zeros(nservers)  # server state {1, 0}
        self.lq = 0   # Queue server length
        self.eventList = [] # Cola de prioridad de Eventos


        self.times = []
        
        # The below is for collection of accumulated waiting time statistics

        self.inQueue =  []          # Almacena tiempos de llegada clientes
        self.queueSize = []         # Almacena el tamano de la cola cuando llega el cliente
        
        self.queueTime = []         # Almacena el tiempo en cola de cada cliente
        self.outQueue = []          # Almacena el tiempo en el sistema
        
        #self.salidas = []           #Almacena salidas
        #self.tiempoEntreSalidas = [0]
        #self.valoresCola = [0]
        #self.ServersUnusedTime = [[0] for _ in range(nservers)]

        #: Number of servers
        self.nservers = nservers

        #: Arrival rate (input to the cumulative exponential generator)
        self.arrivalrate = arrivalrate

        #: Service time (inputs to the exponential distribution generator)
        self.serverrate   = serverrate    # Mean service time ( 1 /serverrate )

        #: Time when each realization is closed (long enough so that equilibrium
        #: may be assumed to prevail during most of each realization)
        self.time = 0
        self.closingtime = closingtime #* max(1.0/arrivalrate, 1.0/max(serverrate))


        self.statistics= {}
        #self.dictEvents = {}
        #self.maxCola=0
        #self.tmaxCola = 0
        #self.meanTime = 0


    def get_server(self,time):
        r = np.where(self.ls == 0);
        l = len(r[0]);
        if (l == 0):

            return -1;

        else:

            pos = rn.randint(0,l-1)
            #self.ServersUnusedTime[pos][-1] = time - self.ServersUnusedTime[pos][-1]
            self.ls[r[0][pos]] = 1;

            return r[0][pos];
        return  -1;


    def add_event(self,e):
        if e.clock_time < self.closingtime:
            hp.heappush(self.eventList, e)

    def simular(self):
        #self.dictEvents.update({"Tiempo en cola medio": []} )
        #self.dictEvents.update({"Serviores tiempo sin usar": []})
        
        e = ev.ArrivalEvent(self.time, self.arrivalrate, self)
        hp.heappush(self.eventList,e)
        
        e = ev.ServerEndEvent(self.closingtime)
        hp.heappush(self.eventList,e)

        while self.eventList:
            e = hp.heappop(self.eventList)       # extrae el evento de maxima prioridad
            ret = e()
            self.generate_statistics(t_actual = ret[0], t_llegada = ret[1])
        
        #if len(self.queueTime) > 0:
        #    self.dictEvents.update({"Tiempo en cola medio": np.mean(self.queueTime)} )
        #else:
        #    self.dictEvents.update({"Tiempo en cola medio": 0} )
        
        #self.dictEvents.update({"Serviores tiempo sin usar": [np.mean(x) for x in self.ServersUnusedTime]})
        return self

    def free_server(self,s,time):
        #self.ServersUnusedTime[s].append(time)
        self.ls[s] = 0;

    def generate_server_time(self,index):
        return self.f_exponential(self.serverrate[index]);

    def f_exponential (self,rate, n = None):
        """ Generate random exponential deviates

        Parameters:
            rate (int): Exponential rate
            n (int): number of observations

        Returns: List sample

        """
        exp = lambda u: -np.log(u) / rate
        u = np.random.uniform(0, 1, n)
        return exp(u)

    def add_arrival(self, time):
        self.inQueue.append(time)
    
    def get_arrival(self):
        return hp.heappop(self.inQueue) #TODO lo sacamos? Estaria bien dejarlos pa estadisticas
    
    def add_tamcola(self, tamcola):
        self.queueSize.append(tamcola)
    
    def generate_statistics(self, t_actual, t_llegada):
        self.outQueue.append(t_actual - t_llegada)
        #tamano cola, estado servidor ...
        
        return

    def collectStatistics(self, time):
        pass

