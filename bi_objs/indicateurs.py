
import numpy as np

def intersect2d(a,b):
      return np.array([x for x in set(tuple(x) for x in a) & set(tuple(x) for x in b)])

def indicateur_P(liste_y, liste_yhat):
    list_inters= intersect2d(liste_y,liste_yhat)
    return len(list_inters)/len(liste_y)

def dist_euclid(a, b):
    p_1 = etendue(Y_N, Y_I, 1)
    p_2 = etendue(Y_N, Y_I, 2)
    return np.sqrt(p_1 * (a[0] - b[0]) ** 2 +  p_2 * (a[1] - b[1]) ** 2)

def etendue(Y_N, Y_I, k):
    denom = Y_I[k - 1] - Y_N[k - 1]
    if denom != 0:
        return 1/denom
    else:
        return 0

def dist_prime(a, b):
    liste_dist=np.empty(np.size(a)[0])
    for y2 in a:
        liste_dist.append(dist_euclid(y2,b))
    return np.min(liste_dist)

def indicateur_D(liste_yhat, liste_y, Y_I, Y_N):
    sum_ = 0
    for y1 in liste_y:
        sum_ += dist_prime(liste_yhat, y1)
    return sum_/len(liste_y)
