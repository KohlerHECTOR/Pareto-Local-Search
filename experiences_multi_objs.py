# classes d'experiences selon le critère choisit
import time
import numpy as np
from utils_multi_objs import read_instance, init_population, voisinage, init_population_S_weighted, voisinage_L, ideal_nadir
from pls_multi_objs import PLS, PLS2, PLS4
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

        sols_pareto_list = []

        ideal_nadir_list = []

        for i in range(nb_inst):

            filename = path + str(i)
            instance = read_instance(filename, nb_items = instance_size, nb_crit = nb_crit)

            ideal_nadir_list.append(ideal_nadir(instance["sols_pareto"]))

            initial_pop = init_population(instance["objects"], instance["max_weight"])

            pls1_list.append(PLS(nb_crit, voisinage, initial_pop, instance, iter_max = iter_max_))

            sols_pareto_list.append(instance["sols_pareto"])
        self.pls1 = pls1_list
        self.sols_pareto = sols_pareto_list
        self.ideal_nadir = ideal_nadir_list

    def get_data(self):
        for i in range(self.nb_inst):
            print("Instance number {}".format(i + 1))
            save_file_sols_pareto = open("data_multi_objs/"+str(self.size)+"_items/_nb_crit_"+ str(self.nb_objectives) + "_nb_objects_"+ str(self.nb_objects)+ "_" +str(i) +"_sols_pareto_results.txt", "w")
            for values in self.sols_pareto[i]:
                to_str = str(values[0])
                for crit in values[1:]:
                    to_str += ", "
                    to_str += str(crit)
                save_file_sols_pareto.write(to_str + "\n")
            save_file_sols_pareto.close()

            save_file_ideal_nadir = open("data_multi_objs/"+str(self.size)+"_items/_nb_crit_"+ str(self.nb_objectives) + "_nb_objects_"+ str(self.nb_objects)+ "_" + str(i) +"_ideal_nadir_results.txt", "w")
            ideal = self.ideal_nadir[i][0]
            nadir = self.ideal_nadir[i][1]
            to_str_ideal = ""
            to_str_nadir = ""
            for crit in ideal:
                to_str_ideal += ", "
                to_str_ideal += str(crit)
            for crit in nadir:
                to_str_nadir += ", "
                to_str_nadir += str(crit)
            save_file_ideal_nadir.write(to_str_ideal + "\n")
            save_file_ideal_nadir.write(to_str_nadir + "\n")
            save_file_ideal_nadir.close()



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


class resolution_time(experience):
    """
    The experience class for resolution time
    """
    def __init__(self, nb_crit, instance_size, iter_max_, nb_inst):
        super().__init__(nb_crit, instance_size, iter_max_, nb_inst)

    def algorithm1(self, PLS):

        if PLS == "PLS1":
            timePLS1 = []
            for i in range(self.nb_inst):
                timea = time.time()
                print("------------------- PLS 1 --------------------")
                self.pls1[i].algorithm1()
                timePLS1.append(time.time() - timea)

            return np.mean(timePLS1)

        elif PLS == "PLS2":
            timePLS2 = []
            for i in range(self.nb_inst):
                timea = time.time()
                print("------------------- PLS 2 --------------------")
                self.pls2[i].algorithm1()
                timePLS2.append(time.time() - timea)

            return np.mean(timePLS2)

        elif PLS == "PLS3":
            timePLS3 = []
            for i in range(self.nb_inst):
                timea = time.time()
                print("------------------- PLS 3 --------------------")
                sel.pls3[i].algorithm1()
                timePLS3.append(time.time() - timea)

            return np.mean(timePLS3)

        elif PLS == "PLS4":
            timePLS4 = []
            for i in range(self.nb_inst):
                timea = time.time()
                print("------------------- PLS 4 --------------------")
                self.pls4[i].algorithm1(L = 5)
                timePLS4.append(time.time() - timea)

            return np.mean(timePLS4)

        return "Aucune methode d'approximation PLS donnée"

