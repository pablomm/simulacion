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

    def __init__(self,nservers,arrivalrate,serverrate,servtimemax):

        if(nservers != 1):
            if(nservers != len(serverrate)):
                raise Exception('ValueError nservers')
        # state variables:
        self.ls = np.zeros((1,nservers))[0]  # server state {1, 0} 
        self.lq = 0                          # Queue server length
        #: Cola de prioridad de Eventos
        self.eventList = []      

        # The below is for collection of accumulated waiting time statistics

        self.inQueue =  []           # Almacena tiempos de llegada clientes
        self.outQueue = []          # Almacena el tiempo en el sistema
        self.inServerQueue = []          #Almacena tiempo en cola
        self.salidas = []           #Almacena salidas
        self.tiempoEntreSalidas = [0]
        self.valoresCola = [0]
        self.ServersUnusedTime = [[0] for _ in range(nservers)]

        #: Number of servers
        self.nservers = nservers 
            
        #: Arrival rate (input to the cumulative exponential generator)
        self.arrivalrate = arrivalrate
            
        #: Service time (inputs to the exponential distribution generator)
        if nservers == 1:
            serverrate = [serverrate]
        self.serverrate   =    serverrate    # Mean service time ( 1 /serverrate )
        self.servtimemax  =  servtimemax  # extreme outliers may screw up the statistics...

        #: Time when each realization is closed (long enough so that equilibrium
        #: may be assumed to prevail during most of each realization)
        self.time = 0
        self.closingtime = 1e3 #* max(1.0/arrivalrate, 1.0/max(serverrate))

        self.statistics= {}
        self.dictEvents = {}
        self.maxCola=0
        self.tmaxCola = 0
        self.meanTime = 0
        #self.timeall        = nrealizations*closingtime



    def get_server(self,time):
        r = np.where(self.ls == 0);
        l = len(r[0]);
        if (l == 0):

            return -1;

        else:

            pos = rn.randint(0,l-1)
            self.ServersUnusedTime[pos][-1] = time - self.ServersUnusedTime[pos][-1]
            self.ls[r[0][pos]] = 1;

            return r[0][pos];
        return  -1;


    def add_event(self,e):

        hp.heappush(self.eventList, e)

    def simular(self):
        self.dictEvents.update({"Tiempo en cola medio": []} )
        self.dictEvents.update({"Serviores tiempo sin usar": []}) 
        e = ev.ArrivalEvent(self.time,self.arrivalrate,self)
        hp.heappush(self.eventList,e)
        e = ev.ServerEndEvent(self.closingtime)
        hp.heappush(self.eventList,e)
        while self.eventList:
            e = hp.heappop(self.eventList)       # extrae el evento de maxima prioridad  
            e()
        self.dictEvents.update({"Tiempo en cola medio": np.mean(self.inServerQueue)} )
        self.dictEvents.update({"Serviores tiempo sin usar": [np.mean(x) for x in self.ServersUnusedTime]}) 
        return

    def free_server(self,s,time):
        self.ServersUnusedTime[s].append(time)
        self.ls[s] = 0;

    def generate_server_time(self,index):
        return self.f_exponential(self.serverrate[index]);

    def generate_statistics(self):
        pass
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
    def collectStatistics(self, time, salida=0):
        if self.maxCola < self.lq:
            self.maxCola = self.lq
            self.tmaxCola = time
            tiempo = [0]
            if (len(self.outQueue)) != 0:
                tiempo = self.outQueue
            self.meanTime = np.mean(tiempo)
        estadisticos = [ self.lq, self.ls, self.inQueue, self.outQueue,
                      self.inServerQueue,  self.ServersUnusedTime,self.salidas,self.maxCola,self.tmaxCola,self.meanTime]

        self.statistics.update({time:estadisticos})
