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

avg_wait_nr_servers_exponential = experiment(
    num_runs=num_runs,
    seed=seed,
    sim_time=sim_time,
    rho=rho,
    fifo=fifo,
    service_dis=service_dis,
)

service_dis = "deterministic"

avg_wait_nr_servers_deterministic = experiment(
    num_runs=num_runs,
    seed=seed,
    sim_time=sim_time,
    rho=rho,
    fifo=fifo,
    service_dis=service_dis,
)

service_dis = "hyperexponential"

avg_wait_nr_servers_hyperexponential = experiment(
    num_runs=num_runs,
    seed=seed,
    sim_time=sim_time,
    rho=rho,
    fifo=fifo,
    service_dis=service_dis,
)


results_dictionary = {
    "exponential_1": avg_wait_nr_servers_exponential[0],
    "exponential_2": avg_wait_nr_servers_exponential[1],
    "exponential_4": avg_wait_nr_servers_exponential[2],
    "deterministic_1": avg_wait_nr_servers_deterministic[0],
    "deterministic_2": avg_wait_nr_servers_deterministic[1],
    "deterministic_4": avg_wait_nr_servers_deterministic[2],
    "hyperexponential_1": avg_wait_nr_servers_hyperexponential[0],
    "hyperexponential_2": avg_wait_nr_servers_hyperexponential[1],
    "hyperexponential_4": avg_wait_nr_servers_hyperexponential[2],
}


plt.rc("xtick", labelsize=14)
plt.rc("ytick", labelsize=14)
plt.rc("axes", labelsize=18)

fig, ax = plt.subplots(figsize=(12, 12))
sns.boxplot(results_dictionary, ax=ax)
sns.swarmplot(data=results_dictionary, color="k")

ax.set_xlabel("Number of servers")
ax.set_ylabel("Average waiting time")

plt.savefig("../figures/exercise_4_boxplot.png", dpi=300)
