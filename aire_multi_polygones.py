from shapely.geometry import Polygon
from shapely.ops import unary_union
from shared import intersection_segments, point_classe, segment_classe
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

def aire_deux_polygones(polygones):
    """
    Arguments :
        - polygones : liste de listes d'objets de classe 'Point' (len=2)
    Retourne :
        - l'aire de la fusion des polygones
    """
    segments_polygone1, segments_polygone2 = [], []

    # recuperer la liste des segments
    for i in range(len(polygones[0])):
        if i > 0:
            A = polygones[0][i]
            B = polygones[0][i-1]
            segments_polygone1.append(segment_classe(B, A))
    A = polygones[0][0]
    B = polygones[0][-1]
    segments_polygone1.append(segment_classe(B, A))

    for i in range(len(polygones[1])):
        if i > 0:
            A = polygones[1][i]
            B = polygones[1][i-1]
            segments_polygone2.append(segment_classe(B, A))
    A = polygones[1][0]
    B = polygones[1][-1]
    segments_polygone2.append.append(segment_classe(B, A))

    intersections_polygones = []
    # liste des intersections entre les segments des polygones
    for segment1 in segments_polygone1:
        for segment2 in segments_polygone2:
            intersection = intersection_segments(segment1, segment2)
            if intersection is not None:
                intersections_polygones.append(intersection)












if __name__ == '__main__':
    # polygones = [[(0, 0), (1, 0), (1, 1), (0, 1)], [(0, 0), (3, 1), (1, 3)]]
    polygones = [[[0, 0], [3, 1], [1, 3]]]
    print(aire_multi_polygones(polygones))



