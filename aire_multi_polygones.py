from shapely.geometry import Polygon
from shapely.ops import unary_union
from shared import intersection_segments
from aire_polygone import aire_polygone

def aire_multi_polygones(polygones):
    """
    Arguments :
        - polygones : liste de listes de points sous forme liste
    Retourne :
        - l'aire de la fusion des polygones
    """
    liste_classe_polygon = []
    for polygone in polygones:
        for elem in polygone:
            elem = list(elem)
            elem[0] = int(elem[0])
            elem[1] = int(elem[1])
        liste_classe_polygon.append(Polygon(polygone))

    polygone_fusion = unary_union(liste_classe_polygon)
    aire = polygone_fusion.area
    return aire
