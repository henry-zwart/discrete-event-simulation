"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    ...
    Arrival rate (lambda)
    Capacity (mu)
"""

import itertools
import random

import numpy as np
import simpy
from scipy.stats import ttest_ind

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()


class System:
    """Class for the system."""

    def __init__(self, env, nr_servers, fifo):
        """Sets up system for new run."""
        self.env = env
        if fifo:
            self.server = simpy.Resource(env, nr_servers)
        else:
            self.server = simpy.PriorityResource(env, nr_servers)

    def serv(self, servicetime):
        """A client is served."""
        yield self.env.timeout(servicetime)

    def request(self, priority=0):
        """A client requests being served."""
        if isinstance(self.server, simpy.PriorityResource):
            return self.server.request(priority).__enter__()
        else:
            return self.server.request().__enter__()


def client(env, system, servicetime):
    """Function handles the proces of a client."""
    global AVG_WAITING_TIME
    time_entering_system = env.now

    # tells enviroment new customer arrives
    with system.request(servicetime) as request:
        yield request

        time_being_serviced = env.now
        AVG_WAITING_TIME += time_being_serviced - time_entering_system

        yield env.process(system.serv(servicetime))


def setup(env, nr_servers, capacity, rho, fifo, service_dis):
    """Set up for system. New clients enter system  and get a service
    time appointed."""
    global CLIENT_COUNT

    arrival_rate = rho * nr_servers * capacity
    system = System(env, nr_servers, fifo)

    # In this while loop new clients enter the system and get a service
    # time appointed.
    while True:
        if service_dis == "exponential":
            servicetime = np.random.exponential(1 / capacity)
        elif service_dis == "deterministic":
            servicetime = 1 / capacity
        elif service_dis == "hyperexponential":
            # TODO: make expected value same
            if np.random.random() < 0.75:
                servicetime = np.random.exponential(1 / capacity)
            else:
                servicetime = np.random.exponential(5 / capacity)
        else:
            raise ValueError(f"Unknown service-time distribution: {service_dis}")

        yield env.timeout(np.random.exponential(1 / arrival_rate))
        env.process(client(env, system, servicetime))


def run(seed, sim_time, nr_servers, capacity, rho, fifo, service_dis):
    """This function runs the simulation from start to end."""

    # Resets global variables.
    global AVG_WAITING_TIME
    global CLIENT_COUNT
    global SIM_TIME
    AVG_WAITING_TIME = 0
    CLIENT_COUNT = itertools.count()
    SIM_TIME = sim_time

    # Standard seed, to make results consistent.
    random.seed(seed)

    # Starts up simpy environment.
    env = simpy.Environment()
    env.process(setup(env, nr_servers, capacity, rho, fifo, service_dis))
    env.run(until=SIM_TIME)

    # At the end of the run, the avg waiting time is calculated.
    nr_clients = next(CLIENT_COUNT)
    AVG_WAITING_TIME /= nr_clients - 1

    return (nr_clients, AVG_WAITING_TIME)


def experiment():
    """From this function runs are called to gather data."""
    avg_wait_nr_servers = []

    num_runs = 5
    for nr_servers in [1, 2, 4]:
        print("nr_servers: ", nr_servers)
        waiting_time_runs = []
        for i in range(num_runs):
            print("run: ", i)
            waiting_time = run(
                145,
                10000,
                nr_servers,
                capacity=1,
                rho=0.95,
                fifo=False,
                service_dis="hyperexponential",
            )
            waiting_time_runs.append(waiting_time)
        avg_wait_nr_servers.append(waiting_time_runs)

    # This is for the statistical significance.
    avg_wait_nr_servers = np.array(avg_wait_nr_servers)
    list_means = np.mean(avg_wait_nr_servers, axis=1)
    list_std = np.std(avg_wait_nr_servers, axis=1, ddof=1)

    print(list_means)
    print(list_std)

    # WELCH, this is for the statistical significance.
    welch = ttest_ind(avg_wait_nr_servers[0], avg_wait_nr_servers[1], equal_var=False)
    print(welch)


experiment()
