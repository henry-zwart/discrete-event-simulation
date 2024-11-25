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

SIM_TIME = 1

class system:
    def __init__(self, env, nr_servers):
        self.env = env
        self.server = simpy.Resource(env, nr_servers)

    def serv(self, servicetime):
        yield self.env.timeout(servicetime)

def client(env, system, servicetime):
    # tells enviroment new customer arrives
    with system.server.request() as request:
        yield request

        yield env.process(system.service(servicetime))

def setup(env, nr_servers, arrival_rate, capacity):
    # arrival rate = lambda
    
    while True:
        servicetime = np.random.poisson(1 / capacity)
        yield  env.timeout(np.random.poisson(1 / capacity))
        env.process(client(env, system, servicetime))


random.seed(145)

env = simpy.Environment()
env.process(setup(env, nr_servers=1))
env.run(until=SIM_TIME)

