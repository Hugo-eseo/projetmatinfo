# -*- coding: utf-8 -*-
# @author : ArthurM 

from shared import classe_point

def rotation(O, M, angle):
    """
    Arguments :
        - O : objet de classe 'Point' 
        - M : objet de classe 'Point'
        - angle : angle donné en degrés
    Retourne :
        - Un objet de classe 'Point' étant la rotation du point M autour du centre O et d'angle 'angle'
    """
    
    # Angle converti en radian
    angle = angle * math.pi / 180
    # calcul de la rotation
    xM = M.x - O.x
    yM = M.y - O.y
    x = xM*math.cos(angle) + yM*math.sin(angle) + O.x
    y = - xM*math.sin(angle) + yM*math.cos(angle) + O.y
    return classe_point(x, y)