class resolution_Dm(experience):
    """
    The experience class for variation of indicator Dm
    """

    def __init__(self, nb_crit, instance_size, iter_max_, nb_inst):
        super().__init__(nb_crit, instance_size, iter_max_, nb_inst)

    def algorithm1(self, PLS):

        if PLS == "PLS1":
            DmPLS1 = []
            for i in range(self.nb_inst):
                # ensemble Y_n des points non-domines par meth exacte
                liste_y = self.sols_pareto[i]

                Y_I, Y_N = self.ideal_nadir[i]

                print("------------------- PLS 1 --------------------")
                self.pls1[i].algorithm1()
                sol_eff_pls1 = self.pls1[i].Xe
                res_pls1 = np.array([self.pls1[i].get_sol_objective_values(s) for s in sol_eff_pls1])
                # liste_yhat : approximation des points non dominés par différents PLS
                DmPLS1.append(indicateur_D(res_pls1, liste_y, Y_I, Y_N))

            return np.mean(DmPLS1)

        elif PLS == "PLS2":
            DmPLS2 = []
            for i in range(self.nb_inst):
                # ensemble Y_n des points non-domines par meth exacte
                liste_y = self.sols_pareto[i]

                Y_I, Y_N = self.ideal_nadir[i]
                print("------------------- PLS 2 --------------------")
                self.pls2[i].algorithm1()
                sol_eff_pls2 = self.pls2[i].Xe
                res_pls2 = np.array([self.pls2[i].get_sol_objective_values(s) for s in sol_eff_pls2])
                # liste_yhat : approximation des points non dominés par différents PLS
                DmPLS2.append(indicateur_D(res_pls2, liste_y, Y_I, Y_N))

            return np.mean(DmPLS2)

        elif PLS == "PLS3":
            DmPLS3 = []
            for i in range(self.nb_inst):
                print("------------------- PLS 3 --------------------")
                self.pls3[i].algorithm1()
                sol_eff_pls3 = self.pls3[i].Xe
                res_pls3 = np.array([self.pls3[i].get_sol_objective_values(s) for s in sol_eff_pls3])
                # liste_yhat : approximation des points non dominés par différents PLS
                DmPLS3.append(indicateur_D(res_pls3, liste_y, Y_I, Y_N))

            return np.mean(DmPLS3)

        elif PLS == "PLS4":
            DmPLS4 = []
            for i in range(self.nb_inst):
                print("------------------- PLS 4 --------------------")
                self.pls4[i].algorithm1()
                sol_eff_pls4 = self.pls4[i].Xe
                res_pls4 = np.array([self.pls4[i].get_sol_objective_values(s) for s in sol_eff_pls4])
                # liste_yhat : approximation des points non dominés par différents PLS
                DmPLS4.append(indicateur_D(res_pls4, liste_y, Y_I, Y_N))

            return np.mean(DmPLS4)

        return "Aucune methode d'approximation PLS donnée"

class resolution_Pm(experience):
    """
    The experience class for variation of indicator Dm
    """

    def __init__(self, nb_crit, instance_size, iter_max_, nb_inst):
        super().__init__(nb_crit, instance_size, iter_max_, nb_inst)

    def algorithm1(self, PLS):

        if PLS == "PLS1":
            PmPLS1 = []
            for i in range(self.nb_inst):
                # ensemble Y_n des points non-domines par meth exacte
                liste_y = self.sols_pareto[i]

                print("------------------- PLS 1 --------------------")
                self.pls1[i].algorithm1()
                sol_eff_pls1 = self.pls1[i].Xe
                res_pls1 = np.array([self.pls1[i].get_sol_objective_values(s) for s in sol_eff_pls1])
                # liste_yhat : approximation des points non dominés par différents PLS
                indicateur = indicateur_P(res_pls1, liste_y)
                PmPLS1.append(indicateur)

            return np.mean(PmPLS1)

        elif PLS == "PLS2":
            PmPLS2 = []
            for i in range(self.nb_inst):
                # ensemble Y_n des points non-domines par meth exacte
                liste_y = self.sols_pareto[i]

                print("------------------- PLS 2 --------------------")
                self.pls2[i].algorithm1()
                sol_eff_pls2 = self.pls2[i].Xe
                res_pls2 = np.array([self.pls2[i].get_sol_objective_values(s) for s in sol_eff_pls2])
                # liste_yhat : approximation des points non dominés par différents PLS
                indicateur = indicateur_P(res_pls2, liste_y)
                PmPLS2.append(indicateur)

            return np.mean(PmPLS2)

        elif PLS == "PLS3":
            PmPLS3 = []
            for i in range(self.nb_inst):
                print("------------------- PLS 3 --------------------")
                self.pls3[i].algorithm1()
                sol_eff_pls3 = self.pls3[i].Xe
                res_pls3 = np.array([self.pls3[i].get_sol_objective_values(s) for s in sol_eff_pls3])
                # liste_yhat : approximation des points non dominés par différents PLS
                PmPLS3.append(indicateur_P(res_pls3, liste_y))

            return np.mean(PmPLS3)

        elif PLS == "PLS4":
            PmPLS4 = []
            for i in range(self.nb_inst):
                print("------------------- PLS 4 --------------------")
                self.pls4[i].algorithm1()
                sol_eff_pls4 = self.pls4[i].Xe
                res_pls4 = np.array([self.pls4[i].get_sol_objective_values(s) for s in sol_eff_pls4])
                # liste_yhat : approximation des points non dominés par différents PLS
                PmPLS4.append(indicateur_P(res_pls4, liste_y))

            return np.mean(PmPLS4)

        return "Aucune methode d'approximation PLS donnée"
