"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file plots the results from the file exercise_4.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from discrete_event_sim.plots import save_fig


def plot_wait_time_by_rho(rhos, servers_means, servers_cis):
    fig, axes = plt.subplots(ncols=3, figsize=(6, 2.5), sharey=True)

    for i, n in enumerate((1, 2, 4)):
        axes[i].set_title(f"n = {n}")

        axes[i].plot(rhos, servers_means[i][0], label="Exp")
        axes[i].plot(rhos, servers_means[i][1], label="Det")
        axes[i].plot(rhos, servers_means[i][2], label="H-Exp")
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
            fig.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    fig.supxlabel(r"$\rho$")
    fig.supylabel(r"$E(W_n)$")

    save_fig(fig, "exercise_4", Path("results/figures"))


def plot_wait_time_by_n(rhos, servers_means, servers_cis):
    fig, axes = plt.subplots(1, 3, sharey=True, figsize=(6, 2.5))
    subset_rho_idx = [30, 40, 45]
    for i, rho_idx in enumerate(subset_rho_idx):
        for j, dist in enumerate(("Exp", "Det", "H-Exp")):
            axes[i].plot(
                np.array([1, 2, 4]),
                servers_means[..., j, rho_idx],
                label=dist if i == 0 else None,
            )
            axes[i].fill_between(
                np.array([1, 2, 4]),
                servers_means[..., j, rho_idx] - servers_cis[..., j, rho_idx],
                servers_means[..., j, rho_idx] + servers_cis[..., j, rho_idx],
                alpha=0.3,
            )
        axes[i].set_title(r"$\rho = $" + f"{rhos[rho_idx]:.2f}")

    fig.supylabel(r"$E(W_n)$")
    fig.supxlabel(r"$n$")
    fig.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    save_fig(fig, "service_dist_by_n", Path("results/figures"))


if __name__ == "__main__":
    FONT_SIZE_SMALL = 9
    FONT_SIZE_DEFAULT = 10
    FONT_SIZE_LARGE = 12

    plt.rc("font", family="Georgia")
    plt.rc("font", weight="normal")  # controls default font
    plt.rc("mathtext", fontset="stix")
    plt.rc("font", size=FONT_SIZE_DEFAULT)  # controls default text sizes
    plt.rc("axes", titlesize=FONT_SIZE_LARGE)  # fontsize of the axes title
    plt.rc("axes", labelsize=FONT_SIZE_DEFAULT)  # fontsize of the x and y labels
    plt.rc("figure", labelsize=FONT_SIZE_DEFAULT)
    plt.rc("xtick", labelsize=FONT_SIZE_SMALL)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=FONT_SIZE_SMALL)  # fontsize of the tick labels

    # plt.rc("axes", titlepad=10)  # add space between title and plot
    plt.rc("figure", dpi=700)  # fix output resolution

    sns.set_context(
        "paper",
        rc={
            "axes.linewidth": 0.5,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "ytick.minor.width": 0.4,
        },
    )

    rhos = np.load("data/rhos.npy")
    servers_means = np.load("data/servers_means.npy")
    servers_cis = np.load("data/servers_cis.npy")

    plot_wait_time_by_rho(rhos, servers_means, servers_cis)
    plot_wait_time_by_n(rhos, servers_means, servers_cis)
