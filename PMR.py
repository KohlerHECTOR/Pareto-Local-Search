#Implementation de PMR par Programme Linéaire
from gurobipy import *
import numpy as np

def PMR_owa(x,y,P):
	x_rearr = np.sort(x)
	y_rearr = np.sort(y)
	return PMR_ws(x,y,P)
	
def PMR_ws(x,y,P):
	
	nbcont = 
	nbvar = len(x)
	
	lines = np.arange(nbcont, dtype=int)
	columns = np.arange(nbvar, dtype=int)
	
	#create model
	m = Model("PMR")

	#decision variables declaration
	w = np.empty(nbvar)
	for i in columns:
		w.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d" %i))
	
	#integration of new variable
	m.update()
	
	#objective function
	obj = w @ y - w @ x
	
	m.setObjective(obj, GRB.MAXIMIZE)
	
	#constraints
	
	
