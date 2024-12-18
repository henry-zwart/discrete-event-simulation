"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    In this file we look at the relative waiting times between a system with
    a different number of servers. The same load characteristics are used
    (system load ρ and processor capacity µ), with an exponential service dis-
    tribution and a FIFO scheduling algorithm. The difference between the average
    waiting time for 1, 2 and 4 servers are compared. Welch is used to ensure
    a statistical signifance.
"""

import random

import numpy as np
from main import experiment


def run():
    """Runs the system for a different number of servers."""
    seed = 145
    sim_time = 2000
    num_runs = 100
    service_dis = "exponential"
    fifo = True
    rho = 0.95

    avg_wait_nr_servers = np.array(
        [
            experiment(
                num_runs=num_runs,
                seed=seed,
                sim_time=sim_time,
                rho=rho,
                fifo=fifo,
                service_dis=service_dis,
                n_servers=n,
            )
            for n in (1, 2, 4)
        ]
    )

    np.save("data/exercise_2_avg_wait_nr_servers", avg_wait_nr_servers)

    # Simulates for multiple values of rho and number of runs and gets statistics.
    avg_wait_nr_servers = []
    means_dict = {}
    std_dict = {}
    rho_list = [0.5, 0.65, 0.8, 0.95]
    sim_time_list = [x for x in range(100, 300, 50)]
    np.save("data/sim_time_list", sim_time_list)
    np.save("data/rho_list", rho_list)
    for rho in rho_list:
        means_dict[(rho)] = []
        std_dict[(rho)] = []
        for sim_time in sim_time_list:
            avg_wait_nr_servers = np.array(
                [
                    experiment(
                        num_runs=num_runs,
                        seed=seed,
                        sim_time=sim_time,
                        rho=rho,
                        fifo=fifo,
                        service_dis=service_dis,
                        n_servers=n,
                    )
                    for n in (1, 2, 4)
                ]
            )
            means_dict[(rho)].append(np.mean(avg_wait_nr_servers, axis=1))
            std_dict[(rho)].append(np.std(avg_wait_nr_servers, axis=1, ddof=1))

    upper = {}
    lower = {}

    for rho in rho_list:
        lower[(rho)] = np.array(means_dict[(rho)]) - np.array(std_dict[(rho)]) * 2
        upper[(rho)] = np.array(means_dict[(rho)]) + np.array(std_dict[(rho)]) * 2
        np.save(f"data/means_{rho}", means_dict[(rho)])
        np.save(f"data/std_{rho}", std_dict[(rho)])
        np.save(f"data/lower_{rho}", lower[(rho)])
        np.save(f"data/upper_{rho}", upper[(rho)])


if __name__ == "__main__":
    random.seed(145)
    run()
