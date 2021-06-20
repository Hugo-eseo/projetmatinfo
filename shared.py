# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 22:07:19 2021

@author: hugob
"""

import math

# Présion demandée la validation des calculs
precision = 0.01


class point_classe():
    """Docstring"""

    def __init__(self, x, y):
        """Prend en argument les coordonées x et y du point"""
        self.x, self.y = x, y

    def __repr__(self):
        string = f"({self.x}, {self.y})"
        return string
    
    def __eq__(self, other):
        return (self.x, self.y) == other

    def return_tuple(self):
        return (self.x, self.y)


class segment_classe():
    """Docstring"""

    def __init__(self, point1, point2):
        """Prend en argument deux points (de classe 'point')
        définissants un segment"""
        self.A, self.B = point1, point2

    def __repr__(self):
        string = "[" + str(self.A) + "," + str(self.B) + "]"
        return string

    def return_tuple(self):
        return [self.A.return_tuple(), self.B.return_tuple()]


def signe(n):
    """Renvoie le signe d'un nombre passé en argument"""
    if n == 0:
        return 0
    if n > 0:
        return 1
    return -1


def det2(mat):
    """Argument :
        - mat : matrice 2*2
    Retourne le déterminant en dimension 2 de mat"""
    return(mat[0][0]*mat[1][1]-mat[1][0]*mat[0][1])


def det3(mat):
    """Argument :
        - mat : matrice 3*3
    Retourne le déterminant en dimension 3 de mat"""
    a = mat[0][0]*det2([[mat[1][1], mat[1][2]], [mat[2][1], mat[2][2]]])
    b = mat[0][1]*det2([[mat[1][0], mat[1][2]], [mat[2][0], mat[2][2]]])
    c = mat[0][2]*det2([[mat[1][0], mat[1][1]], [mat[2][0], mat[2][1]]])
    return a-b+c


def dist(point1, point2):
    """Arguments :
        - point1, point2 : objets de classe 'point'
    Retourne la distance entre 'point1' et 'point2'"""
    return(math.sqrt((point2.x - point1.x)**2+(point2.y - point1.y)**2))


def determinant_3_points(point1, point2, point3):
    """Arguments :
        - point1, point2, point3 : objets de classe 'point'
    Retourne le déterminant de 3 points"""
    mat = [[point1.x, point2.x, point3.x], [point1.y, point2.y, point3.y],
           [1, 1, 1]]
    return det3(mat)


def point_appartient_segment(point, segment):
    """Arguments :
        - point : objet de classe 'point'
        - segment : objet de classe 'segment'
    Retourne True si 'point' appartient à 'segment' (bornes incluses).
    False sinon"""
    if abs(determinant_3_points(point, segment.A, segment.B)) < precision:
        if abs(dist(point, segment.A) + dist(point, segment.B) -
               dist(segment.A, segment.B)) < precision:
            return True
    return False


def point_egaux(point1, point2):
    """Arguments :
        - point1, point2 : objets de classe 'point'
    Retourne True si les points sont égaux à precision près
    False sinon"""
    if abs(point1.x - point2.x) < precision and\
            abs(point1.y - point2.y) < precision:
        return True
    return False


def intersection_segments(segment1, segment2):
    """Arguments :
        - segment1, segment2 : objets de classe 'segment'
    Retourne le point d'intersection des deux segments. None si les
    deux segments n'ont pas de point d'intersection. "Infinite" si ils en ont
    une infinité"""
    a = determinant_3_points(segment2.A, segment2.B, segment1.B)
    b = determinant_3_points(segment2.B, segment2.A, segment1.A)
    # Si tous les points sont alignés
    if a == 0 and b == 0:
        # Il y a une infinité de points d'intersection
        return 'Infinite'
    # Si un des segment est nul ou si les segments sont parallèles
    if a+b == 0:
        return None
    x = (a*segment1.A.x + b*segment1.B.x)/(a + b)
    y = (a*segment1.A.y + b*segment1.B.y)/(a + b)
    I = point_classe(x, y)
    # Si le point d'intersection appartient aux deux segments
    if point_appartient_segment(I, segment1) and\
            point_appartient_segment(I, segment2):
        # On retourne le point d'intersection trouvé
        return I
    return None

def angle_deux_points(A, O):
    """
    Arguments : 
        - A : objet de classe 'Point'
        - O : objet de classe 'Point'
    Retourne :
        - L'angle en radians entre le point A et la droite horizontale passant par O
    """
    angle = math.atan2(A.y - O.y, A.x - O.x)
    return angle

def intersection_demi_droite_segment(demi_droite, segment):
    """Arguments :
        - demi_droite, segment : objet de classe 'segment'
    Retourne le point d'intersection entre la demi_droite (définie par le
    premier point) et le segment. None si ils n'en ont pas."Infinite" si
    ils en ont une infinité"""
    a = determinant_3_points(demi_droite.A, demi_droite.B, segment.B)
    b = determinant_3_points(demi_droite.B, demi_droite.A, segment.A)
    # Si tous les points sont alignés
    if a == 0 and b == 0:
        # Il y a une infinité de points d'intersection
        return 'Infinite'
    # Si la demi-droite ou le segment est nul ou si ils sont parallèles
    if a+b == 0:
        return None
    x = (a*segment.A.x + b*segment.B.x)/(a + b)
    y = (a*segment.A.y + b*segment.B.y)/(a + b)
    I = point_classe(x, y)
    points_to_check = [demi_droite.A, demi_droite.B, segment.A, segment.B]
    # Vérifie que le point d'intersection trouvé est sur la droite
    if signe(a) != signe(b):
        equal = False
        # Cas où le point trouvé est un des points renseigné
        for point in points_to_check:
            if point_egaux(I, point):
                equal = True
        if not equal:
            return None
    # Vérifie que le point d'intersection se trouve sur la demi droite et non
    # la droite seulement
    if signe(I.y-demi_droite.A.y) != signe(demi_droite.B.y-demi_droite.A.y):
        if signe(I.y-demi_droite.A.y) != signe(demi_droite.B.y-demi_droite.A.y):
            return None
    # Vérifie si le point appartient au segment
    if point_appartient_segment(I, segment):
        return I
    return None

if __name__ == "__main__":
    print(type(point_classe(0, 0)))