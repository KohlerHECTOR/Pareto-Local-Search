import numpy as np
from utils_multi_objs import dominates, strictly_dominates, init_greedy, read_instance, voisinage, init_population
from gurobipy import *
from elicitation import get_DM

class RBLS():
	def __init__(self, nb_crit, f_voisinage, init_pop, instance, DM, iter_max = 10, agreg = "OWA"):
		self.size_of_a_sol = len(init_pop[0])
		self.N = f_voisinage # neighborhood function
		self.x = init_pop[0]
		self.P = []
		self.F_P = []
		self.DM = DM
		self.mmr_per_query = []
		self.agreg = agreg
		# INSTANCE OF MULTI-OBJS KNAPSACK
		self.objects = instance["objects"]
		self.max_weight = instance["max_weight"]
		self.weights = self.objects["weights"]

		self.nb_crit = nb_crit
		self.values_crit = np.array([self.objects["values_crit_"+str(i+1)] for i in range(self.nb_crit)])

		self.iter_max = iter_max # stopping criterion
		self.improve = True

	def get_sol_objective_values(self, sol):
		return np.array([sol @ self.values_crit[i] for i in range(len(self.values_crit))])

	def algorithm1(self, thresh = 0):
		"""
		The main algorithmic loop of the RBLS alogirthm.
		"""
		iter = 0
		# print("initial x values by DM : {}".format(self.DM @ self.get_sol_objective_values(self.x)))
		while self.improve and iter < self.iter_max:
			neighbors = self.N(self.x, self.weights, self.max_weight)
			neighbors_vals = [self.get_sol_objective_values(n) for n in neighbors]
			non_dominated_neigh = []
			for i, n in enumerate(neighbors_vals):
				add = True
				for j, k in enumerate(neighbors_vals):
					if strictly_dominates(k, n):
						add = False
						break
				if add:
					non_dominated_neigh.append(neighbors[i])

			non_dominated_neigh.append(self.x)
			non_dominated_neigh_values = [self.get_sol_objective_values(n) for n in non_dominated_neigh]
			x, y, valeur, w, z = self.CSS(non_dominated_neigh_values)
			while valeur > thresh:
				if z=='x':
					self.P.append((list(x),list(y)))
					self.F_P.append(w)
				else:
					self.P.append((list(y),list(x)))
					self.F_P.append(w)
				x, y, valeur, w, z = self.CSS(non_dominated_neigh_values)

			y_, max_, w_ = self.MR(self.get_sol_objective_values(self.x), non_dominated_neigh_values)
			if  max_ > thresh:
				MR_min = 10e5
				for i, n_val in enumerate(non_dominated_neigh_values):
					_, max_, _ = self.MR(n_val, non_dominated_neigh_values)
					if max_ < MR_min:
						MR_min = max_
						self.x = non_dominated_neigh[i]
				iter += 1

			else:
				self.improve = False

			# print("new x values by DM : {}".format(self.DM @ self.get_sol_objective_values(self.x)))


		return self.x


	def CSS(self, X):

		x, y, valeur, w = self.MMR(X)

		if valeur >= 0:
			self.mmr_per_query.append(valeur)
		if self.agreg == "OWA":
			if (self.DM @ np.sort(x)) > (self.DM @ np.sort(y)):
				z = "x"
			else:
				z = "y"
		elif self.agreg == "WS":
			if (self.DM @ x) > (self.DM @ y):
				z = "x"
			else:
				z = "y"

		return x, y, valeur, w, z


	def MMR(self, X):

		min_ = 10e5
		x_ = np.zeros(self.nb_crit)
		y_ = np.zeros(self.nb_crit)
		w_ = []

		for x in X :
			y, valeur, w = self.MR(x, X)

			if valeur < min_ :
				min_ = valeur
				x_ = x
				y_ = y
				w_ = w

		return x_, y_, min_, w_


	def MR(self, x, X):


		max_ = -10e5
		y_ = np.zeros(self.nb_crit)
		w_ = []

		for y in X:
			if not np.array_equal(x,y):
				valeur, w = self.PMR_owa(x,y)

				if max_ < valeur :
					max_ = valeur
					y_ = y
					w_ = w

		return y_, max_, w_

	def PMR_owa(self, x,y):
		if self.agreg == "OWA":
			x_rearr = np.sort(x)
			y_rearr = np.sort(y)

			return self.PMR_ws(x_rearr,y_rearr)
		elif self.agreg == "WS":
			return self.PMR_ws(x, y)

	def PMR_ws(self, x,y):

		nbvar = len(x)
		columns = np.arange(nbvar, dtype=int)

		#create model
		m = Model("PMR")
		#aucun affichage de l'optimisation
		m.Params.LogToConsole = 0

		#decision variables declaration
		w = []
		for i in columns:
			w.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d" %(i+1)))

		#integration of new variable
		m.update()

		#objective function
		w = np.array(w)
		obj = (w @ y - w @ x)

		m.setObjective(obj, GRB.MAXIMIZE)

		#constraints
		for i in columns[:-1]:
			m.addConstr(w[i], GRB.GREATER_EQUAL, 0, "Constraint 1_%d" % (i+1))
			m.addConstr(w[i], GRB.GREATER_EQUAL, w[i+1], "Constraint 2_%d" % (i+1))
		m.addConstr(w[nbvar-1], GRB.GREATER_EQUAL, 0, "Constraint 1_%d"%(nbvar+1))

		m.addConstr(sum(w), GRB.EQUAL, 1, "Constraint 3")

		for (a,b) in self.P:

			if self.agreg == "OWA":
				a_rearr = np.sort(a)
				b_rearr = np.sort(b)
			elif self.agreg == "WS":
				a_rearr = a
				b_rearr = b
			m.addConstr(w @ a_rearr, GRB.GREATER_EQUAL, w @ b_rearr)

		# Resolution
		m.optimize()
		"""
		print("")
		print('Solution optimale:')
		for i in columns:
			print('w%d'%(i+1), '=', w[i].x)
		print("")
		print('Valeur de la fonction objectif :', m.objVal)
		"""

		return round(m.getObjective().getValue(),3), [round(w[i].x, 3) for i in columns]

if __name__ == '__main__':
	filename = "data_multi_objs/200_items/2KP200-TA-0"
	instance = read_instance(filename, nb_items = 20, nb_crit = 3)
	initial_pop = init_greedy(instance["objects"], instance["max_weight"])
	DM = get_DM(3)
	rbls = RBLS(nb_crit = 3, f_voisinage = voisinage, init_pop = initial_pop, instance = instance, DM = DM, iter_max = 10, agreg = "OWA")
	rbls.algorithm1(thresh = 0)
