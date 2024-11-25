"""
DES	

For this assignment we’ll be using the following notation:
λ – the arrival rate into the system as a whole.
µ – the capacity of each of n equal servers.
ρ represents the system load. In a single server system, it will be: ρ=λ/µ
In a multi-server system (one queue with n equal servers, each with capacity µ), it will be
ρ=λ/(nµ).
"""

import itertools
import random
import simpy
import numpy as np

SIM_TIME = 20
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()

class System:
    # setup system
    def __init__(self, env, nr_servers):
        self.env = env
        self.server = simpy.Resource(env, nr_servers)

    # serving of client
    def serv(self, servicetime):
        yield self.env.timeout(servicetime)

def client(env, system, servicetime, id):
    global AVG_WAITING_TIME
    # tells enviroment new customer arrives
    time_entering_system = env.now
    print(f'a client {id} arrives the system at {time_entering_system:.2f}.')
    with system.server.request() as request:
        yield request
        
        time_being_serviced = env.now
        print(f'a client {id} is being serviced at {time_being_serviced:.2f}.')
        AVG_WAITING_TIME += time_being_serviced - time_entering_system
        yield env.process(system.serv(servicetime))
        print(f'a client {id} stopped being serviced at {env.now:.2f}.')

def setup(env, nr_servers, arrival_rate, rho):
    global CLIENT_COUNT
    # arrival rate = lambda
    capacity = arrival_rate / (rho * nr_servers)
    system = System(env, nr_servers)
    
    while True:
        servicetime = np.random.exponential(1 / capacity)
        yield  env.timeout(np.random.exponential(1 / arrival_rate))
        env.process(client(env, system, servicetime, next(CLIENT_COUNT)))


random.seed(145)
env = simpy.Environment()

nr_servers = 1
env.process(setup(env, nr_servers=1, arrival_rate=1, rho=0.95))
env.run(until=SIM_TIME)
AVG_WAITING_TIME /= next(CLIENT_COUNT) - 1
print(AVG_WAITING_TIME)

