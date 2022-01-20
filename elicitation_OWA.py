from gurobipy import *
import numpy as np

def main_(X):
	P=[]
	while True:
		x, y, valeur = CSS(X,P)
		print("### ", x, " ", y, " ", valeur)
		input("x, y, valeur")
		if valeur <= 0:
			break
		print("P : ", P)
		print("x y : ", x, " ", y)
		z = input("x or y ?")
		
		if z=='x':
			P.append((x,y))
		else:
			P.append((y,x))
		print("main_ : ", P)
		input("Nouvelle boucle ?")
	return P

def CSS(X,P):
	print("IN CSS")
	return MMR(X,P)
	
def MMR(X,P):
	print("\n\nIN MMR")
	min_ = 10e3
	print("min_  ", min_)
	x_ = 0
	print("X : ", X)
	for x in X :
		y, valeur = MR(x, X, P)
		
		print("~~ x : ", x, "  ", valeur)
		#input("x")
		if valeur < min_ :
			print(valeur, "<", min_)
			#input("valeur < min")
			min_ = valeur 
			x_ = x
	print(x_, "  ", min_)
	#input("#### MMR return x, min")
	return x_, y, min_

def MR(x, X, P):
	print("IN MR")
	max_ = 0
	y_ = 0
	print("X : ", X)
	for y in X:
		print("x : ", x, " ## y : ", y)
		valeur = PMR_owa(x,y,P)
		if max_ < valeur :
			print(max_, "<", valeur)
			#input("max < valeur")
			max_ = valeur
			y_ = y
	print(y_, "  ", max_)
	#input("#### MR return y, max") 
	return y_, max_

def PMR_owa(x,y,P):
	print("IN PMR_owa")
	x_rearr = np.sort(x)
	y_rearr = np.sort(y)
	return PMR_ws(x_rearr,y_rearr,P)
	
#Implementation de PMR par Programme Linéaire
def PMR_ws(x,y,P):
	print("IN PMR_ws")
	
	nbvar = len(x)
	columns = np.arange(nbvar, dtype=int)
	
	print("vector columns : ", columns)
	
	#create model
	m = Model("PMR")

	#decision variables declaration
	w = []
	for i in columns:
		w.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d" %(i+1)))
		
	print(w)
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
	
	print("avant for")
	for (a,b) in P:
		print("in for : ", a, " ", b)
		a_rearr = np.sort(a)
		b_rearr = np.sort(b)
		print(a_rearr, " ", b_rearr)
		input("a_rearr, b_rearr")
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

	return m.getObjective().getValue()
	
if __name__ == '__main__':
	X = np.array([[45,32], [21,3], [5,90]])
	print(main_(X))
