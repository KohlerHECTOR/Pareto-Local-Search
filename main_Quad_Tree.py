from pls_Quad_Tree import PLS_QT
from utils_multiobj import read_instance, init_population

instance = read_instance("data/100_items/2KP100-TA-0", nb_items = 20, nb_crit = 2)

initial_pop = init_population(instance["objects"], instance["max_weight"])

PLS_QT = PLS_QT(2, utils_multiobj.voisinage, initial_pop, instance, iter_max = 5)
PLS_QT.algorithm1()



















































