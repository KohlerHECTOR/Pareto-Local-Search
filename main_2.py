from experiences import resolution_time, resolution_Dm, resolution_Pm

#Experiences sur des instances de tailles 100 individus

#Sur les 2 premières instances
print("Pour les 2 premières instances de taille 100 individus")
#Temps de resolution
tps_resolution_100 = resolution_time(instance_size="100", iter_max_=5, nb_inst=2)
print("Temps moyen d'execution : ")
print("Avec approximation PLS1 : ", tps_resolution_100.algorithm1("PLS1"))
print("Avec approximation PLS2 : ", tps_resolution_100.algorithm1("PLS2"))
print("Avec approximation PLS3 : ", tps_resolution_100.algorithm1("PLS3"))
print("Avec approximation PLS4 : ", tps_resolution_100.algorithm1("PLS4"))

#Indicateur Dm
dm_100 = resolution_Dm(instance_size="100", iter_max_=5, nb_inst=2)
print("Resultats de l'indicateur Dm : ")
print("Avec approximation PLS1 : ", dm_100.algorithm1("PLS1"))
print("Avec approximation PLS2 : ", dm_100.algorithm1("PLS2"))
print("Avec approximation PLS3 : ", dm_100.algorithm1("PLS3"))
print("Avec approximation PLS4 : ", dm_100.algorithm1("PLS4"))

#Indicateur Pm
pm_100 = resolution_Pm(instance_size="100", iter_max_=5, nb_inst=2)
print("Resultats de l'indicateur Pm : ")
print("Avec approximation PLS1 : ", pm_100.algorithm1("PLS1"))
print("Avec approximation PLS2 : ", pm_100.algorithm1("PLS2"))
print("Avec approximation PLS3 : ", pm_100.algorithm1("PLS4"))
print("Avec approximation PLS4 : ", pm_100.algorithm1("PLS4"))

"""
Mis en commentaire car prend beaucoup de temps d'execution
#Sur les 2 premières instances
print("Pour les 2 premières instances de taille 200 individus")

for i in range(2,8):
    size_ = 100*i
    tps_resolution = resolution_time(instance_size=str(size_), iter_max_=5, nb_inst=2)
    print("Temps moyen d'execution : ")
    print("Avec approximation PLS1 : ", tps_resolution.algorithm1("PLS1"))
    print("Avec approximation PLS2 : ", tps_resolution.algorithm1("PLS2"))
    print("Avec approximation PLS3 : ", tps_resolution.algorithm1("PLS3"))
    print("Avec approximation PLS4 : ", tps_resolution.algorithm1("PLS4"))
    
    #Indicateur Dm
    dm = resolution_Dm(instance_size=str(size_), iter_max_=5, nb_inst=2)
    print("Resultats de l'indicateur Dm : ")
    print("Avec approximation PLS1 : ", dm.algorithm1("PLS1"))
    print("Avec approximation PLS2 : ", dm.algorithm1("PLS2"))
    print("Avec approximation PLS3 : ", dm.algorithm1("PLS3"))
    print("Avec approximation PLS4 : ", dm.algorithm1("PLS4"))
    
    #Indicateur Pm
    pm = resolution_Pm(instance_size=str(size_), iter_max_=5, nb_inst=2)
    print("Resultats de l'indicateur Pm : ")
    print("Avec approximation PLS1 : ", pm.algorithm1("PLS1"))
    print("Avec approximation PLS2 : ", pm.algorithm1("PLS2"))
    print("Avec approximation PLS3 : ", pm.algorithm1("PLS4"))
    print("Avec approximation PLS4 : ", pm.algorithm1("PLS4"))
"""
