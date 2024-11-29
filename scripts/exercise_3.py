import itertools

import matplotlib.pyplot as plt
import seaborn as sns
from main import experiment

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()


seed = 145
sim_time = 5000
num_runs = 30
service_dis = "exponential"
fifo = True
rho = 0.99

avg_wait_nr_servers_fifo = experiment(
    num_runs=num_runs,
    seed=seed,
    sim_time=sim_time,
    rho=rho,
    fifo=fifo,
    service_dis=service_dis,
)

fifo = False

avg_wait_nr_servers_not_fifo = experiment(
    num_runs=num_runs,
    seed=seed,
    sim_time=sim_time,
    rho=rho,
    fifo=fifo,
    service_dis=service_dis,
)

results_dictionary = {
    "FIFO": avg_wait_nr_servers_fifo[0],
    "NOT_FIFO": avg_wait_nr_servers_not_fifo[0],
}


plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
plt.rc("axes", labelsize=18)

fig, ax = plt.subplots(figsize=(12, 12))
sns.boxplot(results_dictionary, ax=ax)
sns.swarmplot(data=results_dictionary, color="k")


ax.set_ylabel("Average waiting time")

plt.savefig("../figures/exercise_3_boxplot.png", dpi=300)
