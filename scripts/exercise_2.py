import itertools
import random

import numpy as np
import simpy
from scipy.stats import ttest_ind

from main import client, System, setup, run, experiment
import matplotlib.pyplot as plt
import seaborn as sns

SIM_TIME = 0
AVG_WAITING_TIME = 0
CLIENT_COUNT = itertools.count()

seed = 145
sim_time = 2000
num_runs = 30
service_dis = 'exponential'
fifo = True
rho = 0.95


avg_wait_nr_servers = experiment(num_runs=num_runs,seed=seed,sim_time=sim_time,rho = rho, fifo=fifo, service_dis=service_dis)


welch_1_2 = ttest_ind(avg_wait_nr_servers[0], avg_wait_nr_servers[1], equal_var=False)
welch_1_4 = ttest_ind(avg_wait_nr_servers[0],avg_wait_nr_servers[2], equal_var=False)

np.save('../data/exercise_2_avg_wait_nr_servers',avg_wait_nr_servers)



with open("../results/exercise_2.txt", "w") as f:
    f.write(f'{welch_1_2} \n')
    f.write(f'{welch_1_4} \n')
    f.close()


# Simulate for multiple values of rho and number of runs and get statistics
avg_wait_nr_servers = []
means_dict = {}
std_dict = {}
rho_list = [0.5,0.65,0.8,0.95]
#num_runs_list = [x for x in range(5,5,200)]
sim_time_list = [x for x in range(100,300, 50)]
np.save(f'../data/sim_time_list', sim_time_list)
np.save(f'../data/rho_list', rho_list)
for rho in rho_list:
    means_dict[(rho)] = []
    std_dict[(rho)] = []
    for sim_time in sim_time_list:
        avg_wait_nr_servers = experiment(num_runs=num_runs,seed=seed,sim_time=sim_time,rho = rho, fifo=fifo, service_dis=service_dis)
        means_dict[(rho)].append(np.mean(avg_wait_nr_servers,axis=1))
        std_dict[(rho)].append(np.std(avg_wait_nr_servers,axis=1,ddof=1))


upper = {}
lower = {}

for rho in rho_list:
    lower[(rho)] = np.array(means_dict[(rho)]) - np.array(std_dict[(rho)])*2 
    upper[(rho)] = np.array(means_dict[(rho)]) + np.array(std_dict[(rho)])*2
    np.save(f'../data/means_{rho}', means_dict[(rho)])
    np.save(f'../data/std_{rho}', std_dict[(rho)])
    np.save(f'../data/lower_{rho}', lower[(rho)])
    np.save(f'../data/upper_{rho}', upper[(rho)])
