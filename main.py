from utils import read_instance, init_population, voisinage, init_population_S_weighted
from indicateurs import indicateur_P
import matplotlib.pyplot as plt
import numpy as np
from pls import PLS, PLS2

instance = read_instance("data/100_items/2KP100-TA-0")

initial_pop = init_population(instance["objects"], instance["max_weight"])
initial_pop_S = init_population_S_weighted(instance["objects"], instance["max_weight"], S = 10)

pls1 = PLS(voisinage, initial_pop, instance)
pls2 = PLS2(voisinage, initial_pop, instance)
pls3 = PLS2(voisinage, initial_pop_S, instance)
