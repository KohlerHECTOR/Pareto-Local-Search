import numpy as np
from indicateurs import *
import matplotlib.pyplot as plt
def to_plot(data, label = None, iter_max = 5):
    for row in data:
        if len(row)< iter_max:
            row += [0 for _ in range(iter_max - len(row))]
    mean_data = np.mean(data, axis = 0)
    std_data = np.std(data, axis = 0)
    plt.plot(mean_data, label = label)
    plt.fill_between(np.arange(len(mean_data)), mean_data + std_data, mean_data - std_data, alpha = 0.2)

NB_INSTANCES = 3
NB_MAX_OBJECTS = 100 # which data were used
ITER_MAX = 5
#### 20 objects ####
NB_OBJECTS = 20
instances_ideals_nadirs_20 = []
instances_pareto_fronts_20 = []
pls1_solve_times_20 = []
pls1_populations_20 = []
pls1_pareto_fronts_20 = []
pls2_solve_times_20 = []
pls2_populations_20 = []
pls2_pareto_fronts_20 = []
pls3_solve_times_20 = []
pls3_populations_20 = []
pls3_pareto_fronts_20 = []
pls4_solve_times_20 = []
pls4_populations_20 = []
pls4_pareto_fronts_20 = []

for i in range(NB_INSTANCES):

    instance_i_pareto_front = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_sols_pareto_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_pareto_front.append([float(x) for x in l.split(", ")])
    instances_pareto_fronts_20.append(instance_i_pareto_front)


    instance_i_ideals_nadirs = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_ideal_nadir_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_ideals_nadirs.append([float(x) for x in l.split(", ")])
    instances_ideals_nadirs_20.append(instance_i_ideals_nadirs)

    ############# PLS1 ###################
    instance_i_pls1_pareto_front = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls1_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls1_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls1_pareto_front.append(iter)

    pls1_pareto_fronts_20.append(instance_i_pls1_pareto_front)


    instance_i_pls1_population = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls1_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls1_population.append(float(l))

    pls1_populations_20.append(instance_i_pls1_population)


    instance_i_pls1_time = 0
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls1_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls1_time = float(lines[0][0])
    pls1_solve_times_20.append(instance_i_pls1_time)

    ######### PLS2 ##########


    instance_i_pls2_pareto_front = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls2_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls2_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls2_pareto_front.append(iter)

    pls2_pareto_fronts_20.append(instance_i_pls2_pareto_front)


    instance_i_pls2_population = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls2_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls2_population.append(float(l))

    pls2_populations_20.append(instance_i_pls2_population)


    instance_i_pls2_time = 0
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls2_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls2_time = float(lines[0][0])
    pls2_solve_times_20.append(instance_i_pls2_time)

    ###### PLS 3 ##########

    instance_i_pls3_pareto_front = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls3_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls3_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls3_pareto_front.append(iter)

    pls3_pareto_fronts_20.append(instance_i_pls3_pareto_front)


    instance_i_pls3_population = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls3_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls3_population.append(float(l))

    pls3_populations_20.append(instance_i_pls3_population)


    instance_i_pls3_time = 0
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls3_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls3_time = float(lines[0][0])
    pls3_solve_times_20.append(instance_i_pls3_time)



    #### PLS4 ##########

    instance_i_pls4_pareto_front = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls4_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls4_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls4_pareto_front.append(iter)

    pls4_pareto_fronts_20.append(instance_i_pls4_pareto_front)


    instance_i_pls4_population = []
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls4_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls4_population.append(float(l))

    pls4_populations_20.append(instance_i_pls4_population)


    instance_i_pls4_time = 0
    with open("data/100_items/_nb_objects_20_" + str(i) + "_pls4_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls4_time = float(lines[0][0])
    pls4_solve_times_20.append(instance_i_pls4_time)



#### 30 objects ####
NB_OBJECTS = 30
instances_ideals_nadirs_30 = []
instances_pareto_fronts_30 = []
pls1_solve_times_30 = []
pls1_populations_30 = []
pls1_pareto_fronts_30 = []
pls2_solve_times_30 = []
pls2_populations_30 = []
pls2_pareto_fronts_30 = []
pls3_solve_times_30 = []
pls3_populations_30 = []
pls3_pareto_fronts_30 = []
pls4_solve_times_30 = []
pls4_populations_30 = []
pls4_pareto_fronts_30 = []

for i in range(NB_INSTANCES):

    instance_i_pareto_front = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_sols_pareto_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_pareto_front.append([float(x) for x in l.split(", ")])
    instances_pareto_fronts_30.append(instance_i_pareto_front)


    instance_i_ideals_nadirs = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_ideal_nadir_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_ideals_nadirs.append([float(x) for x in l.split(", ")])
    instances_ideals_nadirs_30.append(instance_i_ideals_nadirs)

    ############# PLS1 ###################
    instance_i_pls1_pareto_front = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls1_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls1_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls1_pareto_front.append(iter)

    pls1_pareto_fronts_30.append(instance_i_pls1_pareto_front)


    instance_i_pls1_population = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls1_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls1_population.append(float(l))

    pls1_populations_30.append(instance_i_pls1_population)


    instance_i_pls1_time = 0
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls1_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls1_time = float(lines[0][0])
    pls1_solve_times_30.append(instance_i_pls1_time)

    ######### PLS2 ##########


    instance_i_pls2_pareto_front = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls2_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls2_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls2_pareto_front.append(iter)

    pls2_pareto_fronts_30.append(instance_i_pls2_pareto_front)


    instance_i_pls2_population = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls2_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls2_population.append(float(l))

    pls2_populations_30.append(instance_i_pls2_population)


    instance_i_pls2_time = 0
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls2_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls2_time = float(lines[0][0])
    pls2_solve_times_30.append(instance_i_pls2_time)

    ###### PLS 3 ##########

    instance_i_pls3_pareto_front = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls3_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls3_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls3_pareto_front.append(iter)

    pls3_pareto_fronts_30.append(instance_i_pls3_pareto_front)


    instance_i_pls3_population = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls3_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls3_population.append(float(l))

    pls3_populations_30.append(instance_i_pls3_population)


    instance_i_pls3_time = 0
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls3_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls3_time = float(lines[0][0])
    pls3_solve_times_30.append(instance_i_pls3_time)



    #### PLS4 ##########

    instance_i_pls4_pareto_front = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls4_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls4_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls4_pareto_front.append(iter)

    pls4_pareto_fronts_30.append(instance_i_pls4_pareto_front)


    instance_i_pls4_population = []
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls4_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls4_population.append(float(l))

    pls4_populations_30.append(instance_i_pls4_population)


    instance_i_pls4_time = 0
    with open("data/100_items/_nb_objects_30_" + str(i) + "_pls4_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls4_time = float(lines[0][0])
    pls4_solve_times_30.append(instance_i_pls4_time)




##### 50 objects ######
NB_OBJECTS = 50
instances_ideals_nadirs_50 = []
instances_pareto_fronts_50 = []
pls1_solve_times_50 = []
pls1_populations_50 = []
pls1_pareto_fronts_50 = []
pls2_solve_times_50 = []
pls2_populations_50 = []
pls2_pareto_fronts_50 = []
pls3_solve_times_50 = []
pls3_populations_50 = []
pls3_pareto_fronts_50 = []
pls4_solve_times_50 = []
pls4_populations_50 = []
pls4_pareto_fronts_50 = []

for i in range(NB_INSTANCES):

    instance_i_pareto_front = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_sols_pareto_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_pareto_front.append([float(x) for x in l.split(", ")])
    instances_pareto_fronts_50.append(instance_i_pareto_front)


    instance_i_ideals_nadirs = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_ideal_nadir_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            instance_i_ideals_nadirs.append([float(x) for x in l.split(", ")])
    instances_ideals_nadirs_50.append(instance_i_ideals_nadirs)

    ############# PLS1 ###################
    instance_i_pls1_pareto_front = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls1_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls1_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls1_pareto_front.append(iter)

    pls1_pareto_fronts_50.append(instance_i_pls1_pareto_front)


    instance_i_pls1_population = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls1_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls1_population.append(float(l))

    pls1_populations_50.append(instance_i_pls1_population)


    instance_i_pls1_time = 0
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls1_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls1_time = float(lines[0][0])
    pls1_solve_times_50.append(instance_i_pls1_time)

    ######### PLS2 ##########


    instance_i_pls2_pareto_front = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls2_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls2_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls2_pareto_front.append(iter)

    pls2_pareto_fronts_50.append(instance_i_pls2_pareto_front)


    instance_i_pls2_population = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls2_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls2_population.append(float(l))

    pls2_populations_50.append(instance_i_pls2_population)


    instance_i_pls2_time = 0
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls2_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls2_time = float(lines[0][0])
    pls2_solve_times_50.append(instance_i_pls2_time)

    ###### PLS 3 ##########

    instance_i_pls3_pareto_front = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls3_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls3_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls3_pareto_front.append(iter)

    pls3_pareto_fronts_50.append(instance_i_pls3_pareto_front)


    instance_i_pls3_population = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls3_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls3_population.append(float(l))

    pls3_populations_50.append(instance_i_pls3_population)


    instance_i_pls3_time = 0
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls3_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls3_time = float(lines[0][0])
    pls3_solve_times_50.append(instance_i_pls3_time)



    #### PLS4 ##########

    instance_i_pls4_pareto_front = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls4_current_pareto_results.txt", "r") as t:
        lines = t.readlines()
        iter = []
        for j, l in enumerate(lines):
            if l == "NEW ITER\n":
                if j > 0:
                    instance_i_pls4_pareto_front.append(iter)
                iter = []
            else:
                iter.append([float(x) for x in l.split(", ")])
        instance_i_pls4_pareto_front.append(iter)

    pls4_pareto_fronts_50.append(instance_i_pls4_pareto_front)


    instance_i_pls4_population = []
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls4_pop_size_results.txt", "r") as t:
        lines = t.readlines()
        for j, l in enumerate(lines):
            if l != "NEW ITER\n":
                instance_i_pls4_population.append(float(l))

    pls4_populations_50.append(instance_i_pls4_population)


    instance_i_pls4_time = 0
    with open("data/100_items/_nb_objects_50_" + str(i) + "_pls4_times_results.txt", "r") as t:
        lines = t.readlines()
        instance_i_pls4_time = float(lines[0][0])
    pls4_solve_times_50.append(instance_i_pls4_time)







#################### PLOTS AND TABLES ################

#### RES TIMES #####
### 20 objects ##
mean_res_time_pls1_20 = np.array(pls1_solve_times_20).mean()
std_res_time_pls1_20 = np.array(pls1_solve_times_20).std()
mean_res_time_pls2_20 = np.array(pls2_solve_times_20).mean()
std_res_time_pls2_20 = np.array(pls2_solve_times_20).std()
mean_res_time_pls3_20 = np.array(pls3_solve_times_20).mean()
std_res_time_pls3_20 = np.array(pls3_solve_times_20).std()
mean_res_time_pls4_20 = np.array(pls4_solve_times_20).mean()
std_res_time_pls4_20 = np.array(pls4_solve_times_20).std()
print(mean_res_time_pls1_20, mean_res_time_pls2_20, mean_res_time_pls3_20, mean_res_time_pls4_20)
### 30 objects ##
mean_res_time_pls1_30 = np.array(pls1_solve_times_30).mean()
std_res_time_pls1_30 = np.array(pls1_solve_times_30).std()
mean_res_time_pls2_30 = np.array(pls2_solve_times_30).mean()
std_res_time_pls2_30 = np.array(pls2_solve_times_30).std()
mean_res_time_pls3_30 = np.array(pls3_solve_times_30).mean()
std_res_time_pls3_30 = np.array(pls3_solve_times_30).std()
mean_res_time_pls4_30 = np.array(pls4_solve_times_30).mean()
std_res_time_pls4_30 = np.array(pls4_solve_times_30).std()
print(mean_res_time_pls1_30, mean_res_time_pls2_30, mean_res_time_pls3_30, mean_res_time_pls4_30)
### 50 objects ##
mean_res_time_pls1_50 = np.array(pls1_solve_times_50).mean()
std_res_time_pls1_50 = np.array(pls1_solve_times_50).std()
mean_res_time_pls2_50 = np.array(pls2_solve_times_50).mean()
std_res_time_pls2_50 = np.array(pls2_solve_times_50).std()
mean_res_time_pls3_50 = np.array(pls3_solve_times_50).mean()
std_res_time_pls3_50 = np.array(pls3_solve_times_50).std()
mean_res_time_pls4_50 = np.array(pls4_solve_times_50).mean()
std_res_time_pls4_50 = np.array(pls4_solve_times_50).std()
print(mean_res_time_pls1_50, mean_res_time_pls2_50, mean_res_time_pls3_50, mean_res_time_pls4_50)


##### POP SIZES #####
### 20 objects
to_plot(pls1_populations_20, "pls1")
to_plot(pls2_populations_20, "pls2")
to_plot(pls3_populations_20, "pls3")
to_plot(pls4_populations_20, "pls4")
plt.xlabel("iteration")
plt.ylabel("pop size")
plt.title("20 possible objects")
plt.legend()
plt.grid()
plt.savefig("results/population_evol_20objects.png")
plt.clf()
### 30 objects
to_plot(pls1_populations_30, "pls1")
to_plot(pls2_populations_30, "pls2")
to_plot(pls3_populations_30, "pls3")
to_plot(pls4_populations_30, "pls4")
plt.xlabel("iteration")
plt.ylabel("pop size")
plt.title("30 possible objects")
plt.legend()
plt.grid()
plt.savefig("results/population_evol_30objects.png")
plt.clf()
### 20 objects
to_plot(pls1_populations_50, "pls1")
to_plot(pls2_populations_50, "pls2")
to_plot(pls3_populations_50, "pls3")
to_plot(pls4_populations_50, "pls4")
plt.xlabel("iteration")
plt.ylabel("pop size")
plt.title("50 possible objects")
plt.legend()
plt.grid()
plt.savefig("results/population_evol_50objects.png")
plt.clf()
