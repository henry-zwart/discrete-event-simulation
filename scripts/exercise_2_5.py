"""
Course: Stochastic Simulation
Names: Petr Chalupský, Henry Zwart, Tika van Bennekum
Student IDs: 15719227, 15393879, 13392425
Assignement: DES simulation	assignment

File description:
    This file elaborates on exercise_2.py.
"""

import sys

import numpy as np
from main import experiment
from tqdm import tqdm


def run(rho, n):
    measure_times = np.arange(200, 5001, 200)
    means = []
    cis = []
    for mt in tqdm(measure_times):
        wait_times = experiment(
            num_runs=100,
            seed=125,
            sim_time=mt,
            rho=rho,
            fifo=True,
            service_dis="exponential",
            n_servers=n,
        )
        avg = wait_times.mean()
        std = wait_times.std(ddof=1)
        ci = 2.576 * std / np.sqrt(100)
        means.append(avg)
        cis.append(ci)
    means = np.array(means)
    cis = np.array(cis)
    rho_label = str(rho)[2:]
    n_label = str(n)
    np.save(f"data/ex2_measure_times_{rho_label}_{n_label}.npy", measure_times)
    np.save(f"data/ex2_cis_{rho_label}_{n_label}.npy", cis)
    np.save(f"data/ex2_means_{rho_label}_{n_label}.npy", means)


if __name__ == "__main__":
    try:
        rho, n = sys.argv[1:3]
        rho = f"0.{rho}"
        rho = float(rho)
        n = int(n)
    except IndexError as err:
        raise ValueError("Expected two arguments: rho, n_servers") from err
    except ValueError as err:
        raise ValueError("Could not parse parameter rho.") from err

    run(rho, n)
