from utils import read_instance, init_population, voisinage, init_population_S_weighted, voisinage_L
from indicateurs import indicateur_P
import matplotlib.pyplot as plt
import numpy as np
from pls import PLS, PLS2, PLS4
import time

instance = read_instance("data/100_items/2KP100-TA-0")

initial_pop = init_population(instance["objects"], instance["max_weight"])

initial_pop_S = init_population_S_weighted(instance["objects"], instance["max_weight"], S = 5)
pls1 = PLS(voisinage, initial_pop, instance, iter_max = 5)
pls2 = PLS2(voisinage, initial_pop, instance, iter_max = 5)
pls3 = PLS2(voisinage, initial_pop_S, instance, iter_max = 5)
pls4 = PLS4(voisinage_L, initial_pop_S, instance, iter_max = 5)
timea = time.time()
print("------------------- PLS 1 --------------------")
pls1.algorithm1()
timePLS1 = time.time() - timea

timea = time.time()
print("------------------- PLS 2 --------------------")
pls2.algorithm1()
timePLS2 = time.time() - timea

timea = time.time()
print("------------------- PLS 3 --------------------")
pls3.algorithm1()
timePLS3 = time.time() - timea

timea = time.time()
print("------------------- PLS 4 --------------------")
pls4.algorithm1(L = 5)
timePLS4 = time.time() - timea

sol_eff_pls1 = pls1.Xe
res_pls1 = np.array([pls1.get_sol_objective_values(s) for s in sol_eff_pls1])
sol_eff_pls2 = pls2.Xe
res_pls2 = np.array([pls2.get_sol_objective_values(s) for s in sol_eff_pls2])
sol_eff_pls3 = pls3.Xe
res_pls3 = np.array([pls3.get_sol_objective_values(s) for s in sol_eff_pls3])
sol_eff_pls4 = pls4.Xe
res_pls4 = np.array([pls4.get_sol_objective_values(s) for s in sol_eff_pls4])


print("------------  TIMES  -------------------")
print("pls1 : " + str(timePLS1))
print("pls2 : " + str(timePLS2))
print("pls3 : " + str(timePLS3))
print("pls4 : " + str(timePLS4))

plt.scatter(instance["sols_pareto"][:,0], instance["sols_pareto"][:,1], label = "Pareto Exact")
plt.scatter(res_pls1[:,0], res_pls1[:,1], label = "PLS1")
plt.scatter(res_pls2[:,0], res_pls2[:,1], label = "PLS2")
plt.scatter(res_pls3[:,0], res_pls3[:,1], label = "PLS3")
plt.scatter(res_pls4[:,0], res_pls4[:,1], label = "PLS4")
plt.legend()
plt.savefig("comparison_pareto_fronts")
