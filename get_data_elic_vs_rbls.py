import numpy as np
from rbls import RBLS
from elicitation import ELICIT, get_DM
from utils_multi_objs import  get_pareto_fronts_from_data, voisinage, init_greedy, read_instance
import time
import matplotlib.pyplot as plt
nb_crit = []
# X = get_pareto_fronts_from_data("data_multi_objs/200_items/_nb_crit_3_nb_objects_20_0_pls1_current_pareto_results.txt")[-1]
NB_SIMUS = 20
FILENAME = "data_multi_objs/200_items/2KP200-TA-0"
# NB_CRIT = 3

for NB_CRIT in [3,4,5]:
	X = get_pareto_fronts_from_data("data_multi_objs/200_items/_nb_crit_"+str(NB_CRIT)+"_nb_objects_20_0_pls1_current_pareto_results.txt")[-1]
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
		DM = get_DM(NB_CRIT)

		elicit_owa =  ELICIT( X, DM, agreg = "OWA", nb_crit = NB_CRIT)
		elicit_ws = ELICIT(X, DM, agreg = "WS", nb_crit = NB_CRIT)


		instance = read_instance(FILENAME, nb_items = 20, nb_crit = NB_CRIT)
		initial_pop = init_greedy(instance["objects"], instance["max_weight"])

		rbls_owa  = RBLS(nb_crit = NB_CRIT, f_voisinage = voisinage, init_pop = initial_pop, instance = instance, DM = DM, iter_max = 100, agreg = "OWA")
		rbls_ws  = RBLS(nb_crit = NB_CRIT, f_voisinage = voisinage, init_pop = initial_pop, instance = instance, DM = DM, iter_max = 100, agreg = "WS")

		print("elicit_owa")
		timea = time.time()
		elicit_owa.algorithm1()
		results_all_simus_times_elicit_owa.append(time.time() - timea)
		mmrq = elicit_owa.mmr_per_query
		np.save("save/elicit_owa_" + str(i) + "_crits_" + str(NB_CRIT), mmrq, allow_pickle = True)
		if len(mmrq) > max_nb_queries:
			max_nb_queries = len(mmrq)
		results_all_simus_mmrq_elicit_owa.append(mmrq)

		print("elicit_ws")
		timea = time.time()
		elicit_ws.algorithm1()
		results_all_simus_times_elicit_ws.append(time.time() - timea)
		mmrq = elicit_ws.mmr_per_query
		np.save("save/elicit_ws_" + str(i)+ "_crits_" + str(NB_CRIT), mmrq, allow_pickle = True)
		if len(mmrq) > max_nb_queries:
			max_nb_queries = len(mmrq)
		results_all_simus_mmrq_elicit_ws.append(mmrq)

		print("rbls_owa")
		timea = time.time()
		rbls_owa.algorithm1()
		results_all_simus_times_rbls_owa.append(time.time() - timea)
		mmrq = rbls_owa.mmr_per_query
		np.save("save/rbls_owa_" + str(i)+ "_crits_" + str(NB_CRIT), mmrq, allow_pickle = True)
		if len(mmrq) > max_nb_queries:
			max_nb_queries = len(mmrq)
		results_all_simus_mmrq_rbls_owa.append(mmrq)

		print("rbls_ws")
		timea = time.time()
		rbls_ws.algorithm1()
		results_all_simus_times_rbls_ws.append(time.time() - timea)
		mmrq = rbls_ws.mmr_per_query
		np.save("save/rbls_ws_" + str(i)+ "_crits_" + str(NB_CRIT), mmrq, allow_pickle = True)
		if len(mmrq) > max_nb_queries:
			max_nb_queries = len(mmrq)
		results_all_simus_mmrq_rbls_ws.append(mmrq)


	print("average time elicit owa ", np.mean(results_all_simus_times_elicit_owa), np.std(results_all_simus_times_elicit_owa))
	print("average time elicit ws ", np.mean(results_all_simus_times_elicit_ws), np.std(results_all_simus_times_elicit_ws))
	print("average time rbls owa ", np.mean(results_all_simus_times_rbls_owa), np.std(results_all_simus_times_rbls_owa))
	print("average time rbls ws ", np.mean(results_all_simus_times_rbls_ws), np.std(results_all_simus_times_rbls_ws))
