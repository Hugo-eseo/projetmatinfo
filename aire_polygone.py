from shared import point_classe
import time

def aire_polygone(liste_sommets):
    """
    Argument : 
        - liste_points liste de tuples (x, y) ou de listes [x, y] ou d'objets
          de type 'Point'.
    retourne :
        - l'aire du polygone defini par les points.
    """
    liste_points = []
    for elem in liste_sommets:
        if type(elem) is tuple or type(elem) is list:
            A = point_classe(elem[0], elem[1])
            liste_points.append(A)
        elif type(elem) is point_classe:
            liste_points.append(elem)

    sommeX_Y1, sommeY_X1 = 0, 0
    for i in range(len(liste_points)):
        if i+1 == len(liste_points):
            sommeX_Y1 += liste_points[i].x * liste_points[0].y
            sommeY_X1 += liste_points[i].y * liste_points[0].x
        else:
            sommeX_Y1 += liste_points[i].x * liste_points[i+1].y
            sommeY_X1 += liste_points[i].y * liste_points[i+1].x
    aire = int(abs(0.5*(sommeX_Y1-sommeY_X1)))
    return aire

    
if __name__ == "__main__":
    # test
    t1 = time.time()
    aire = aire_polygone([point_classe(0, 0), (0, 3), point_classe(3, 3), (3, 0)])  # retourne 9
    t2 = time.time()
    print(t2-t1, 'secondes')    # sans numba : 2.288818359375e-05 secondes
    