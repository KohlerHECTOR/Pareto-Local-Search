import numpy as np
import matplotlib.pyplot as plt

NB_SIMUS = 20
NB_CRIT =[3 ,4]

def to_plot(data, label = None, iter_max = 20):
	for row in data:
		if len(row)< iter_max:
			row += [0 for _ in range(iter_max - len(row))]
	mean_data = np.mean(data, axis = 0)
	std_data = np.std(data, axis = 0)
	plt.plot(mean_data, label = label)
	plt.fill_between(np.arange(len(mean_data)), mean_data + std_data, mean_data - std_data, alpha = 0.2)

for NB_CRIT in [3 ,4]:
	## MMR per query
	results_all_simus_mmrq_elicit_owa = []
	results_all_simus_mmrq_elicit_ws = []
	results_all_simus_mmrq_rbls_owa = []
	results_all_simus_mmrq_rbls_ws = []
	max_nb_queries = 0


	for i in range(NB_SIMUS):

		elicit_owa = np.load("elicit_owa_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
		results_all_simus_mmrq_elicit_owa.append(elicit_owa.tolist())
		if len(elicit_owa) > max_nb_queries:
			max_nb_queries = len(elicit_owa)

		elicit_ws = np.load("elicit_ws_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
		results_all_simus_mmrq_elicit_ws.append(elicit_ws.tolist())
		if len(elicit_ws) > max_nb_queries:
			max_nb_queries = len(elicit_ws)

		rbls_owa = np.load("rbls_owa_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
		results_all_simus_mmrq_rbls_owa.append(rbls_owa.tolist())
		if len(rbls_owa) > max_nb_queries:
			max_nb_queries = len(rbls_owa)

		rbls_ws = np.load("rbls_ws_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
		results_all_simus_mmrq_rbls_ws.append(rbls_ws.tolist())
		if len(rbls_ws) > max_nb_queries:
			max_nb_queries = len(rbls_ws)





	to_plot(results_all_simus_mmrq_elicit_owa, label = "INCR_ELIC + OWA", iter_max = max_nb_queries)
	to_plot(results_all_simus_mmrq_elicit_ws, label = "INCR_ELIC + WS", iter_max = max_nb_queries)
	to_plot(results_all_simus_mmrq_rbls_owa, label = "RBLS + OWA", iter_max = max_nb_queries)
	to_plot(results_all_simus_mmrq_rbls_ws, label = "RBLS + WS", iter_max = max_nb_queries)
	plt.xlabel("number of queries")
	plt.ylabel("MMR")
	plt.title("20 possible objects, "+str(NB_CRIT)+" criteria")
	plt.legend()
	plt.grid()
	plt.savefig("comparison_20objects"+str(NB_CRIT)+"criteria.png")
	plt.clf()


NB_CRIT = 5
for i in range(4):
	elicit_owa = np.load("elicit_owa_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
	results_all_simus_mmrq_elicit_owa.append(elicit_owa.tolist())
	if len(elicit_owa) > max_nb_queries:
		max_nb_queries = len(elicit_owa)

	elicit_ws = np.load("elicit_ws_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
	results_all_simus_mmrq_elicit_ws.append(elicit_ws.tolist())
	if len(elicit_ws) > max_nb_queries:
		max_nb_queries = len(elicit_ws)

	rbls_owa = np.load("rbls_owa_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
	results_all_simus_mmrq_rbls_owa.append(rbls_owa.tolist())
	if len(rbls_owa) > max_nb_queries:
		max_nb_queries = len(rbls_owa)

	rbls_ws = np.load("rbls_ws_" + str(i) + "_crits_" + str(NB_CRIT) + ".npy", allow_pickle = True)
	results_all_simus_mmrq_rbls_ws.append(rbls_ws.tolist())
	if len(rbls_ws) > max_nb_queries:
		max_nb_queries = len(rbls_ws)


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
plt.xlabel("number of queries")
plt.ylabel("MMR")
plt.title("20 possible objects, "+str(NB_CRIT)+" criteria")
plt.legend()
plt.grid()
plt.savefig("comparison_20objects"+str(NB_CRIT)+"criteria.png")
plt.clf()
