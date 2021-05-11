# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:44:36 2021

@author: hugob
"""

from shared import point_classe, segment_classe, intersection_segments, dist,\
    point_egaux, point_appartient_segment

from point_in_polygon import point_in_polygon

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

    # Création d'une liste contenant les sommets du polygon
    liste_sommets_polygon = list()
    for point in polygon:
        liste_sommets_polygon.append(point_classe(point[0], point[1]))

    # Le point O est le point où l'on souhaite connaître le polygon d'éclairage
    O = point_classe(start_point[0], start_point[1])

    if mode_demo:
        # Affichage de la source lumineuse en jaune
        canvas.create_oval(O.x-size, O.y-size, O.x+size, O.y+size,
                           fill='white', tag='demo')

    # Liste des intersections définitives avec leur status
    liste_intersections_def = list()

    for sommet in liste_sommets_polygon:
        # Liste des points d'intersections avec les sommets du polygon
        liste_intersections = list()

        # On cherche toutes les intersections avec les segments du polygon
        segment_sommet = segment_classe(O, sommet)
        for segment in liste_segments_polygon:
            I = intersection_segments(segment_sommet, segment)
            # Si il y a un point d'intersection
            if I is not None:
                # Les sommets étant détectés deux fois, on ne les compte qu'une
                if liste_intersections.count([dist(O, I), I]) == 1:
                    continue
                liste_intersections.append([dist(O, I), I])
        # Une fois toutes les intersections trouvés, on cherche la plus proche
        # du point O
        min_intersection = min(liste_intersections)
        status_found = False
        I = min_intersection[1]
        status = None
        # On cherche le statut du point d'intersection trouvé
        while not status_found:
            # On cherche le point juste après le sommet sur la même demi-droite
            point_suivant = point_classe(I.x + (sommet.x - O.x)/dist(sommet, O),
                                         I.y + (sommet.y - O.y)/dist(sommet, O))
            canvas.create_oval(point_suivant.x-size, point_suivant.y-size, point_suivant.x+size, point_suivant.y+size,
                               fill='purple', tag='demo')
            point_suivant_in_polygon = point_in_polygon(point_suivant, polygon, canvas)
            # On parcours une seconde fois la liste des sommets du polygon
            # En vérité, cela n'est utile que dans le cas où l'on fait
            # plusieurs tours de boucle
            for sommet in liste_sommets_polygon:
                # Si l'intersection est un sommet
                print(point_suivant_in_polygon)
                if point_egaux(I, sommet) and not point_suivant_in_polygon: # Problème vient d'ici !! Fonction point in polygon
                    # Si il ne s'agit pas d'une projection
                    if status is None:
                        # Le statut est donc "EQUALS"
                        status = "EQUALS"
                    # On l'ajoute à la liste finale
                    liste_intersections_def.append([I, status])
                    status_found = True
                    # Sortie du for
                    break
            # Si le point suivant n'est pas dans le polygon
            if not point_suivant_in_polygon and not status_found:
                # Si il ne s'agit pas d'une projection
                if status is None:
                    # Le statut est donc "AHEAD"
                    status = "AHEAD"
                # On l'ajoute à la liste finale
                liste_intersections_def.append([I, status])
                status_found = True
            # Sinon c'est une projection
            elif not status_found:
                # Il faut ajouter ce point d'intersection comme sommet
                liste_intersections_def.append([I, "EQUALS"])
                # Puis chercher l'intersection suivante
                liste_intersections.remove(min_intersection)
                min_intersection = min(liste_intersections)
                I = min_intersection[1]
                status = "BEYOND"
                print("Hello world")

    if mode_demo:
        for intersection in liste_intersections_def:
            I = intersection[0]
            canvas.create_line(O.x, O.y, I.x, I.y,
                               fill='white', tag='demo')
            if intersection[1] == 'AHEAD':
                continue
            elif intersection[1] == 'EQUALS':
                color = 'green'
            else:
                color = 'blue'
            canvas.create_oval(I.x-size, I.y-size, I.x+size, I.y+size,
                               fill=color, tag='demo')

    # Liste des intersections dans l'ordre
    liste_intersections_ordones = list()
    count = 0
    # Une fois toutes les intersections trouvés
    for segment in liste_segments_polygon:
        intersections_sur_segment = list()
        for intersection in liste_intersections_def:
            I = intersection[0]
            if point_appartient_segment(I, segment):
                if not intersection[1] == "AHEAD":
                    intersections_sur_segment.append([dist(segment.A, I), intersection])
                else:
                    liste_intersections_def.remove(intersection)
        if not intersections_sur_segment:
            continue
        intersections_sur_segment.sort()
        for intersection in intersections_sur_segment:
            count += 1
            I = (intersection[1][0].x, intersection[1][0].y)
            liste_intersections_ordones.append(I)
            liste_intersections_def.remove(intersection[1])
            if mode_demo:
                canvas.create_text(I[0], I[1]-10, text=count, tag='demo')
    return liste_intersections_ordones
