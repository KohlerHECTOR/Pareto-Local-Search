#from utils import read_instance, init_population_S_weighted, voisinage_L
#from pls import PLS4
#from utils_multiobj import read_instance, init_population_S_weighted, voisinage_L
#from pls_multiobj import PLS4
import utils_multiobj
import pls_multiobj
import time
import utils
import pls

instance = utils_multiobj.read_instance("data/100_items/2KP100-TA-0")

initial_pop_S = utils_multiobj.init_population_S_weighted(2, instance["objects"], instance["max_weight"], S = 5)

pls3 = pls_multiobj.PLS2(2, utils_multiobj.voisinage, initial_pop_S, instance, iter_max = 5)

timea = time.time()
print("------------------- pls 3 --------------------")
pls3.algorithm1()
timepls3 = time.time() - timea

print("------------  TIMES  -------------------")
print("pls3 : " + str(timepls3))

"""

instance = utils.read_instance("data/100_items/2KP100-TA-0")

initial_pop_S = utils.init_population_S_weighted(instance["objects"], instance["max_weight"], S = 5)

pls3 = pls.PLS2(utils.voisinage, initial_pop_S, instance, iter_max = 5)

timea = time.time()
print("------------------- pls 3 --------------------")
pls3.algorithm1()
timepls3 = time.time() - timea

print("------------  TIMES  -------------------")
print("pls3 : " + str(timepls3))
"""
