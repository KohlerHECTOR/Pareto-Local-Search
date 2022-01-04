import utils_multiobj
import numpy as np
from utils_multiobj import dominates

class Node_():

    def __init__(self, list_crit, root_=False):
        """
        Function to initialize a node of the quad treee
        """
        self.criteria = list_crit
        self.k = [0]*len(list_crit)
        self.root = root_
        self.successor = []
        self.predecessor = None
        
    def getSuccessor(self):
        return self.successor
        
    def setSuccessor(self, succ):
        self.successor.append(succ)
    
    def getPredecessor(self):
        return self.predecessor
        
    def setPredecessor(self, predec):
        self.predecessor = predec
    
    def dominate(self, y):
        """ return true if self.node dominate y """
        return dominates(np.array(self.criteria), np.array(y.getCriteria()))
    
    def getCriteria(self):
        return self.criteria
    
    def getVectorK(self):
        return self.k
    
    def setVectorK(self, pred):
        x = self.criteria
        y = pred.getCriteria()
        
        for i in range(len(y)):
            """ boucle sur critères du predecesseur """
            if x[i] <= y[i]:
                self.k[i] = 1
            else :
                self.k[i] = 0
                        
    def isRoot(self):
        return self.root
    
class Quad_Tree():

    def __init__(self, nb_crit, size_sol):
        """ 
        Function to initialize the Quad Tree class
        Tree initialized as empty --> set Root/Nodes manually 
        """
        self.nb_crit = nb_crit
        self.root = None
        self.nodes = []
        
    def setRoot(self, x_values):
        """ set Root as the first p' not dominate found """
        self.root = Node_(x_values, True)
        self.nodes.append(self.root)   
        

    def isEmpty(self):
        """ return if list of nodes empty or not
        """
        return len(self.nodes) == 0

    def insertNode(self, x_values):
        """ insert new Node not dominate in tree
        """
        assert self.isEmpty, "OUPS Quad Tree is empty"

        node_ = Node_(x_values)
        position = False
        pred = self.root
        
        if len(self.root.getSuccessor()) == 0 :
            """ 1er noeud inseré dans l'arbre """
            node_.setVectorK(self.root)
            node_.setPredecessor(self.root)
            self.root.setSuccessor(node_)
            self.nodes.append(node_)

        else : 
            while not position :
                node_.setVectorK(pred)
                k = node_.getVectorK()

                """ check if a node dominates node_ """
                for n in self.dominateNode(pred, k):
                    if n.dominate(node_):
                        return position

                for n in self.dominatedByNode(pred, k):
                    if node_.dominate(n):
                        """ supprimer n de l'arbre """
                        self.nodes.remove(n)
                        
                        """ reinserer tous les successeurs de n """
                        for s in n.getSuccessors():
                            self.insertNode(s.getCriteria())
                        
                
                """ verify if same succersorship in  de node_ """
                new_loop = False
                for y in pred.getSuccessor():

                    if np.all(y.getVectorK() == node_.getVectorK()) == True :
                        """ node_ has same successorship than y 
                            --> check if node_ dominated by y """
                        if not y.dominate(node_) : 
                            """ node_ not dominated by y """
                            pred = y
                            new_loop = True
                            break
                
                if not new_loop :
                    """ insertion de node_ """
                    node_.setPredecessor(pred)
                    pred.setSuccessor(node_)
                    self.nodes.append(node_)
                    position = True

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
        for s in pred.getSuccessor():
            k_prim = s.getVectorK()
            
            if np.all([k[i] == k_prim[i] for i in range(len(k)) if k[i]==1]) == True and (np.all(k == k_prim)==False):
                list_dominate_by_node.append(s)
                
        return list_dominate_by_node
        
    def getNodes(self):
        return self.nodes
        
        
        
        
