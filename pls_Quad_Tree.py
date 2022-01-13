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
        
        #print([n.getCriteria() for n in self.P.getNodes()])
        
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
                #print("B : ", p.getCriteria())
                # Get the objective values of sol p
                #p_values = self.get_sol_objective_values(p)
                p_values = p.getCriteria()
                #print("A ", p_values)
                # Get neighbors of sol p
                neighbors = self.N(p_values, self.weights, self.max_weight)
                #print("neighbors : ", len(neighbors))
                for p_prime in neighbors:
                    p_prime_values = self.get_sol_objective_values(p_prime)
                    
                    """
                    if not dominates(p_values, p_prime_values):
                        # We check if p' is part of the current efficient sols
                        add, self.Xe = self.updates(self.Xe, p_prime)

                        if add:

                            if len(self.Pa) == 0:
                                self.Pa = p_prime.reshape(1, self.size_of_a_sol)

                            else:
                                _, self.Pa = self.updates(self.Pa, p_prime)
                    """
                    print(len(self.P.getNodes()))
                    #add = self.Pa.insertNode(p_prime)
                    #print(self.values_crit)
                    add = self.P.insertNode(p_prime, self.values_crit)
                    #print(len(self.P.getRoot().getSuccessor()))
                    #input("Entree")
                    #print(add)

            #print(self.Pa.getNodes())
            # P is made of newly found potentially efficient solutions.
            #self.P = self.P.copy_(self.Pa)
            print("Updated current population !")
            print("population is of size: " , len(self.P.getNodes()))
            input("Entree")
            #print(self.P.getNodes())
            # Reinit of auxiliary pop.
            #self.Pa = Quad_Tree(self.nb_crit, self.values_crit)

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
        # make a list of all the values of the objective of the sols in the archive and the tested sol
        all_values = [self.get_sol_objective_values(sol) for sol in array_of_sols]
        all_values = np.array(all_values)

        for val in all_values:
            # If there is an efficient solution dominating p', we dont add p_prime.
            if dominates(val, p_prime_values):
                add = False
                break

        # If we want to add p' to the set of efficient sols, we have to delete the solutions
        # dominated by p' in the set of efficient sols.
        if add:
            idx_to_delete = []

            for i , val in enumerate(all_values):
                # We delete all the solutions strictly dominated by p'.
                if dominates(p_prime_values, val):
                    idx_to_delete.append(i)

            # Update of set of approximated efficient sols (delete dominated sols, add p')
            array_of_sols = np.delete(array_of_sols, idx_to_delete, axis = 0)
            array_of_sols = np.concatenate((array_of_sols, p_prime.reshape(1, self.size_of_a_sol)), axis = 0)

        return add, array_of_sols

"""
class PLS2(PLS):
    def  __init__(self, nb_crit, f_voisinage, init_pop, instance, iter_max = 10):
        super().__init__(nb_crit, f_voisinage, init_pop, instance, iter_max)

    def updates(self, array_of_sols, p_prime):
        """"""
        Function to update the set of approximated efficient solutions. But
        the set is  sorted with respect to the values of the first objective.
        It is sorted, because we insert new sols in order.

        ARGS

        array_of_sols : array of arrays, an archive to be tested against a new
        potentially non-dominated sol.
        p_prime : array, a solution to be tested as an efficient solution.

        RETURNS

        add : bool, whether or not the solution p_prime was added to the set of efficient solutions.
        array_of_sols : array of arrays, the updated archive.
        """"""
        add = True
        p_prime_values = self.get_sol_objective_values(p_prime) # objective vals of p'

        # make a list of all the values of the objective of the sols in the archive and the tested sol
        sorted_values = [self.get_sol_objective_values(sol) for sol in array_of_sols]
        sorted_values = np.array(sorted_values) 

        # find the index i such that obj1(sol[0]) >= obj1(sol[i-1])... obj1(sol[i-1]) > obj1(solTested) >= obj1(sol[i]) ...
        rank_of_p_prime_in_sorted_sols = bisect_left(-1 * sorted_values[:,0], -1 * p_prime_values[0])

        for sorted_val in np.flip(sorted_values[:rank_of_p_prime_in_sorted_sols], axis = 0):
            # If there is an efficient solution dominating p', we dont add p_prime.
            if dominates(sorted_val, p_prime_values):
                add = False
                break

        # If we want to add p' to the set of efficient sols, we have to delete the solutions
        # dominated by p' in the set of efficient sols.
        if add:
            to_delete = []
            for i , sorted_val in enumerate(sorted_values[rank_of_p_prime_in_sorted_sols: ]):
                if dominates(p_prime_values, sorted_val):
                    to_delete.append(i)

            # Update of set of approximated efficient sols (delete dominated sols, add p')
            tmp = np.delete(array_of_sols[rank_of_p_prime_in_sorted_sols: ], to_delete, axis = 0)


            array_of_sols = np.concatenate((array_of_sols[:rank_of_p_prime_in_sorted_sols], p_prime.reshape(1,self.size_of_a_sol)), axis = 0)
            array_of_sols = np.concatenate((array_of_sols , tmp), axis = 0)
        return add, array_of_sols


class PLS4(PLS2):
    def  __init__(self, nb_crit, f_voisinage, init_pop, instance, iter_max = 10):
        super().__init__(nb_crit, f_voisinage, init_pop, instance, iter_max)

    def algorithm1(self, L = 5):
        """"""
        The main algorithmic loop of the PLS alogirthm. It is building
        iteratively the population P of approximated solutions.
        """"""
        iter = 0
        while len(self.P) > 0 and iter < self.iter_max:
            # Generate all neighbors p' of each solution in the current population.
            for p in self.P:
                # Get the objective values of sol p
                p_values = self.get_sol_objective_values(p)
                # Get neighbors of sol p
                neighbors = self.N(p, self.weights, self.max_weight, self.values_crit, self.nb_crit, L = L)
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

            iter += 1"""
