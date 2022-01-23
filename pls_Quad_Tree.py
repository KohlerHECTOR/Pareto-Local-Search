import numpy as np
from utils_multiobj import dominates, strictly_dominates
from bisect import bisect_left
from Quad_Tree import Quad_Tree, Node_

class PLS_QT():
    """
    The Pareto Local Search class for the PLS algorithm in the context of multi-objs knapsack problem.
    """
    def __init__(self, nb_crit, f_voisinage, init_pop, instance, iter_max = 10):
        """
        Function to initialise the PLS class.

        ARGS

        f_voisinage : a function to generate the neighborhood of workable solution.

        init_pop : a nb_crit-D array of workable solutions.
        """
        # INSTANCE OF MULTI-OBJS KNAPSACK
        self.objects = instance["objects"]
        self.max_weight = instance["max_weight"]
        self.weights = self.objects["weights"]

        self.nb_crit = nb_crit
        self.values_crit = np.array([self.objects["values_crit_"+str(i+1)] for i in range(self.nb_crit)])

        self.iter_max = iter_max # stopping criterion

        self.size_of_a_sol = len(init_pop[0])

        self.Xe = Quad_Tree(nb_crit, self.values_crit) # approximation of efficient solutions
        self.Xe.setRoot(init_pop[0], self.values_crit)	# root of Xe tree : init_pop
        self.P = Quad_Tree(nb_crit, self.values_crit) # current population of solutions
        self.P.setRoot(init_pop[0], self.values_crit)	# root of P tree : init_pop
        self.Pa = Quad_Tree(nb_crit, self.values_crit) # auxiliary population of solutions
        self.N = f_voisinage # neighborhood function


    def get_sol_objective_values(self, sol):
        return np.array([sol @ self.values_crit[i] for i in range(len(self.values_crit))])

    def algorithm1(self):
        """
        The main algorithmic loop of the PLS alogirthm. It is building
        iteratively the population P of approximated solutions.
        """
        iter = 0

        while len(self.P.getNodes()) > 0 and iter < self.iter_max:
            # Generate all neighbors p' of each solution in the current population.
            for p in self.P.getNodes():

                # Get the objective values of sol p
                p_values = p.getCriteria()

                # Get neighbors of sol p
                neighbors = self.N(p_values, self.weights, self.max_weight)

                for p_prime in neighbors:
                    p_prime_values = self.get_sol_objective_values(p_prime)

                    add = self.P.insertNode(p_prime, self.values_crit)

            # P is made of newly found potentially efficient solutions.
            #self.P = self.P.copy_(self.Pa)
            print("Updated current population !")
            print("population is of size: " , len(self.P.getNodes()))

            # Reinit of auxiliary pop.
            #self.Pa = Quad_Tree(self.nb_crit, self.values_crit)

            iter += 1
