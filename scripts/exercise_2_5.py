import sys

import numpy as np
from main import experiment
from tqdm import tqdm


def run(rho):
    measure_times = np.arange(100, 5000, 100)
    means = []
    cis = []
    for n in (1, 2, 4):
        n_means = []
        n_cis = []
        for mt in tqdm(measure_times):
            wait_times = experiment(
                num_runs=100,
                seed=42,
                sim_time=mt,
                rho=rho,
                fifo=True,
                service_dis="exponential",
                n_servers=n,
            )
            avg = wait_times.mean()
            std = wait_times.std(ddof=1)
            ci = 3 * std / np.sqrt(100)
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
        rho = sys.argv[1]
        rho = float(rho)
    except IndexError as err:
        raise ValueError("Expected two arguments: rho, n_servers") from err
    except ValueError as err:
        raise ValueError("Could not parse parameter rho.") from err

    run(rho)
