import numpy as np
from rbls import RBLS
from elicitation import ELICIT, get_DM
from utils_multi_objs import  get_pareto_fronts_from_data, voisinage, init_greedy, read_instance
import time
import matplotlib.pyplot as plt

X = get_pareto_fronts_from_data("data_multi_objs/200_items/_nb_crit_3_nb_objects_20_0_pls1_current_pareto_results.txt")[-1]
NB_SIMUS = 20
FILENAME = "data_multi_objs/200_items/2KP200-TA-0"


## TIMES
results_all_simus_times_elicit_owa = []
results_all_simus_times_elicit_ws = []
results_all_simus_times_rbls_owa = []
results_all_simus_times_rbls_ws = []

## MMR per query
results_all_simus_mmrq_elicit_owa = []
results_all_simus_mmrq_elicit_ws = []
results_all_simus_mmrq_rbls_owa = []
results_all_simus_mmrq_rbls_ws = []
max_nb_queries = 0
for i in range(NB_SIMUS):
	DM = get_DM(3)

	elicit_owa =  ELICIT( X, DM, agreg = "OWA")
	elicit_ws = ELICIT(X, DM, agreg = "WS")


	instance = read_instance(FILENAME, nb_items = 30, nb_crit = 3)
	initial_pop = init_greedy(instance["objects"], instance["max_weight"])

	rbls_owa  = RBLS(nb_crit = 3, f_voisinage = voisinage, init_pop = initial_pop, instance = instance, DM = DM, iter_max = 100, agreg = "OWA")
	rbls_ws  = RBLS(nb_crit = 3, f_voisinage = voisinage, init_pop = initial_pop, instance = instance, DM = DM, iter_max = 100, agreg = "WS")

	print("elicit_owa")
	timea = time.time()
	elicit_owa.algorithm1()
	results_all_simus_times_elicit_owa.append(time.time() - timea)
	mmrq = elicit_owa.mmr_per_query
	np.save("save/elicit_owa_" + str(i), mmrq, allow_pickle = True)
	if len(mmrq) > max_nb_queries:
		max_nb_queries = len(mmrq)
	results_all_simus_mmrq_elicit_owa.append(mmrq)

	print("elicit_ws")
	timea = time.time()
	elicit_ws.algorithm1()
	results_all_simus_times_elicit_ws.append(time.time() - timea)
	mmrq = elicit_ws.mmr_per_query
	np.save("save/elicit_ws_" + str(i), mmrq, allow_pickle = True)
	if len(mmrq) > max_nb_queries:
		max_nb_queries = len(mmrq)
	results_all_simus_mmrq_elicit_ws.append(mmrq)

	print("rbls_owa")
	timea = time.time()
	rbls_owa.algorithm1()
	results_all_simus_times_rbls_owa.append(time.time() - timea)
	mmrq = rbls_owa.mmr_per_query
	np.save("save/rbls_owa_" + str(i), mmrq, allow_pickle = True)
	if len(mmrq) > max_nb_queries:
		max_nb_queries = len(mmrq)
	results_all_simus_mmrq_rbls_owa.append(mmrq)

	print("rbls_ws")
	timea = time.time()
	rbls_ws.algorithm1()
	results_all_simus_times_rbls_ws.append(time.time() - timea)
	mmrq = rbls_ws.mmr_per_query
	np.save("save/rbls_ws_" + str(i), mmrq, allow_pickle = True)
	if len(mmrq) > max_nb_queries:
		max_nb_queries = len(mmrq)
	results_all_simus_mmrq_rbls_ws.append(mmrq)


print("average time elicit owa ", np.mean(results_all_simus_times_elicit_owa), np.std(results_all_simus_times_elicit_owa))
print("average time elicit ws ", np.mean(results_all_simus_times_elicit_ws), np.std(results_all_simus_times_elicit_ws))
print("average time rbls owa ", np.mean(results_all_simus_times_rbls_owa), np.std(results_all_simus_times_rbls_owa))
print("average time rbls ws ", np.mean(results_all_simus_times_rbls_ws), np.std(results_all_simus_times_rbls_ws))


def to_plot(data, label = None, iter_max = 20):
    for row in data:
        if len(row)< iter_max:
            row += [0 for _ in range(iter_max - len(row))]
    mean_data = np.mean(data, axis = 0)
    std_data = np.std(data, axis = 0)
    plt.plot(mean_data, label = label)
    plt.fill_between(np.arange(len(mean_data)), mean_data + std_data, mean_data - std_data, alpha = 0.2)


to_plot(results_all_simus_mmrq_elicit_owa, label = "INCR_ELIC + OWA", iter_max = max_nb_queries)
to_plot(results_all_simus_mmrq_elicit_ws, label = "INCR_ELIC + WS", iter_max = max_nb_queries)
to_plot(results_all_simus_mmrq_rbls_owa, label = "RBLS + OWA", iter_max = max_nb_queries)
to_plot(results_all_simus_mmrq_rbls_ws, label = "RBLS + WS", iter_max = max_nb_queries)
plt.xlabel("number of query")
plt.ylabel("MMR")
plt.title("20 possible objects, 3 criteria")
plt.legend()
plt.grid()
plt.savefig("save/comparison_20objects.png")
plt.clf()
