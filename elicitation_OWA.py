from gurobipy import *
import numpy as np
from utils_multi_objs import get_pareto_fronts_from_data
def main_(X, DM):
	P = []
	F_P = []
	while True:
		x, y, valeur, w, z = CSS(X,P, DM)

		assert z != "", "Aucune preference n'a été donnée"

		if z=='x':
			P.append((list(x),list(y)))
			F_P.append(w)
		else:
			P.append((list(y),list(x)))
			F_P.append(w)

		if valeur <= 0:
			break

		print("P update : ", P, "\n")

	print("Set of preference P : ", P)
	print("Set of agregation function F_P : ", F_P, "\n")
	return P[-1][0], F_P[-1]

def CSS(X,P, DM):

	x, y, valeur, w = MMR(X,P)
	print("valeur PL : ", valeur, " vector w : ", w)
	print("x : ", x, " y : ", y)
	if np.dot(DM, x) > np.dot(DM, y):
		z = "x"
	else:
		z = "y"
	# z = input("x or y ?")

	return x, y, valeur, w, z

def MMR(X,P):

	min_ = 10e5
	x_ = 0
	y_ = 0
	w_ = []

	for x in X :
		y, valeur, w = MR(x, X, P)

		if valeur < min_ :
			min_ = valeur
			x_ = x
			y_ = y
			w_ = w

	return x_, y_, min_, w_

def MR(x, X, P):

	max_ = -10e5
	y_ = 0
	w_ = []

	for y in X:
		if not np.array_equal(x,y):
			valeur, w = PMR_owa(x,y,P)

			if max_ < valeur :
				max_ = valeur
				y_ = y
				w_ = w

	return y_, max_, w_

def PMR_owa(x,y,P):

	x_rearr = np.sort(x)
	y_rearr = np.sort(y)

	return PMR_ws(x_rearr,y_rearr,P)

#Implementation de PMR par Programme Linéaire
def PMR_ws(x,y,P):

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

	for (a,b) in P:

		a_rearr = np.sort(a)
		b_rearr = np.sort(b)
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
	X = get_pareto_fronts_from_data("data_multi_objs/200_items/_nb_crit_3_nb_objects_20_0_pls1_current_pareto_results.txt")[-4]
	print(len(X))
	DM = np.random.random_sample(3) # 3 criteria
	DM = DM/DM.sum()
	DM = -1 * np.sort(-1 * DM) # get an OWA DM
	print("Fake OWA DM :", DM)
	sol_opti, w = main_(X, DM)
	print(" weighted vector : ", w)
