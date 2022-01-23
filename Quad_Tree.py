import numpy as np
from utils_multiobj import dominates

class Node_():

    def __init__(self, list_crit, values_crit, root_=False):
        """
        Function to initialize a node of the quad treee
        """
        self.criteria = list_crit	#sac a dos binaire
        self.k = [0]*len(values_crit)
        self.root = root_
        self.successor = []
        self.predecessor = None
        self.deleted = False
        self.values_crit = values_crit
        
    def setSuccessor(self, succ):
        print(succ.getVectorK())
        self.successor.append(succ)

    def setPredecessor(self, predec):
        self.predecessor = predec
            
    def setVectorK(self, pred):
        #x = self.criteria
        #y = pred.getCriteria()
        x = self.get_sol_objective_values()
        y = pred.get_sol_objective_values()
        
        print("A.", x, "  ", y)
        
        for i in range(len(y)):
            print("i : ", i)
            """ boucle sur critères du predecesseur """
            if x[i] <= y[i]:
                self.k[i] = 1
            else :
                self.k[i] = 0
                
        print("B. ", self.k)
    
    def setDeleted(self):
        self.deleted = True
        
    def dominate(self, y):
        """ return true if self.node dominate y """
        return dominates(np.array(self.criteria), np.array(y.getCriteria()))
    
    def isRoot(self):
        return self.root
    
    def isDeleted(self):
        return self.deleted
        
    def getSuccessor(self):
        return self.successor
        
    def getPredecessor(self):
        return self.predecessor
        
    def getCriteria(self):
        return self.criteria
    
    def getVectorK(self):
        return self.k
        
    def get_sol_objective_values(self):
        return np.array([self.criteria @ self.values_crit[i] for i in range(len(self.values_crit))]) 
    
class Quad_Tree():

    def __init__(self, nb_crit, values_crit):
        """ 
        Function to initialize the Quad Tree class
        Tree initialized as empty --> set Root/Nodes manually 
        """
        self.nb_crit = nb_crit
        self.values_crit = values_crit
        self.root = None
        self.nodes = []
        self.toDelete = []
        
    def setRoot(self, x_values, values_crit):
        """ set Root as the first p' not dominate found """
        self.root = Node_(x_values, values_crit, True)
        self.nodes.append(self.root)

    def isEmpty(self):
        """ return if list of nodes empty or not
        """
        return len(self.nodes) == 0
   
    def insertNode(self, x_values, values_crit):
        """ insert new Node not dominate in tree
        """
        assert self.isEmpty, "OUPS Quad Tree is empty"

        node_ = Node_(x_values, values_crit)
        add = False
        pred = self.root
        
        if self.isEmpty():
            """ insertion de la racine de l'arbre """
            self.setRoot(x_values)
            add = True
            return add

        else : 
            while not add :
                new_loop = False
                node_.setVectorK(pred)
                k = node_.getVectorK()

                """ check if a node dominates node_ """
                for n in self.dominateNode(pred, k):
                    if n.dominate(node_):
                        """ condition 1. a solution dominates x, discard x """
                        return add
                
                for n in self.dominatedByNode(pred, k):
                    """ boucle sur noeuds domines par node_ , diff de node_"""

                    if n.getVectorK() == node_.getVectorK() :
                        if not node_.dominate(n):
                            """ same vector k and node_ not dominate by y """
                            pred = n
                            new_loop = True
                            break
                            
                    if not new_loop and node_.dominate(n):
                        
                        """ delete successor of n dominate by node_ """
                        for s in n.getSuccessor():
                            if node_.dominate(s):
                                s.setDeleted()
                                self.toDelete.append(s)
                            else:
                                s.setVectorK(node_)
                                s.setPredecessor(node_)
                                node_.setSuccessor(s)
                        
                        if not add:
                            """ noeud n delete from tree """
                            self.nodes[self.nodes.index(n)] = node_
                            node_.setPredecessor(pred)	#set predecessor of node_
                            # update successor of pred --> remplace n by node_
                            pred.getSuccessor()[pred.getSuccessor().index(n)] = node_
                            """ delete nodes dominate by node_ """
                            [self.nodes.remove(n) for n in self.toDelete if self.nodes.count(n)>0]
                            self.nodes
                            add = True
                            
                        else:
                            """ node_ already add in tree --> delete n dominate by node_ """
                            if self.nodes.count(n)>0:
                                self.nodes.remove(n)
                
                if not add :
                    """ insertion de node_ """
                    node_.setPredecessor(pred)
                    node_.setVectorK(pred)
                    pred.setSuccessor(node_)
                    self.nodes.append(node_)
                    add = True
                    return add
                    
        return add

    def dominateNode(self, pred, k):
        """ get vectors that dominate node_ """
        list_dominate_node = []
        for s in pred.getSuccessor():
            k_prim = s.getVectorK()
            
            if np.all([k[i] == k_prim[i] for i in range(len(k)) if k[i]==0]) == True and (np.all(k == k_prim)==False):
                list_dominate_node.append(s)
                
        return list_dominate_node
    
    def dominatedByNode(self, pred, k):
        """ get vectors that are dominated by node_ """
        list_dominate_by_node = []
        same = None
        for s in pred.getSuccessor():
            k_prim = s.getVectorK()
            
            if np.all([k[i] == k_prim[i] for i in range(len(k)) if k[i]==1]) == True and (np.all(k == k_prim)==False):
                list_dominate_by_node.append(s)
            
            if np.all(k == k_prim)==True:
                same = s
        if same !=None:
            return [same] + list_dominate_by_node    
        return list_dominate_by_node
        
    def copy_(self, quad_tree):
        """ copy of a quad tree """
        
        assert self.nb_crit == quad_tree.getNb_crit(), "nb criteria different btw 2 Quad Tree"
         
        new_QT = Quad_Tree(quad_tree.getNb_crit(), quad_tree.getValues())
        
        root = quad_tree.getRoot()
        new_QT.setRoot(root.getCriteria())
        new_QT.setNodes(quad_tree.getNodes())
        
        return new_QT        
        
    def setNodes(self, l_nodes):
        new_nodes = []
        for n in l_nodes:
            node = Node_(n.getCriteria(), n.isRoot())
            
            [node.setSuccessor(s) for s in n.getSuccessor()]
            node.setPredecessor(n.getPredecessor)
                
            new_nodes.append(node)
        return new_nodes
        
    def getNb_crit(self):
        return self.nb_crit
        
    def getValues(self):
        return self.values_crit 
        
    def getRoot(self):
        return self.root
        
    def getNodes(self):
        return self.nodes
        
    def getTree(self):
    
        print("Root : ", self.get_sol_objective_values(self.root.getCriteria()), " has for successor : ")
        for n in self.root.getSuccessor() :
            print(self.get_sol_objective_values(n.getCriteria()))
            
        for n in self.nodes[1:]:
            if len(n.getSuccessor()) > 0:
                print("Node ", self.get_sol_objective_values(n.getCriteria(), "has for successor : ", [j.getCriteria() for j in n.getSuccessor()]))
                    
            else:
                print ("Node ", self.get_sol_objective_values(n.getCriteria()), " is a leaf")

        
        
        
