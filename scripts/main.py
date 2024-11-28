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

import random
from dataclasses import dataclass, field

import numpy as np
import simpy


@dataclass
class ClientData:
    """Event times for a specific client."""

    _id: int
    arrived_at: float
    service_time: float
    served_at: float | None = None
    departed_at: float | None = None

    def be_served(self, at_time: float):
        """Update served_at when server is available for client."""
        self.served_at = at_time

    def depart(self, at_time: float):
        """Update departed_at when client finished with server."""
        self.departed_at = at_time

    def waiting_time(self) -> float | None:
        """Time elapsed from arrival to start of service."""
        if self.served_at is None:
            return None
        return self.served_at - self.arrived_at

    def sojourn_time(self) -> float | None:
        """Total time in system. Only defined for departed clients."""
        if self.departed_at is None:
            return None
        return self.departed_at - self.arrived_at


@dataclass
class SimulationData:
    """Data for a single experiment."""

    clients: dict[int, ClientData] = field(default_factory=dict)

    def add_client(self, c: ClientData):
        """A new client has joined the queue."""
        self.clients[c._id] = c

    def n_arrived(self) -> int:
        """Total number of clients who have been in the system."""
        return len(self.clients)

    def n_waiting(self) -> int:
        """Those clients who have arrived but not been served."""
        return len([c for c in self.clients.values() if c.served_at is None])

    def n_in_system(self) -> int:
        """Those clients who have not yet departed. May be waiting or being served."""
        return len([c for c in self.clients.values() if c.departed_at is None])

    def n_served(self) -> int:
        """Those clients who are no longer in the system."""
        return len(self.clients) - self.n_in_system()

    def mean_waiting_time(self) -> float:
        """Average waiting time for clients _not still waiting_."""
        return np.mean(
            [wt for c in self.clients.values() if (wt := c.waiting_time()) is not None]
        ).astype(float)


class System:
    """Coupled system: servers and clients (queues).

    Includes generation of new clients."""

    def __init__(
        self,
        env,
        nr_servers,
        capacity: float,
        service_dist: str = "exponential",
        fifo=False,
    ):
        """Initialise system.

        env: (SimPy environment) event loop.
        nr_servers: (int) number of clients who can be served concurrently.
        capacity: (float) number of clients who can be processed per unit time
            by a given server.
        service_dist: (str) distribution for the service time, one of
            {exponential, deterministic, hyperexponential}.
        fifo: (bool) if true, clients are selected in order of arrival. If false,
            clients are selected in increasing order of service time.
        """
        # Internal data
        self.env = env
        self.capacity = capacity
        self.record = SimulationData()

        # Initialise servers
        if fifo:
            self.server = simpy.Resource(self.env, nr_servers)
        else:
            self.server = simpy.PriorityResource(self.env, nr_servers)

        # Choose service time distribution
        if service_dist == "exponential":
            self.sample_service_time = self._sample_exp_service_time
        elif service_dist == "deterministic":
            self.sample_service_time = self._det_service_time
        elif service_dist == "hyperexponential":
            self.sample_service_time = self._sample_hexp_service_time
        else:
            raise ValueError(f"Unknown service-time distribution: {service_dist}")

    def generate_clients(self, arrival_rate: float):
        """Continuously generate new clients with exponential interarrival times."""
        while True:
            # Sample next arrival time, and wait for this duration
            next_arrival = np.random.exponential(1 / arrival_rate)
            yield self.env.timeout(next_arrival)

            # Then spawn the new client process
            self.env.process(self.spawn_client(name=len(self.record.clients)))

    def spawn_client(self, name: int):
        """Create a new client process and run it."""
        # Calculate initial client data and add to records
        arrival_time = self.env.now
        service_time = self.sample_service_time()
        client = ClientData(
            _id=name,
            arrived_at=arrival_time,
            service_time=service_time,
        )
        self.record.add_client(client)

        with self.request(client) as request:
            # Request a server -> enter queue
            yield request

            # Server free -> serve client
            client.be_served(self.env.now)
            yield self.env.process(self.serve(client))

            # Client finished -> depart
            client.depart(self.env.now)

    def serve(self, c: ClientData):
        """Serve a client."""
        yield self.env.timeout(c.service_time)

    def request(self, client_data: ClientData):
        """Request access to a server.

        Unifies access via regular FIFO and service-time priority.
        """
        if isinstance(self.server, simpy.PriorityResource):
            return self.server.request(client_data.service_time).__enter__()  # type: ignore
        else:
            return self.server.request().__enter__()

    def _sample_exp_service_time(self) -> float:
        """Helper function: sample service times from exponential dist."""
        return np.random.exponential(1 / self.capacity)

    def _det_service_time(self) -> float:
        """Helper function: sample service times deterministically."""
        return 1 / self.capacity

    def _sample_hexp_service_time(self) -> float:
        """Helper function: sample service times from hyperexponential dist."""
        if np.random.random() < 0.75:
            return np.random.exponential(1 / self.capacity)
        else:
            return np.random.exponential(5 / self.capacity)


def setup(
    env,
    nr_servers,
    capacity,
    rho,
    fifo=True,
    service_dis="exponential",
) -> System:
    """Initialises a system and the client-generating process.

    The arrival rate is calculated w.r.t. the total load, number
    of servers, and individual server capacity.

    Fifo specifies whether clients should be served in arrival order
    (True) or in increasing order of service time (False).

    Service dis specifies the distribution from which to sample
    client service times. Valid options are 'exponential', 'deterministic',
    and 'hyperexponential'.
    """
    arrival_rate = rho * nr_servers * capacity
    system = System(env, nr_servers, capacity, service_dis, fifo)
    env.process(system.generate_clients(arrival_rate))
    return system


def run(seed, sim_time, nr_servers, capacity, rho, fifo, service_dis):
    """Simulate an M/(M,D,G)/n queue, and return the average waiting time."""
    random.seed(seed)
    env = simpy.Environment()
    system = setup(env, nr_servers, capacity, rho, fifo, service_dis)
    env.run(until=sim_time)
    avg_waiting_time = system.record.mean_waiting_time()
    return avg_waiting_time


def experiment(num_runs, seed, sim_time, rho, fifo, service_dis):
    """From this function runs are called to gather data."""
    avg_wait_nr_servers = []

    for nr_servers in [1, 2, 4]:
        print("nr_servers: ", nr_servers)
        waiting_time_runs = []
        for i in range(num_runs):
            print("run: ", i)
            waiting_time = run(
                seed,
                sim_time,
                nr_servers,
                capacity=1,
                rho=rho,
                fifo=fifo,
                service_dis=service_dis,
            )
            waiting_time_runs.append(waiting_time)
        avg_wait_nr_servers.append(waiting_time_runs)

    # This is for the statistical significance.
    avg_wait_nr_servers = np.array(avg_wait_nr_servers)

    return avg_wait_nr_servers
