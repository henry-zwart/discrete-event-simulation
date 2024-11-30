"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file plots the results from the file exercise_4.
"""

import matplotlib.pyplot as plt
import numpy as np

rhos = np.load("data/rhos.npy")
servers_means = np.load("data/servers_means.npy")
servers_cis = np.load("data/servers_cis.npy")

plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
plt.rc("axes", labelsize=18)

fig, axes = plt.subplots(ncols=3, figsize=(12, 6), sharey=True)

for i, n in enumerate((1, 2, 4)):
    axes[i].set_title(f"n = {n}")

    axes[i].plot(rhos, servers_means[i][0], label="exponential")
    axes[i].plot(rhos, servers_means[i][1], label="deterministic")
    axes[i].plot(rhos, servers_means[i][2], label="hyperexponential")
    axes[i].fill_between(
        rhos,
        servers_means[i][0] - servers_cis[i][0],
        servers_means[i][0] + servers_cis[i][0],
        alpha=0.3,
    )
    axes[i].fill_between(
        rhos,
        servers_means[i][1] - servers_cis[i][1],
        servers_means[i][1] + servers_cis[i][1],
        alpha=0.3,
    )
    axes[i].fill_between(
        rhos,
        servers_means[i][2] - servers_cis[i][2],
        servers_means[i][2] + servers_cis[i][2],
        alpha=0.3,
    )
    if i == 0:
        fig.legend(loc="upper right", bbox_to_anchor=(0.98, 0.9))


fig.supxlabel(r"$\rho$", fontsize=20)
fig.supylabel("Average waiting time", fontsize=20)
fig.tight_layout()
plt.savefig("./figures/exercise_4.png", dpi=300)
