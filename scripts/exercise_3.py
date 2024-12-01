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

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from main import experiment

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()


seed = 145
sim_time = 5000
num_runs = 30
service_dis = "exponential"
fifo = True
rho = 0.99

avg_wait_nr_servers_fifo = np.array(
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

fifo = False

avg_wait_nr_servers_not_fifo = np.array(
    [
        experiment(
            num_runs=num_runs,
            seed=seed,
            sim_time=sim_time,
            rho=rho,
            fifo=fifo,
            service_dis=service_dis,
        )
        for n in (1, 2, 4)
    ]
)

results_dictionary = {
    "FIFO": avg_wait_nr_servers_fifo[0],
    "NOT_FIFO": avg_wait_nr_servers_not_fifo[0],
}


plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
plt.rc("axes", labelsize=18)

fig, ax = plt.subplots(figsize=(12, 12))
sns.boxplot(results_dictionary, ax=ax)
sns.swarmplot(data=results_dictionary, color="k")

ax.set_ylabel("Average waiting time")
plt.savefig("results/figures/exercise_3_boxplot.png", dpi=300)
