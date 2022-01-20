import numpy as np
from random import random
from itertools import combinations

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

def read_instance(file_):
    """
    Function to read a multi-objs knapsack problem instance
    """
    f_dat = open(file_+".dat", "r")
    lines = f_dat.readlines()
    liste_w = []
    liste_crit = []
    nb_crit = 0
    poids_total = 0

    for line in lines:
        tmp = line.split()
        if tmp[0:2] == ['c',  'w']:
           liste_crit = [[] for i in range(2,len(tmp))]

        if tmp[0] == "i":
            liste_w.append(int(tmp[1]))
            for i in range(len(liste_crit)):
                liste_crit[i].append(int(tmp[i+2]))

        elif tmp[0] == "W":
            poids_total = tmp[1]

    liste_crit = np.array(liste_crit)
    f_eff = open(file_+".eff","r")
    lines_eff = f_eff.readlines()
    liste_pareto=[]
    for line in lines_eff:
        temp=line.split()
        liste_pareto.append([int(temp[0]), int(temp[1])])

    objects = {"weights": np.array(liste_w)}
    for i in range(len(liste_crit)):
        objects["values_crit_"+str(i+1)] = np.array(liste_crit[i])

    instance = {"objects": objects, "max_weight": int(poids_total),
                "sols_pareto": np.array(liste_pareto)}

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
