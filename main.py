from utils import read_instance, init_population, voisinage
from indicateurs import indicateur_P
import matplotlib.pyplot as plt
import numpy as np
from pls import PLS, PLS2

instance = read_instance("data/100_items/2KP100-TA-0")
pareto = instance["sols_pareto"]
initial_pop = init_population(instance["objects"], instance["max_weight"])


# pls = PLS(voisinage, initial_pop, instance)
pls = PLS(voisinage, initial_pop, instance)
pls.algorithm1()
print("RESULT")
print(pls.Xe)
# plt.scatter(pareto[:,0], pareto[:,1])
#plt.savefig("2KP100-TA-0_pareto.png")
# plt.show()
