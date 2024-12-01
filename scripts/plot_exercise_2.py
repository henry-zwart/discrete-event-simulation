"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file plots the results from the file exercise_2.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Plot box plot

avg_wait = np.load("data/exercise_2_avg_wait_nr_servers.npy")

results_dictionary = {"1": avg_wait[0], "2": avg_wait[1], "4": avg_wait[2]}
plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
plt.rc("axes", labelsize=18)

fig, ax = plt.subplots(figsize=(12, 12))
sns.boxplot(results_dictionary, ax=ax)
sns.swarmplot(data=results_dictionary, color="k")

ax.set_xlabel("Number of servers")
ax.set_ylabel("Average waiting time")

plt.savefig("results/figures/exercise_2_boxplot.png", dpi=300)


means_dict = {}
std_dict = {}
lower_dict = {}
upper_dict = {}

sim_time_list = np.load("data/sim_time_list.npy")
rho_list = np.load("data/rho_list.npy")


for rho in rho_list:
    means_dict[(rho)] = np.load(f"data/means_{rho}.npy")
    std_dict[(rho)] = np.load(f"data/std_{rho}.npy")
    lower_dict[(rho)] = np.load(f"data/lower_{rho}.npy")
    upper_dict[(rho)] = np.load(f"data/upper_{rho}.npy")

# Plots results with confidence intervals.
fig, axes = plt.subplots(4, sharex=True, sharey=True, figsize=(12, 12))
for i, rho in enumerate(rho_list):
    axes[i].plot(sim_time_list, np.take(np.array(means_dict[(rho)]), 0, axis=1))
    axes[i].plot(sim_time_list, np.take(np.array(means_dict[(rho)]), 1, axis=1))
    axes[i].plot(sim_time_list, np.take(np.array(means_dict[(rho)]), 2, axis=1))
    axes[i].fill_between(
        sim_time_list,
        np.take(np.array(upper_dict[rho]), 0, axis=1),
        np.take(np.array(lower_dict[rho]), 0, axis=1),
        alpha=0.5,
    )
    axes[i].fill_between(
        sim_time_list,
        np.take(np.array(upper_dict[rho]), 1, axis=1),
        np.take(np.array(lower_dict[rho]), 1, axis=1),
        alpha=0.5,
    )
    axes[i].fill_between(
        sim_time_list,
        np.take(np.array(upper_dict[rho]), 2, axis=1),
        np.take(np.array(lower_dict[rho]), 2, axis=1),
        alpha=0.5,
    )

    axes[i].text(
        1.05,
        0.5,
        horizontalalignment="center",
        verticalalignment="center",
        s=f"rho = {rho}",
        transform=axes[i].transAxes,
        rotation=45,
    )


fig.supylabel("Average waiting time")
fig.supxlabel("Simulation time")
axes[0].text(0.1, 0.5, f"rho={rho}")
plt.savefig("results/figures/exercise_2_confidence_plot", dpi=300)
