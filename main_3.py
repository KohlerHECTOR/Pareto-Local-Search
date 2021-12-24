#from utils import read_instance, init_population_S_weighted, voisinage_L
#from pls import PLS4
from utils_multiobj import read_instance, init_population_S_weighted, voisinage_L
from pls_multiobj import PLS4
import time

instance = read_instance("data/100_items/2KP100-TA-0")

initial_pop_S = init_population_S_weighted(instance["objects"], instance["max_weight"], S = 5)

pls4 = PLS4(2, voisinage_L, initial_pop_S, instance, iter_max = 5)

timea = time.time()
print("------------------- PLS 4 --------------------")
pls4.algorithm1(L = 5)
timePLS4 = time.time() - timea

print("------------  TIMES  -------------------")
print("pls4 : " + str(timePLS4))
