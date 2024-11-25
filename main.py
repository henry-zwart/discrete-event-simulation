"""
DES

For this assignment we’ll be using the following notation:
λ – the arrival rate into the system as a whole.
µ – the capacity of each of n equal servers.
ρ represents the system load. In a single server system, it will be: ρ=λ/µ
In a multi-server system (one queue with n equal servers, each with capacity µ),
it will be
ρ=λ/(nµ).
"""

import itertools
import random

import numpy as np
import simpy

SIM_TIME = 0
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
    # print(f'a client {id} arrives the system at {time_entering_system:.2f}.')
    with system.server.request() as request:
        yield request

        time_being_serviced = env.now
        # print(f'a client {id} is being serviced at {time_being_serviced:.2f}.')
        AVG_WAITING_TIME += time_being_serviced - time_entering_system
        yield env.process(system.serv(servicetime))
        # print(f'a client {id} stopped being serviced at {env.now:.2f}.')


def setup(env, nr_servers, arrival_rate, rho):
    global CLIENT_COUNT
    # arrival rate = lambda
    capacity = arrival_rate / (rho * nr_servers)
    system = System(env, nr_servers)

    while True:
        servicetime = np.random.exponential(1 / capacity)
        yield env.timeout(np.random.exponential(1 / arrival_rate))
        env.process(client(env, system, servicetime, next(CLIENT_COUNT)))


def run(seed, sim_time, nr_servers, arrival_rate, rho):
    global AVG_WAITING_TIME
    global CLIENT_COUNT
    global SIM_TIME
    AVG_WAITING_TIME = 0
    CLIENT_COUNT = itertools.count()
    SIM_TIME = sim_time

    random.seed(seed)
    env = simpy.Environment()

    env.process(setup(env, nr_servers, arrival_rate, rho))
    env.run(until=SIM_TIME)
    nr_clients = next(CLIENT_COUNT)
    AVG_WAITING_TIME /= nr_clients - 1

    return (nr_clients, AVG_WAITING_TIME)


def experiment():
    avg_wait_nr_servers = []

    num_runs = 5
    for nr_servers in [1, 2, 4]:
        print("nr_servers: ", nr_servers)
        waiting_time_runs = 0
        for i in range(num_runs):
            print("run: ", i)
            nr_clients, waiting_time = run(
                145, 10000, nr_servers, arrival_rate=1, rho=0.75
            )
            waiting_time_runs += waiting_time
        avg_wait_nr_servers.append(waiting_time_runs / num_runs)

    print(avg_wait_nr_servers)


experiment()
