# classes d'experiences selon le critère choisit
import time
import numpy as np
from utils_multi_objs import read_instance, init_population, voisinage, ideal_nadir
from pls_multi_objs import PLS
from indicateurs import indicateur_P, indicateur_D, intersect2d

class Experience():
    """
    Subclass for the differents exepriences
    """
    def __init__(self, nb_crit, instance_size, iter_max_, nb_inst, tot_items = 100):
        """
        Function to initialized differents objects of PLS
        """
        self.nb_inst = nb_inst
        self.size = tot_items
        self.nb_objects = instance_size
        self.nb_objectives = nb_crit

        path = "data_multi_objs/"+str(tot_items)+"_items/2KP"+str(tot_items)+"-TA-"
        pls1_list = []

        for i in range(nb_inst):

            filename = path + str(i)
            instance = read_instance(filename, nb_items = instance_size, nb_crit = nb_crit)
            print(instance)


            initial_pop = init_population(instance["objects"], instance["max_weight"])

            pls1_list.append(PLS(nb_crit, voisinage, initial_pop, instance, iter_max = iter_max_))

        self.pls1 = pls1_list

    def get_data(self):
        for i in range(self.nb_inst):
            print("Instance number {}".format(i + 1))



            save_file_pls1_times = open("data_multi_objs/"+str(self.size)+"_items/_nb_crit_"+ str(self.nb_objectives) + "_nb_objects_"+ str(self.nb_objects)+ "_" + str(i) +"_pls1_times_results.txt", "w")
            save_file_pls1_pop_size = open("data_multi_objs/"+str(self.size)+"_items/_nb_crit_"+ str(self.nb_objectives) + "_nb_objects_"+ str(self.nb_objects)+ "_" +str(i) +"_pls1_pop_size_results.txt", "w")
            save_file_pls1_current_pareto = open("data_multi_objs/"+str(self.size)+"_items/_nb_crit_"+ str(self.nb_objectives) + "_nb_objects_"+ str(self.nb_objects)+ "_" +str(i) +"_pls1_current_pareto_results.txt", "w")

            print("------------------- PLS 1 --------------------")
            timea = time.time()
            self.pls1[i].algorithm1(file_pop = save_file_pls1_pop_size, file_pareto = save_file_pls1_current_pareto)
            save_file_pls1_times.write(str(time.time() - timea))

            save_file_pls1_times.close()
            save_file_pls1_pop_size.close()
            save_file_pls1_current_pareto.close()
