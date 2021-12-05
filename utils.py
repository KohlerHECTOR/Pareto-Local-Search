import numpy as np

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
    while((sol @ list_weights < max_weight) and (max_weight - sol @ list_weights > min_weight)):
        rand_object = np.random.choice(tmp_sol) # choose an object at random

        # if that object is light enough to fit
        if (sol @ list_weights + list_weights[rand_object] <= max_weight):
            sol[rand_object] = 1 # add the object to the bag
            tmp_sol = np.delete(tmp_sol, np.where(tmp_sol == rand_object)) # remove that object from the available objects
            min_weight = np.min(list_weights[tmp_sol]) # update the lightest object available

    assert sol @ list_weights <= max_weight , "Initial solution is not workable (too heavy)."

    return np.array([sol])  #codage binaire du contenu du sac

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

                if tmp_sol not in neighbors:
                    neighbors = np.concatenate((neighbors, tmp_sol.reshape(1, len(solution))), axis = 0)

            tmp_sol = solution.copy()
    return neighbors


def read_instance(file_):
    f_dat = open(file_+".dat", "r")
    lines = f_dat.readlines()
    liste_w = []
    liste_v1 = []
    liste_v2 = []
    poids_total = 0
    for line in lines:
        tmp = line.split()
        if tmp[0] == "i":
            liste_w.append(int(tmp[1]))
            liste_v1.append(int(tmp[2]))
            liste_v2.append(int(tmp[3]))
        elif tmp[0] == "W":
            poids_total = tmp[1]

    f_eff = open(file_+".eff","r")
    lines_eff = f_eff.readlines()
    liste_pareto=[]
    for line in lines_eff:
        temp=line.split()
        liste_pareto.append([int(temp[0]), int(temp[1])])

    objects = {"weights": np.array(liste_w), "values_crit_1": np.array(liste_v1),
                "values_crit_2": np.array(liste_v2)}
    instance = {"objects": objects, "max_weight": int(poids_total),
                "sols_pareto": np.array(liste_pareto)}

    return instance

def dominates(p_values, p_prime_values):
    p_values_crit_1 = p_values[0]
    p_values_crit_2 = p_values[1]

    p_prime_values_crit_1 = p_prime_values[0]
    p_prime_values_crit_2 = p_prime_values[1]

    condition1 = p_values_crit_1 > p_prime_values_crit_1 and p_values_crit_2 >= p_prime_values_crit_2
    condition2 = p_values_crit_1 >= p_prime_values_crit_1 and p_values_crit_2 > p_prime_values_crit_2

    if condition1 or condition2 :
        return True
    else:
        return False

def strictly_dominates(p_values, p_prime_values):
    p_values_crit_1 = p_values[0]
    p_values_crit_2 = p_values[1]

    p_prime_values_crit_1 = p_prime_values[0]
    p_prime_values_crit_2 = p_prime_values[1]

    if (p_values_crit_1 > p_prime_values_crit_1 and p_values_crit_2 > p_prime_values_crit_2):
        return True
    else:
        return False
