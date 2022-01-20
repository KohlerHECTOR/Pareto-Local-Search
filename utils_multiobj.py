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

def R(weight, q, liste_v):
    """
    Function to compute the R indicator of an object
    """
    res = q * liste_v[0]
    nb_crit = np.size(liste_v)
    for i in range(1,nb_crit):
        res = res + (1-q)/(nb_crit-1)*liste_v[i]
    return res / weight

def init_population_S_weighted(nb_crit, objects, max_weight, S):
    """
    Function to generate a good quality intial population in terms of R indicators for each objects
    """
    list_weights = objects["weights"]
    list_values_crit = [objects["values_crit_"+str(i+1)] for i in range(nb_crit)]

    nb_objects = len(list_weights)
    idx_available_objects = np.arange(nb_objects)

    init_pop = []
    min_weight = np.min(list_weights[idx_available_objects])

    while len(init_pop) < S:
        q = random()

        list_R = np.array([R(list_weights[i], q, np.array([c[i] for c in list_values_crit])) for i in idx_available_objects])
        best_R = np.argsort(-1 * list_R)
        sorted_objects_by_R = idx_available_objects[best_R].copy()# objects sorted by best R
        i = 0
        sol = np.zeros(nb_objects)

        while((sol @ list_weights < max_weight) and (max_weight - sol @ list_weights >= min_weight)):
            object_to_test = sorted_objects_by_R[i]

            if (sol @ list_weights + list_weights[object_to_test] <= max_weight):
                sol[object_to_test] = 1
                idx_available_objects = np.delete(idx_available_objects, np.where(idx_available_objects == object_to_test), axis = 0)
                min_weight = np.min(list_weights[idx_available_objects])
            i += 1

        idx_available_objects = np.arange(nb_objects)

        init_pop.append(sol)

    init_pop = np.array(init_pop).reshape(S, len(sol))
    return init_pop


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
    print(solution)
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

def voisinage_L(solution, list_weights, max_weight, list_values, nb_crit, L = 5, solve = "enum"):

    q = random()
    # indexes of objects in/not in the bag
    idx_objects_in = np.where(solution == 1)[0]
    idx_objects_not_in = np.where(solution == 0)[0]

    neighbors = np.empty((0, len(solution)), int)

    tmp_sol = solution.copy()

    list_R = np.array([R(list_weights[i], q, np.array([c[i] for c in list_values])) for i in idx_objects_in])
    worst_R = np.argsort(list_R)
    L1 = worst_R[:L]

    list_R = np.array([R(list_weights[i], q, np.array([c[i] for c in list_values])) for i in idx_objects_not_in])
    best_R = np.argsort(-1 * list_R)
    L2 = best_R[:L]

    # New instance of Knapsack problem
    new_KP_objects = np.concatenate((L1, L2))

    # weight_objects_not_in_L1 = 0
    #
    # for i in range(len(list_weights)):
    #     if i not in L1:
    #         weight_objects_not_in_L1 += list_weights[i]



    new_KP_max_weight = max_weight - np.sum(list_weights[L2]) #weight_objects_not_in_L1

    new_KP = [list_values[i] for i in range(nb_crit)]
    new_KP_nb_objs = len(new_KP_objects)


    if solve == "enum": #for L < 5
        init_sol = np.zeros(new_KP_nb_objs)
        pareto = [[0, 0]]
        sols = np.array([init_sol])
        for i in range(L):
            combs = combinations(new_KP_objects, i + 1)

            for comb in combs:
                comb = list(comb)
                comb_sol = np.zeros(new_KP_nb_objs)

                for o in comb:
                    id = np.where(new_KP_objects == o)
                    comb_sol[id] = 1
                if np.sum(list_weights[comb]) <= new_KP_max_weight:
                    vals_comb = np.array([np.sum(list_values[i][comb]) for i in range(nb_crit)])
                    add = True
                    for s in pareto:
                        if dominates(np.array(s), vals_comb):
                            add = False
                            break
                    if add:
                        to_delete = []
                        for i, s in enumerate(pareto):
                            if dominates(vals_comb, s):
                                pareto.remove(s)
                                to_delete.append(i)
                        sols = np.delete(sols, to_delete, axis = 0)
                        sols = np.concatenate((sols, comb_sol.reshape(1, new_KP_nb_objs)), axis = 0)

    for sol in sols:
        tmp = np.concatenate((sol, solution[2 * L:]))
        neighbors = np.concatenate((neighbors, tmp.reshape(1, len(solution))), axis = 0)

    return neighbors

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
