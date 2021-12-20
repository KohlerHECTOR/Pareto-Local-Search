# classes d'experiences selon le critère choisit
import time
import numpy as np
from utils import read_instance, init_population, voisinage, init_population_S_weighted, voisinage_L
from pls import PLS, PLS2, PLS4

class experience():
    """ 
    Subclass for the differents exepriences 
    """
    def __init__(self, instance_size, iter_max_, nb_inst):
        """ 
        Function to initialized differents objects of PLS
        """
        self.nb_inst = nb_inst
        self.taille = taille_instance
        
        path = "data/"+taille_instance+"_items/2KP"+taille_instance+"-TA-"
        pls1_list = []
        pls2_list = []
        pls3_list = []
        pls4_list = []
        
        for i in range(nb_inst):

            filename = path + str(i)
            instance = read_instance(filename)
            
            initial_pop = init_population(instance["objects"], instance["max_weight"])
            
            initial_pop_S = init_population_S_weighted(instance["objects"], instance["max_weight"], S = 5)
            pls1_list.append(PLS(voisinage, initial_pop, instance, iter_max = iter_max_))
            """pls2_list.append(PLS2(voisinage, initial_pop, instance, iter_max = iter_max_))
            pls3_list.append(PLS2(voisinage, initial_pop_S, instance, iter_max = iter_max_))
            pls4_list.append(PLS4(voisinage_L, initial_pop_S, instance, iter_max = iter_max_))
        """
        self.pls1 = pls1_list
        """self.pls2 = pls2_list
        self.pls3 = pls3_list
        self.pls4 = pls4_list"""
    
    
class resolution_time(experience):
    """ 
    The experience class for resolution time
    """
    def __init__(self, instance_size, iter_max_, nb_inst):
        super().__init__(instance_size, iter_max_, nb_inst)
    
    def algorithm1(self):
        timePLS1 = []
        timePLS2 = []
        timePLS3 = []
        timePLS4 = []
        
        for i in range(self.nb_inst):
            
            timea = time.time()
            #print("------------------- PLS 1 --------------------")
            self.pls1[i].algorithm1()
            timePLS1.append(time.time() - timea)
            
            timea = time.time()
            #print("------------------- PLS 2 --------------------")
            self.pls2[i].algorithm1()
            timePLS2.append(time.time() - timea)
            
            timea = time.time()
            #print("------------------- PLS 3 --------------------")
            self.pls3[i].algorithm1()
            timePLS3.append(time.time() - timea)
            
            timea = time.time()
            #print("------------------- PLS 4 --------------------")
            self.pls4[i].algorithm1(L = 5)
            timePLS4.append(time.time() - timea)
        
        return np.mean(timePLS1), np.mean(timePLS2), np.mean(timePLS3), np.mean(timePLS4)

class resolution_Dm(experience):
    """
    The experience class for variation of indicator Dm
    """
    
    def __init__(self, instance_size, iter_max_, nb_inst):
        super().__init__(instance_size, iter_max, nb_inst_)
        
    def algorithm1():
        

          
        
            

            
            
            
            
            
            
            
            
        
    
