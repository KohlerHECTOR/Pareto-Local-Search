import numpy as np
from random import random
from itertools import combinations
import math

def voisinage(solution, list_weights, max_weight):
    """
    Function to generate the neighborhood of a workable solution.
    ARGS
    solution : binary encoding of a workable solution (array of 0s and 1s
    of len total number of possible objects)
    list_weights : an array weights (one weight per possible object).
    max_weight : an integer for the weight available in the bag.
    RETURNS
    neighbors : an array of binary encodings.
    Each one corresponding to a workable solution in the neighborhood of the input solution .
    """
    # indexes of objects in/not in the bag
    idx_objects_in = np.where(solution == 1)[0]
    idx_objects_not_in = np.where(solution == 0)[0]

    neighbors = np.empty((0, len(solution)), int)

    tmp_sol = solution.copy()

    # Iterate over all possible 1-1 exchanges
    for i in idx_objects_in:
        for j in idx_objects_not_in:
            # 1-1 exchange
            tmp_sol[i] = 0
            tmp_sol[j] = 1

           #print("A : ", tmp_sol, "  ", list_weights)
            #print(tmp_sol @ list_weights, " ", max_weight)

            # check if the generated sol is workable
            if tmp_sol @ list_weights <= max_weight:

                # fill the bag as much as possible
                free_weight =  max_weight - tmp_sol @ list_weights
                objects_that_could_fit = np.where(list_weights <= free_weight)[0]

                while free_weight > 0 and len(objects_that_could_fit) > 0:
                    object_to_add = np.random.choice(objects_that_could_fit)
                    tmp_sol[object_to_add] = 1
                    free_weight -= list_weights[object_to_add]
                    objects_that_could_fit = np.where(list_weights <= free_weight)[0]

                if tmp_sol.tolist() not in neighbors.tolist():
                    neighbors = np.concatenate((neighbors, tmp_sol.reshape(1, len(solution))), axis = 0)
                # neighbors = np.concatenate((neighbors, tmp_sol.reshape(1, len(solution))), axis = 0)

            tmp_sol = solution.copy()


    return neighbors

def init_population(objects, max_weight):
	"""
	Function to build an initial population for the Pareto Local Search algo.

	ARGS

	objects : dictionary of objects with a key for the list of weights and a key
	for each criteria to optimize.

	max_weight : an integer for the weight available in the bag.

	RETURNS

	sol : binary encoding of a workable solution (array of 0s and 1s of len total number of possible objects)

	"""
	list_weights = objects["weights"]

	nb_objects = len(list_weights)
	# Construction d'une solution realisable
	# Init d'un solution realisable
	sol=np.zeros(nb_objects)
	tmp_sol = np.arange(nb_objects)

	min_weight = np.min(list_weights)

	# While there is space in the bag and there exists an object light enough to fit
	while((sol @ list_weights < max_weight) and (max_weight - sol @ list_weights >= min_weight)):
		rand_object = np.random.choice(tmp_sol) # choose an object at random

		# if that object is light enough to fit
		if (sol @ list_weights + list_weights[rand_object] <= max_weight):
			sol[rand_object] = 1 # add the object to the bag
			tmp_sol = np.delete(tmp_sol, np.where(tmp_sol == rand_object)) # remove that object from the available objects
			min_weight = np.min(list_weights[tmp_sol]) # update the lightest object available

	assert sol @ list_weights <= max_weight , "Initial solution is not workable (too heavy)."

	return np.array([sol])  #codage binaire du contenu du sac

def read_instance(file_, nb_items = None, nb_crit = 3):
	"""
	Function to read a multi-objs knapsack problem instance
	"""
	f_dat = open(file_+".dat", "r")
	lines = f_dat.readlines()
	liste_w = []
	liste_crit = []
	poids_total = 0

	for line in lines:
		tmp = line.split()
		if tmp[0:2] == ['c',  'w']:

		   liste_crit = [[] for i in range(2, 2 + nb_crit)]

		if tmp[0] == "i":
			liste_w.append(int(tmp[1]))
			for i in range(len(liste_crit)):
				liste_crit[i].append(int(tmp[i+2]))

		elif tmp[0] == "W":
			poids_total = tmp[1]

	liste_crit = np.array(liste_crit)

	if nb_items == None:
		nb_items = len(liste_w)


	objects = {"weights": np.array(liste_w[:nb_items])}
	for i in range(len(liste_crit)):
		objects["values_crit_"+str(i+1)] = np.array(liste_crit[i][:nb_items])

	instance = {"objects": objects, "max_weight": int(math.floor(sum(liste_w[:nb_items])/2))}

	return instance

def dominates(p_values, p_prime_values):
	"""
	Function to check if vector p dominates (pareto) p' in maximisation
		p_values >= p_prime_values and p_values != p_prime_values
	"""
	assert np.size(p_values) == np.size(p_prime_values), "OUPS, p and p' not same number of criteria"
	return (np.all(p_values >= p_prime_values)==True) and (np.all(p_values == p_prime_values)==False)

def strictly_dominates(p_values, p_prime_values):
	"""
	Function to check if vector p strictly dominates (pareto) p' in maximisation
	"""
	assert np.size(p_values) == np.size(p_prime_values), "OUPS, p and p' not same number of criteria"

	return np.all(p_values > p_prime_values)==True

def ideal_nadir(pareto_front):
	ideal = [max(pareto_front[:, i]) for i in range(pareto_front.shape[1])]
	nadir = [min(pareto_front[:, i]) for i in range(pareto_front.shape[1])]
	return [ideal, nadir]
