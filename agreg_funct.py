# Implementation des fonctions d'agregations

def OWA(Xe, instance):
    weights = instance["objects"]["weights"] #weights list
    owa = []
    
    for x in Xe :
        owa.append(x @ weights)
        
    return owa
