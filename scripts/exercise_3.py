"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    In this file we look at the relative waiting times between using a FIFO
    or a shortest job first scheduling algorithm. The system used is M/M/1.
"""

import itertools
import sys

import numpy as np
from main import experiment

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()


def run(rho: float):
    seed = 145
    sim_time = 5000
    num_runs = 100
    n_servers = 1
    service_dis = "exponential"
    fifo = False

    avg_wait = experiment(
        num_runs=num_runs,
        seed=seed,
        sim_time=sim_time,
        rho=rho,
        fifo=fifo,
        service_dis=service_dis,
        n_servers=n_servers,
    )
    rho_label = str(rho)[2:]
    np.save(f"data/ex2_means_{rho_label}_{n_servers}_{sim_time}_prio.npy", avg_wait)


if __name__ == "__main__":
    try:
        rho = sys.argv[1]
        rho = f"0.{rho}"
        rho = float(rho)
    except IndexError as err:
        raise ValueError("Expected one argument: rho") from err
    except ValueError as err:
        raise ValueError("Could not parse parameter rho.") from err

    run(rho)
# results_dictionary = {
#     "FIFO": avg_wait_nr_servers_fifo[0],
#     "NOT_FIFO": avg_wait_nr_servers_not_fifo[0],
# }
#
#
# plt.rc("xtick", labelsize=14)
# plt.rc("ytick", labelsize=14)
# plt.rc("axes", labelsize=18)
#
# fig, ax = plt.subplots(figsize=(12, 12))
# sns.boxplot(results_dictionary, ax=ax)
# sns.swarmplot(data=results_dictionary, color="k")
#
# ax.set_ylabel("Average waiting time")
# plt.savefig("results/figures/exercise_3_boxplot.png", dpi=300)
