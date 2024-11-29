import matplotlib.pyplot as plt
import numpy as np


def plot():
    measure_times = np.load("data/measure_times.npy")

    fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharey=True)
    for i, rho in enumerate((0.5, 0.9, 0.99)):
        means = np.load(f"data/means_rho_{str(rho).replace(".", "_")}.npy")
        cis = np.load(f"data/cis_rho_{str(rho).replace(".", "_")}.npy")
        for j, (n, color) in enumerate(
            zip((1, 2, 4), ("red", "green", "blue"), strict=False)
        ):
            axes[i].plot(
                measure_times, means[j], color=color, label=str(n) if i == 0 else None
            )
            axes[i].plot(measure_times, means[j] + cis[j], color=color)
            axes[i].plot(measure_times, means[j] - cis[j], color=color)
            axes[i].fill_between(
                measure_times,
                means[j] - cis[j],
                means[j] + cis[j],
                alpha=0.5,
                color=color,
            )
        axes[i].set_title(r"$\rho$ = " + f"{rho:.2f}")
    fig.legend()
    fig.supxlabel("Measurement time")
    fig.supylabel("Expected waiting time")

    fig.tight_layout()
    fig.savefig("results/figures/exp_waiting_time.png", dpi=500)


if __name__ == "__main__":
    plot()