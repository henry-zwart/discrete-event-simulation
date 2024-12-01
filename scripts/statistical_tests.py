import json
import random
import sys
from pathlib import Path

import numpy as np
from scipy.stats import ttest_ind


def run(rhos, ns):
    sig_results = {}
    for rho in rhos:
        avg_results = []

        # Load FIFO results
        for n in ns:
            avg_results.append(np.load(f"data/ex2_means_{rho}_{n}_5000_fifo.npy"))

        # Load M/M/1 service-order priority results
        avg_results.append(np.load(f"data/ex2_means_{rho}_1_5000_prio.npy"))

        # Compare FIFO M/M/1 to each other config
        rho_sig_results = [
            ttest_ind(avg_results[0], avg_results[i], equal_var=False).pvalue
            for i in range(1, 4)
        ]
        sig_results[rho] = {
            "mm1,mm2": rho_sig_results[0],
            "mm1,mm4": rho_sig_results[1],
            "mm1,mm1_prio": rho_sig_results[2],
        }
        if rho == rhos[-1]:
            sig_results[rho]["mm4,mm1_prio"] = ttest_ind(
                avg_results[2], avg_results[3], equal_var=False
            ).pvalue

    with Path("results/sig_tests.json").open("w") as f:
        json.dump(sig_results, f)


if __name__ == "__main__":
    random.seed(145)
    try:
        rhos, ns = sys.argv[1:3]
        rhos = rhos.split(" ")
        ns = ns.split(" ")
    except IndexError as err:
        raise ValueError("Expected two arguments: rho's, n's") from err
    except ValueError as err:
        raise ValueError("Could not parse parameters.") from err
    run(rhos, ns)
