import Quad_Tree
import pls_Quad_Tree
import utils_multiobj
"""
n1 = [10,10,10]
n2 = [14,18,6]
n3 = [6,16,22]
n4 = [5,5,23]
n5 = [40,16,7]
n6 = [11,15,9]
n7 = [3,25,16]
n8 = [7,8,18]
n9 = [6,9,21]

QT = Quad_Tree.Quad_Tree(nb_crit=3)

QT.insertNode(n1)
QT.insertNode(n2)
QT.insertNode(n3)
QT.insertNode(n4)
QT.insertNode(n5)
QT.insertNode(n6)
QT.insertNode(n7)
QT.insertNode(n8)
QT.insertNode(n9)
print("\nQT nodes : ", [n.getCriteria() for n in QT.getNodes()],"\n")
""""""
print("\n-----------------------------\n\n")
n1 = [10,10,10]
n2 = [14,18,6]
n3 = [6,16,8]
n4 = [7,15,22]
n5 = [5,5,23]
n6 = [3,25,7]
n7 = [6,16,23]
n8 = [7,16,22]

QT = Quad_Tree.Quad_Tree(nb_crit=3)

QT.insertNode(n1)
QT.insertNode(n2)
QT.insertNode(n3)
QT.insertNode(n4)
QT.insertNode(n5)
QT.insertNode(n6)
QT.insertNode(n7)
print("\nQT nodes : ", [n.getCriteria() for n in QT.getNodes()],"\n")
QT.getTree()
    
QT.insertNode(n8)
print("\nQT nodes : ", [n.getCriteria() for n in QT.getNodes()],"\n")

QT.getTree()"""
instance = utils_multiobj.read_instance("data/100_items/2KP100-TA-0")

initial_pop = utils_multiobj.init_population(instance["objects"], instance["max_weight"])
initial_pop_S = utils_multiobj.init_population_S_weighted(2, instance["objects"], instance["max_weight"], S = 5)

PLS_QT = pls_Quad_Tree.PLS_QT(2, utils_multiobj.voisinage, initial_pop, instance, iter_max = 5)
PLS_QT.algorithm1()
import pls
import utils

#PLS = pls.PLS(utils.voisinage, initial_pop, instance, iter_max = 5)
#PLS.algorithm1()



















































