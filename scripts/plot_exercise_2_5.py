"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file plots the results from the file exercise_2_5.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from discrete_event_sim.plots import save_fig


def plot_wait_vs_measure_duration(rhos, ns):
    """Plots results from the file exercise_2_5."""
    fig, axes = plt.subplots(1, 3, figsize=(6, 2.5), sharey=True)

    for i, rho in enumerate(rhos):
        for n, color in zip(ns, ("red", "green", "blue"), strict=False):
            params_str = f"{rho}_{n}"
            means = np.load(f"data/ex2_means_{params_str}.npy")
            cis = np.load(f"data/ex2_cis_{params_str}.npy")
            measure_times = np.load(f"data/ex2_measure_times_{params_str}.npy")

            axes[i].plot(
                measure_times, means, color=color, label=str(n) if i == 0 else None
            )
            axes[i].plot(measure_times, means + cis, color=color)
            axes[i].plot(measure_times, means - cis, color=color)
            axes[i].fill_between(
                measure_times,
                means - cis,
                means + cis,
                alpha=0.5,
                color=color,
            )
        float_rho = float(f"0.{rho}")
        axes[i].set_title(r"$\rho$ = " + f"{float_rho:.2f}")

    fig.legend(loc="center left", bbox_to_anchor=(1, 0.5), title=r"$n$")
    fig.supxlabel("Measurement duration")
    fig.supylabel(r"$E(W_n)$")
    fig.tight_layout()
    save_fig(fig, "wait_time_vs_measure_time", Path("results/figures"))


def plot_wait_time_by_rho(rhos, ns):
    """Plots expected wait time against rho for FIFO M/M/n, service-order M/M/1"""
    fig, ax = plt.subplots(figsize=(3, 2.5))

    float_rhos = [float(f"0.{rho}") for rho in rhos]
    for n, color in zip(ns, ("red", "green", "blue"), strict=False):
        config_means = []
        config_lower = []
        config_upper = []
        for rho in rhos:
            params_str = f"{rho}_{n}"
            rho_avgs = np.load(f"data/ex2_means_{params_str}_5000_fifo.npy")
            rho_mean = rho_avgs.mean()
            rho_ci = 1.96 * rho_avgs.std(ddof=1) / np.sqrt(rho_avgs.size)
            config_means.append(rho_mean)
            config_lower.append(rho_mean - rho_ci)
            config_upper.append(rho_mean + rho_ci)

        ax.plot(float_rhos, config_means, color=color, label=f"{n}")
        ax.plot(float_rhos, config_lower, color=color, alpha=0.7)
        ax.plot(float_rhos, config_upper, color=color, alpha=0.7)
        ax.fill_between(float_rhos, config_lower, config_upper, alpha=0.5, color=color)

    # Plot M/M/1 service-order prio
    config_means = []
    config_lower = []
    config_upper = []
    for rho in rhos:
        rho_avgs = np.load(f"data/ex2_means_{rho}_1_5000_prio.npy")
        rho_mean = rho_avgs.mean()
        rho_ci = 1.96 * rho_avgs.std(ddof=1) / np.sqrt(rho_avgs.size)
        config_means.append(rho_mean)
        config_lower.append(rho_mean - rho_ci)
        config_upper.append(rho_mean + rho_ci)
    ax.plot(float_rhos, config_means, color="purple", label="1 (ST)")
    ax.plot(float_rhos, config_lower, color="purple", alpha=0.7)
    ax.plot(float_rhos, config_upper, color="purple", alpha=0.7)
    ax.fill_between(float_rhos, config_lower, config_upper, alpha=0.5, color="purple")

    ax.set_xlim(0.8, 1.0)
    ax.set_xlabel(r"$\rho$")
    ax.set_ylabel(r"$E(W)$")
    # fig.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.legend(
        loc="lower center",
        bbox_to_anchor=(0.55, 0.95),
        fontsize=8,
        handlelength=1,
        title=r"$n$",
        ncol=4,
    )
    fig.tight_layout()
    save_fig(fig, "exp_wait_at_5000", Path("results/figures"))


if __name__ == "__main__":
    try:
        rhos, ns = sys.argv[1:3]
        rhos = rhos.split(" ")
        ns = ns.split(" ")
    except IndexError as err:
        raise ValueError("Expected two arguments: rho's, n's") from err
    except ValueError as err:
        raise ValueError("Could not parse parameters.") from err

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

    plot_wait_vs_measure_duration(rhos, ns)
    plot_wait_time_by_rho(rhos, ns)
