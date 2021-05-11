# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:44:36 2021

@author: hugob
"""

from shared import point_classe, segment_classe

# Taille des point affichés sur le canvas
size = 4


def polygon_eclairage(start_point, polygon, canvas, mode_demo=False):
    """Arguments :
        - start_point : Tuple ou liste sous la forme (x, y) ou [x, y]
        - polygon : Liste de sommets sous la forme  [(xA, yA), (xB, yB) ...]
        - canvas : Canvas de dessin
        - mode_demo : Boolean, True pour activer le mode de démonstration
    Retourne le polygon d'éclairage sous la forme d'une liste de points
    au format tuple : [(xA, yA), (xB, yB) ...]"""

    # Vérifications élémentaires
    if not (type(start_point) == tuple or type(start_point) == list):
        return None
    if not (len(start_point) == 2):
        return None

    canvas.delete("demo")
    # Récupération des informations de la fenêtre
    width = canvas.winfo_width()

    # Création d'une liste contenant les segments du polygon
    liste_segments_polygon = list()
    A = point_classe(polygon[0][0], polygon[0][1])
    for i in range(1, len(polygon)):
        B = point_classe(polygon[i][0], polygon[i][1])
        liste_segments_polygon.append(segment_classe(A, B))
        A = B
    B = point_classe(polygon[0][0], polygon[0][1])
    liste_segments_polygon.append(segment_classe(A, B))

    # Le point 0 dans tout l'algorithme correspond au point
    # dont nous souhaitons savoir si il est dans le poylgon
    O = point_classe(start_point[0], start_point[1])
    
    