import experiences
import experiences_multi

""" Fonction main de comparaison de resolution between implementations bi and multi objectif of PLS """

#Sur les 2 premières instances
print("Pour les 2 premières instances de taille 100 individus")
#Temps de resolution
tps_resol_BI = experiences.resolution_time(instance_size="100", iter_max_=5, nb_inst=1)
tps_resol_MULT = experiences_multi.resolution_time(nb_crit=2, instance_size="100", iter_max_=5, nb_inst=1)
print("Temps moyen d'execution : ")
"""print("BI-OBJ : Avec approximation PLS1 : ", tps_resol_BI.algorithm1("PLS1"))
print("MULTI OBJ : Avec approximation PLS1 : ", tps_resol_MULT.algorithm1("PLS1"))"""
print("BI-OBJ : Avec approximation PLS4 : ", tps_resol_BI.algorithm1("PLS4"))
print("MULTI OBJ : Avec approximation PLS4 : ", tps_resol_MULT.algorithm1("PLS4"))
"""
#Indicateur Dm
dm_BI = experiences.resolution_Dm(instance_size="100", iter_max_=5, nb_inst=2)
dm_MULT = experiences_multi.resolution_Dm(nb_crit=2, instance_size="100", iter_max_=5, nb_inst=2)
print("Resultats de l'indicateur Dm : ")
print("BI-OBJ : Avec approximation PLS1 : ", dm_BI.algorithm1("PLS1"))
print("MULTI OBJ : Avec approximation PLS1 : ", dm_MULT.algorithm1("PLS1"))
print("BI-OBJ : Avec approximation PLS4 : ", dm_BI.algorithm1("PLS4"))
print("MULTI OBJ : Avec approximation PLS4 : ", dm_MULT.algorithm1("PLS4"))

#Indicateur Pm
pm_BI = resolution_Pm(instance_size="100", iter_max_=5, nb_inst=2)
pm_MULT = experiences_multi.resolution_Pm(nb_crit=2, instance_size="100", iter_max_=5, nb_inst=2)
print("Resultats de l'indicateur Pm : ")
print("BI-OBJ : Avec approximation PLS1 : ", pm_BI.algorithm1("PLS1"))
print("MULTI OBJ : Avec approximation PLS1 : ", pm_MULT.algorithm1("PLS1"))
print("BI-OBJ : Avec approximation PLS4 : ", pm_BI.algorithm1("PLS4"))
print("MULTI OBJ : Avec approximation PLS4 : ", pm_MULT.algorithm1("PLS4"))
"""
