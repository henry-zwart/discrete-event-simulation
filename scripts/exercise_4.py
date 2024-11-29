import itertools

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from main import experiment
from tqdm import tqdm

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()


seed = 145
sim_time = 2000
num_runs = 30
rhos = np.arange(0.5, 1, 0.01)
n_tuple = (1, 2, 4)
# plot avg waiting time for each n show each distribution as a plot of rho


def run_exercise_4():
    servers_means = []
    servers_cis = []
    for n in tqdm(n_tuple):
        n_means = []
        n_cis = []
        for service_dis in ("exponential", "deterministic", "hyperexponential"):
            service_means = []
            service_cis = []
            for rho in tqdm(rhos):
                wait_times = experiment(
                    num_runs=num_runs,
                    seed=seed,
                    sim_time=sim_time,
                    rho=rho,
                    service_dis=service_dis,
                    n_servers=n,
                )
                avg = wait_times.mean()
                std = wait_times.std(ddof=1)
                ci = 1.96 * std / np.sqrt(num_runs)
                service_means.append(avg)
                service_cis.append(ci)
            n_means.append(service_means)
            n_cis.append(service_cis)
        servers_means.append(n_means)
        servers_cis.append(n_cis)

    return servers_means, servers_cis


servers_means, servers_cis = run_exercise_4()

np.save("data/rhos.npy", rhos)
np.save("data/servers_means.npy", servers_means)
np.save("data/servers_cis.npy", servers_cis)
