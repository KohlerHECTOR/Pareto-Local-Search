from gurobipy import *
import numpy as np
from utils_multi_objs import get_pareto_fronts_from_data


class ELICIT():
	def __init__(self, X, DM, agreg, nb_crit = 3):
		self.X = X
		self.DM = DM
		self.agreg = agreg
		self.P = []
		self.F_P = []
		self.mmr_per_query = []
		sefl.nb_crit = nb_crit
	def algorithm1(self):
		while True:
			x, y, valeur, w, z = self.CSS()

			assert z != "", "Aucune preference n'a été donnée"

			if z=='x':
				self.P.append((list(x),list(y)))
				self.F_P.append(w)
			else:
				self.P.append((list(y),list(x)))
				self.F_P.append(w)

			if valeur <= 0:
				break

			# print("P update : ", self.P, "\n")

		# print("Set of preference P : ", self.P)
		# print("Set of agregation function F_P : ", self.F_P, "\n")
		return self.F_P[-1]

	def CSS(self):

		x, y, valeur, w = self.MMR()
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
		# z = input("x or y ?")

		return x, y, valeur, w, z

	def MMR(self):

		min_ = 10e5
		x_ = np.zeros(self.nb_crit)
		y_ = np.zeros(self.nb_crit)
		w_ = []

		for x in self.X :
			y, valeur, w = self.MR(x)

			if valeur < min_ :
				min_ = valeur
				x_ = x
				y_ = y
				w_ = w

		return x_, y_, min_, w_

	def MR(self, x):

		max_ = -10e5
		y_ = np.zeros(self.nb_crit)
		w_ = []

		for y in self.X:
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

	#Implementation de PMR par Programme Linéaire
	def PMR_ws(self,x,y):

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

def get_DM(nb_crit, agreg = "OWA"):
	DM = np.random.random_sample(nb_crit) # 3 criteria
	DM = DM/DM.sum()
	# if agreg == "OWA":
	# 	DM = -1 * np.sort(-1 * DM) # get an OWA DM
	print("Fake DM :", DM)
	return DM

if __name__ == '__main__':
	X = get_pareto_fronts_from_data("data_multi_objs/200_items/_nb_crit_3_nb_objects_30_0_pls1_current_pareto_results.txt")[-1]


	DM = get_DM(3, agreg = "WS")
	elic = ELICIT( X, DM, agreg = "WS")
	w = elic.algorithm1()
