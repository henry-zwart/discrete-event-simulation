"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file plots the results from the file exercise_2_5.
"""

import sys

import matplotlib.pyplot as plt
import numpy as np


def plot(rhos, ns):
    """Plots results from the file exercise_2_5."""
    fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharey=True)

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

    fig.legend()
    fig.supxlabel("Measurement time")
    fig.supylabel("Expected waiting time")
    fig.tight_layout()
    fig.savefig("results/figures/wait_time_vs_measure_time.png", dpi=500)


if __name__ == "__main__":
    try:
        rhos, ns = sys.argv[1:3]
        rhos = rhos.split(" ")
        ns = ns.split(" ")
    except IndexError as err:
        raise ValueError("Expected two arguments: rho's, n's") from err
    except ValueError as err:
        raise ValueError("Could not parse parameters.") from err

    plot(rhos, ns)
