from experiences import Experience

exp_20 = Experience(instance_size = 20, iter_max_ = 5, nb_inst = 3, tot_items = 100)
exp_30 = Experience(instance_size = 30, iter_max_ = 5, nb_inst = 3, tot_items = 100)
exp_50 = Experience(instance_size = 50, iter_max_ = 5, nb_inst = 3, tot_items = 100)


exp_20.get_data()
exp_30.get_data()
exp_50.get_data()