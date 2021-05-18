# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:44:36 2021

@author: hugob
"""

from shared import point_classe, segment_classe,\
    intersection_demi_droite_segment, dist,\
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

    # Liste qui contiendra les intersections retenues (la plus proche du point
    # et les projections) avec leur status
    liste_intersections_def = list()

    # Pour chaque sommet du polygon, on va chercher son projeté le plus proche
    for sommet in liste_sommets_polygon:
        # Liste des points d'intersections des segments du polygon
        liste_intersections = list()

        # Segment de référence du point O au sommet
        segment_sommet = segment_classe(O, sommet)

        # Pour chaque sommet : on parcours la liste de tous les segments
        # du polygon
        for segment in liste_segments_polygon:
            # On cherche les points d'intersection entre la demi droite
            # définie par O et le sommet et le segment considéré du polygon
            I = intersection_demi_droite_segment(segment_sommet, segment)
            # Si un point d'intersection existe
            if I is not None:
                # Les sommets étant détectés deux fois, on ne les compte qu'une
                if liste_intersections.count([dist(O, I), I]) == 1:
                    continue
                # On l'ajoute à la liste des intersections détectés.
                liste_intersections.append([dist(O, I), I])

        # Pour chaque sommet, une fois toutes les intersections trouvés,
        # on cherche la plus proche du point O
        min_intersection = min(liste_intersections)

        # Un fois l'intersection la plus proche trouvée, il convient
        # d'identifier son status
        status_found = False
        I = min_intersection[1]
        status = None

        # On cherche le statut du point d'intersection trouvé
        while not status_found:
            # Pour cela, on cherche tout d'abord le point juste après le
            # sommet sur la demi-droite
            point_suivant =\
                point_classe(I.x + (sommet.x - O.x)/dist(sommet, O),
                             I.y + (sommet.y - O.y)/dist(sommet, O))

            # On vérifie si ce dernier se situe dans le polygon
            point_to_check = (point_suivant.x, point_suivant.y)
            point_suivant_in_polygon =\
                point_in_polygon(point_to_check, polygon, canvas)

            # On parcours une seconde fois la liste des sommets du polygon
            # pour savoir si le point d'intersection trouvé est un sommet
            for sommet2 in liste_sommets_polygon:
                # Si l'intersection est un sommet et que le point suivant
                # n'est pas dans le polygon (il s'agirait dans ce cas de faire
                # une projection) ou si il n'y a pas d'autre point
                # d'intersection detecté
                if point_egaux(I, sommet2) and\
                    (not point_suivant_in_polygon or
                     len(liste_intersections) == 1):
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
                # Le point d'intersection est donc un sommet
                liste_intersections_def.append([I, "EQUALS"])
                # Il faut ensuite trouver sa projection
                liste_intersections.remove(min_intersection)
                # Il s'agit de l'intersection suivante la plus proche
                min_intersection = min(liste_intersections)
                I = min_intersection[1]
                status = "BEYOND"
                # On refait un tour de boucle pour déterminer le status
                # de cette nouvelle intersection

    # Dans le mode de démonstration, on affiche les intersections définitives
    # trouvés avec la couleur associée à son status.
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

    # Une fois toutes les intersections trouvés, il convient de les trier
    # pour en faire un polygon d'éclairage

    # On parcous la liste des segments du polygon dans l'ordre
    for segment in liste_segments_polygon:
        intersections_sur_segment = list()
        # On parcous la liste des intersections trouvés plus haut
        for intersection in liste_intersections_def:
            I = intersection[0]
            # Si l'intersection est sur le segment considéré, on l'ajoute
            # dans une nouvelle liste.
            if point_appartient_segment(I, segment):
                if not intersection[1] == "AHEAD":
                    intersections_sur_segment.append(
                        [dist(segment.A, I), intersection])
                # Les cas "AHEAD" sont ignorés et supprimés
                else:
                    liste_intersections_def.remove(intersection)
        # Une fois la liste tous les points d'intersections se trouvant sur
        # le segment considéré sont trouvés
        # On vérifie qu'il y en a au moins un
        if not intersections_sur_segment:
            continue
        # On les tris dans l'ordre croissant de leur distance avec le premier
        # point du segment
        intersections_sur_segment.sort()
        # Une fois dans l'ordre
        for intersection in intersections_sur_segment:
            # On leur attribut leur numéro
            count += 1
            I = (intersection[1][0].x, intersection[1][0].y)
            # On sauvegarde les coordonnées de l'intersections dans une
            # nouvelle liste
            liste_intersections_ordones.append(I)
            liste_intersections_def.remove(intersection[1])
            # Dans le mode de démo, on affiche leur numéro à côté
            if mode_demo:
                canvas.create_text(I[0], I[1]-10, text=count, tag='demo')
    # On retourne la liste ordonnée des intersections
    # correspondant au polygon d'éclairage
    return liste_intersections_ordones
