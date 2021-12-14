import numpy as np
from utils import dominates, strictly_dominates
from bisect import bisect_left

class PLS():
    """
    The Pareto Lcoal Search class for the PLS algorithm in the context of bi-objs knapsack problem.
    """
    def __init__(self, f_voisinage, init_pop, instance, iter_max = 10):
        """
        Function to initialise the PLS class.

        ARGS

        f_voisinage : a function to generate the neighborhood of workable solution.

        init_pop : a 2-D array of workable solutions.
        """
        self.size_of_a_sol = len(init_pop[0])
        self.Xe = init_pop # approximation of efficient solutions
        self.P = init_pop # current population of solutions
        self.Pa = np.empty((0, self.size_of_a_sol), int) # auxiliary population of solutions
        self.N = f_voisinage # neighborhood function

        # INSTANCE OF BI-OBJS KNAPSACK
        self.objects = instance["objects"]
        self.max_weight = instance["max_weight"]
        self.weights = self.objects["weights"]
        self.values_crit_1 = self.objects["values_crit_1"]
        self.values_crit_2 = self.objects["values_crit_2"]

        self.iter_max = iter_max # stopping criterion

    def get_sol_objective_values(self, sol):
        values_obj_1 = sol @ self.values_crit_1
        values_obj_2 = sol @ self.values_crit_2
        return np.array([values_obj_1, values_obj_2])


    def algorithm1(self):
        """
        The main algorithmic loop of the PLS alogirthm. It is building
        iteratively the population P of approximated solutions.
        """
        iter = 0
        while len(self.P) > 0 and iter < self.iter_max:
            # Generate all neighbors p' of each solution in the current population.
            for p in self.P:
                # Get the objective values of sol p
                p_values = self.get_sol_objective_values(p)
                # Get neighbors of sol p
                neighbors = self.N(p, self.weights, self.max_weight)
                for p_prime in neighbors:
                    p_prime_values = self.get_sol_objective_values(p_prime)
                    # If p' is non-dominated by p:
                    if not dominates(p_values, p_prime_values):
                        # We check if p' is part of the current efficient sols
                        add, self.Xe = self.updates(self.Xe, p_prime)

                        if add:

                            if len(self.Pa) == 0:
                                self.Pa = p_prime.reshape(1, self.size_of_a_sol)

                            else:
                                _, self.Pa = self.updates(self.Pa, p_prime)

            # P is made of newly found potentially efficient solutions.
            self.P = self.Pa.copy()
            print("Updated current population !")
            print("population is of size: " , self.P.shape)
            # Reinit of auxiliary pop.
            self.Pa = np.empty((0, self.size_of_a_sol), int)

            iter += 1


    def updates(self, array_of_sols, p_prime):
        """
        Function to update a set of objective values with respect to pareto dominance.

        ARGS

        array_of_sols : array of arrays, an archive to be tested against a new
        potentially non-dominated sol.
        p_prime : array, a solution to be tested as an efficient solution.

        RETURNS

        add : bool, whether or not the solution p_prime was added to the set of efficient solutions.
        array_of_sols : array of arrays, the updated archive.

        """

        add = True

        # get objective values of the solution to be tested
        p_prime_values = self.get_sol_objective_values(p_prime)

        for sol in array_of_sols:
            sol_values = self.get_sol_objective_values(sol)
            # If there is an efficient solution dominating p', we dont add p_prime.
            if dominates(sol_values, p_prime_values):
                add = False
                break

        # If we want to add p' to the set of efficient sols, we have to delete the solutions
        # dominated by p' in the set of efficient sols.
        if add:
            idx_to_delete = []

            for i , sol in enumerate(array_of_sols):
                sol_values = self.get_sol_objective_values(sol)
                # We delete all the solutions strictly dominated by p'.
                if strictly_dominates(p_prime_values, sol_values):
                    idx_to_delete.append(i)

            # Update of set of approximated efficient sols (delete dominated sols, add p')
            array_of_sols = np.delete(array_of_sols, idx_to_delete, axis = 0)
            array_of_sols = np.concatenate((array_of_sols, p_prime.reshape(1, self.size_of_a_sol)), axis = 0)

        return add, array_of_sols


class PLS2(PLS):
    def  __init__(self, f_voisinage, init_pop, instance, iter_max = 10):
        super().__init__(f_voisinage, init_pop, instance, iter_max)

    def updates(self, array_of_sols, p_prime):
        """
        Function to update the set of approximated efficient solutions. But we sort
        the set with respect to the values of the first objective.

        ARGS

        array_of_sols : array of arrays, an archive to be tested against a new
        potentially non-dominated sol.
        p_prime : array, a solution to be tested as an efficient solution.

        RETURNS

        add : bool, whether or not the solution p_prime was added to the set of efficient solutions.
        array_of_sols : array of arrays, the updated archive.
        """
        add = False
        p_prime_values = self.get_sol_objective_values(p_prime) # objective vals of p'

        # make a list of all the values of the objective of the sols in the archive and the tested sol
        all_values = [self.get_sol_objective_values(sol) for sol in array_of_sols]
        all_values = np.array(all_values)

        # argsort descending order with respect to first objective
        rank_of_p_prime_in_sorted_sols = bisect_left(-1 * all_values[:,0], -1 * p_prime_values[0])

        if rank_of_p_prime_in_sorted_sols == 0:
            add = True
        else:
            for sorted_val in np.flip(all_values[:rank_of_p_prime_in_sorted_sols], axis = 0):
                # If there is an efficient solution dominating p', we dont add p_prime.
                if dominates(sorted_val, p_prime_values):
                    add = False
                    break

        # If we want to add p' to the set of efficient sols, we have to delete the solutions
        # dominated by p' in the set of efficient sols.
        if add:
            to_delete = []
            for i , sorted_val in enumerate(all_values[rank_of_p_prime_in_sorted_sols: ]):
                if dominates(p_prime_values, sorted_val):
                    to_delete.append(i)

            # Update of set of approximated efficient sols (delete dominated sols, add p')
            tmp = np.delete(array_of_sols[rank_of_p_prime_in_sorted_sols: ], to_delete, axis = 0)

            array_of_sols = np.concatenate((array_of_sols[:rank_of_p_prime_in_sorted_sols], p_prime.reshape(1,self.size_of_a_sol)), axis = 0)
            array_of_sols = np.concatenate((array_of_sols , tmp), axis = 0)
            
        return add, array_of_sols
