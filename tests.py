# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 18:43:00 2021

@author: hugob
"""


def status_intersection(liste_intersections, sommet, points_indentifies = list()):
    '''
    

    Parameters
    ----------
    intersection : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    liste_intersections.sort()
    I = liste_intersections[0][1]
    indice_sommet = liste_intersections[0][2]

    if points_indentifies:
        recursif = True

    sommet = False

    # Si il s'agit du sommet en cours
    if point_egaux(I, sommet):
        sommet = True

    # Si il s'agit d'un autre sommet du polygon
    elif sommet_du_polygon(I):
        sommet = True

    if sommet:
        # On ajoute le statut du point indentifié
        status = "EQUALS"
        if recursif:
            status = "BEYOND"
        points_indentifies.append([I, status])

        # Si il ne s'agit pas d'une projection, fin de traitement
        if not verif_si_projection(sommet, indice_sommet):
            return points_indentifies

        # Sinon, on passe à l'intersection suivante
        del liste_intersections[0]
        # On rappelle la fonction
        return status_intersection(liste_intersections, sommet, points_indentifies)

    status = "AHEAD"
    if recursif:
        status = "BEYOND"
    points_indentifies.append([I, status])
    return points_indentifies


def verif_si_projection(self, sommet, indice_sommet):
    '''
    

    Parameters
    ----------
    sommet : TYPE
        DESCRIPTION.
    indice_sommet : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    det1 = determinant_3_points(self.O, sommet,
        self.liste_sommets_polygon[indice_sommet-1])

    if indice_sommet == len(self.liste_sommets_polygon)-1:
        indice_sommet = -1

    det2 = determinant_3_points(self.O, sommet,
        self.liste_sommets_polygon[indice_sommet+1])

    if signe(det1) == signe(det2):
        return True
    return False

def sommet_du_polygon(self, I):
    '''
    

    Parameters
    ----------
    I : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    for sommet in self.liste_sommets_polygon():
        if point_egaux(I, sommet):
            return True
    return False
