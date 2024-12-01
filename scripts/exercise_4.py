"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    In this file we look at the relative waiting times between a system with
    different service time distributions:
        - Exponential
        - Deterministic
        - Hyperexponential
"""

import random

import numpy as np
from main import experiment
from tqdm import tqdm


# Plots avg waiting time for each n show each distribution as a plot of rho.
def run_exercise_4():
    seed = 145
    sim_time = 5000
    num_runs = 100
    rhos = np.array([0.8, 0.9, 0.98])
    n_tuple = (1, 2, 4)

    servers_means = []
    servers_cis = []
    with tqdm(
        total=len(n_tuple) * 3 * len(rhos),
        desc="Compare service distributions",
    ) as pbar:
        for n in n_tuple:
            n_means = []
            n_cis = []
            for service_dis in ("exponential", "deterministic", "hyperexponential"):
                service_means = []
                service_cis = []
                for rho in rhos:
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
                    pbar.update()
                n_means.append(service_means)
                n_cis.append(service_cis)
            servers_means.append(n_means)
            servers_cis.append(n_cis)

    np.save("data/rhos.npy", rhos)
    np.save("data/servers_means.npy", servers_means)
    np.save("data/servers_cis.npy", servers_cis)


if __name__ == "__main__":
    random.seed(145)
    run_exercise_4()
