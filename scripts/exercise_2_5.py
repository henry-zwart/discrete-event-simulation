import sys

import numpy as np
from main import experiment
from tqdm import tqdm


def run(rho, n):
    measure_times = np.arange(50, 2000, 50)
    means = []
    cis = []
    for n in (1, 2, 4):
        n_means = []
        n_cis = []
        for mt in tqdm(measure_times):
            wait_times = experiment(
                num_runs=50,
                seed=42,
                sim_time=mt,
                rho=rho,
                fifo=False,
                service_dis="exponential",
                n_servers=n,
            )
            avg = wait_times.mean()
            std = wait_times.std(ddof=1)
            ci = 1.96 * std / np.sqrt(50)
            n_means.append(avg)
            n_cis.append(ci)
        means.append(n_means)
        cis.append(n_cis)
    means = np.array(means)
    cis = np.array(cis)
    np.save("data/measure_times.npy", measure_times)
    np.save(f"data/means_rho_{str(rho).replace(".", "_")}.npy", means)
    np.save(f"data/cis_rho_{str(rho).replace(".", "_")}.npy", cis)


if __name__ == "__main__":
    try:
        rho, n = sys.argv[1:3]
        rho = float(rho)
    except IndexError as err:
        raise ValueError("Expected two arguments: rho, n_servers") from err

    run(rho, n)
