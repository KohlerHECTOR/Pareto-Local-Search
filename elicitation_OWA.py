from gurobipy import *
import numpy as np

def CSS(X,P):
	return MMR(X,P)
	
def MRR(X,P):
	min_ = 10^3
	x_ = 0
	for x in X :
		y, valeur = MR(x, X, P)
		if valeur < min_ :
			min_ = valeur 
			x_ = x
	return x_, y, min_

def MR(x, X, P):
	max_ = 0
	y_ = 0
	for y in X.solution:
		valeur = PMR_owa(x,y,P)
		if max_ < valeur :
			max_ = valeur
			y_ = y
	return y_, max_

def PMR_owa(x,y,P):
	x_rearr = np.sort(x)
	y_rearr = np.sort(y)
	return PMR_ws(x_rearr,y_rearr,P)
	
#Implementation de PMR par Programme Linéaire
def PMR_ws(x,y,P):
	
	nbvar = len(x)
	columns = np.arange(nbvar, dtype=int)
	
	print("vector columns : ", columns)
	
	#create model
	m = Model("PMR")

	#decision variables declaration
	w = np.empty(nbvar)
	for i in columns:
		w.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d" %(i+1)))
	
	#integration of new variable
	m.update()
	
	#objective function
	obj = (w @ y - w @ x)
	
	m.setObjective(obj, GRB.MAXIMIZE)
	
	#constraints

	for i in columns[:-1]:
		m.addConstr(w[i] >= 0, "Constraint 1_%d" % (i+1))
		m.addConstr(w[i] >= w[i+1], "Constraint 2_%d" % (i+1))
	m.addConstr(w[nb_var-1] >= 0, "Constraint 1_%d"%(nb_var+1))
	
	m.addConstr(sum(w) == 1, "Constraint 3")
	
	for (a,b) in P:
		a_rearr = np.sort(a)
		b_rearr = np.sort(b)
		m.addConst(w @ a_rearr >= w @ b_rearr)
		
	# Resolution
	m.optimize()
	
	print("")
	print('Solution optimale:')
	for i in columns:
		print('w%d'%(i+1), '=', w[i].x)
	print("")
	print('Valeur de la fonction objectif :', m.objVal)
	
	return m.objVal
	

