# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:21:25 2021

@author: hugob
"""
import math

# Taille des point affichés sur le canvas
size = 4
# Présion demandée la validation des calculs
precision = 0.01


class point_classe():
    """Docstring"""

    def __init__(self, x, y):
        """Prend en argument les coordonées x et y du point"""
        self.x, self.y = x, y

    def __str__(self):
        string = "(" + str(self.x) + "," + str(self.y) + ")"
        return string

    def return_tuple(self):
        return (self.x, self.y)


class segment_classe():
    """Docstring"""

    def __init__(self, point1, point2):
        """Prend en argument deux points (de classe 'point')
        définissants un segment"""
        self.A, self.B = point1, point2

    def __str__(self):
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


def point_in_polygon(point_to_check, polygon, canvas, mode_demo=False):
    """Arguments :
        - point_to_check : Tuple ou liste sous la forme (x, y) ou [x, y]
        - polygon : Liste de sommets sous la forme [[xA, yA], [xB, yB] ...]
        - canvas : Canvas de dessin
        - mode_demo : Boolean, True pour activer le mode de démonstration
    Retourne True si 'point_to_check' se trouve à l'intérieur de
    'polygon'. False sinon (segments et sommets du polygon sont considérés
    comme à l'extérieur')
    Retourne None en cas d'erreur"""

    # Vérifications élémentaires
    if not (type(point_to_check) == tuple or type(point_to_check) == list):
        return None
    if not (len(point_to_check) == 2):
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
    O = point_classe(point_to_check[0], point_to_check[1])

    # Cette fonction se base sur l'algorithme présenté sur cet article
    # https://towardsdatascience.com/is-the-point-inside-the-polygon-574b86472119

    # Winding number
    wn = 0
    # A et B : points définissants le segment horizontal de référence
    # Possèdent la même hauteur que O
    A = point_classe(0, O.y)
    B = point_classe(width, O.y)
    segment_horizontal = segment_classe(A, B)

    if mode_demo:
        canvas.create_oval(O.x-size, O.y-size, O.x+size, O.y+size,
                           fill='green', tag='demo')
        canvas.create_line((0, O.y), (width, O.y), fill='red', tag='demo')

    # Liste contenant les coordonnées des points d'intersections de la droite
    # horizontale avec les segments du polygon
    liste_intersections = list()

    # On parcours la liste des segments du polygon
    for segment in liste_segments_polygon:
        # Si le point appartien à un segment du polygon, il n'appartient
        # donc pas dans polygon
        if point_appartient_segment(O, segment):
            return False
        I = intersection_segments(segment_horizontal, segment)

        # Différents cas possibles

        # Si les deux segments sont alignés
        if I == "Infinite":
            # On considère les deux extrémités du segments comme deux
            # points d'intersection
            liste_intersections.append([segment.A, segment])
            liste_intersections.append([segment.B, segment])

        # Si un point d'intersection a été trouvé
        elif I is not None:
            liste_intersections.append([I, segment])
    # Un fois toutes les intersections trouvés, on les passe en revue une
    # par une
    i = 0
    while i < len(liste_intersections):
        intersection = liste_intersections[i][0]
        # Vecteur directeur du segment où se trouve l'intersection
        # Par similitude, on se permet de l'assimiler à une classe point
        u = point_classe(liste_intersections[i][1].B.x -
                         liste_intersections[i][1].A.x,
                         liste_intersections[i][1].B.y -
                         liste_intersections[i][1].A.y)
        # Dans le cas de la dernière intersection, il faut vérifier avec
        # la première
        if i == len(liste_intersections)-1:
            indice = 0
        else:
            indice = i+1
        ignore = False
        # Si l'intersection est un sommet
        if point_egaux(intersection, liste_intersections[indice][0]):
            if mode_demo:
                canvas.create_oval(intersection.x-size, intersection.y-size,
                                   intersection.x+size, intersection.y+size,
                                   fill='blue', tag='demo')
            v = point_classe(liste_intersections[indice][1].B.x -
                             liste_intersections[indice][1].A.x,
                             liste_intersections[indice][1].B.y -
                             liste_intersections[indice][1].A.y)
            # Si l'intersection n'est pas une entrée ou sortie du polygone
            # (une pointe par exemple), elle doit être ignoré
            # Les deux premiers if sont les cas où l'un des segments est
            # horizontal
            if signe(u.y) == 0:
                if signe(v.y) == 0 or signe(v.y) == 1:
                    ignore = True
            elif signe(v.y) == 0:
                if signe(u.y) == -1:
                    ignore = True
            elif signe(v.y) != signe(u.y):
                ignore = True
            # Dans tous les cas, on ignore l'indice suivant (étant une nouvelle
            # fois le sommet)
            i += 1
            # Si on est rendu au dernier indice, on quitte la boucle
            if i == len(liste_intersections):
                continue
        elif mode_demo:
            canvas.create_oval(intersection.x-size, intersection.y-size,
                               intersection.x+size, intersection.y+size,
                               fill='red', tag='demo')
        # Si l'intersection ne doit pas être ignorée
        result = 0
        if not ignore:
            # On met à jour le winding number
            if u.y < 1:
                # Croisement vers le haut
                if intersection.x > O.x:
                    wn += 1
                    result = 1
            else:
                # Croisement vers le bas
                if intersection.x > O.x:
                    wn -= 1
                    result = -1
        canvas.create_text(intersection.x, intersection.y+10, text=result,
                           tag='demo')
        i += 1
    if wn != 0:
        return True
    return False
