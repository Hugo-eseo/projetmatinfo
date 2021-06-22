# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:48:30 2021

@author: Utilisateur
"""


import tkinter as tk
import random
from PIL import Image, ImageDraw
import numpy as np
import math
from shared import (point_classe, segment_classe, det2, determinant_3_points,
vabs, intersection_segments, vect, sc, angle_deux_points, rotation, dist)
from clipping import clip
from point_in_polygon import point_in_polygon_classes

def polygone_predefini(canvas, numero_predefini):
    """
    Arguments :
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera 
                   dessiné
        - numero_preset : integer definissant quel polygone sera dessiné,
                          si il est egal à None la dataset sera selectionée
                          aleatoirement
    Affiche :
        - Un polygone predefini en fonction du numero_predefini
    Retourne :
        - Une liste de tous les segments du polygone
        - Une liste des sommets du polygone
        - Une liste de listes representant la carte
    """

    database = [[(221, 183), (221, 221), (90, 223), (91, 109),
                (140, 106), (143, 168), (173, 168), (176, 70),
                (46, 65), (50, 276), (223, 274), (225, 321),
                (81, 330), (82, 403), (116, 400), (112, 359),
                (224, 357), (275, 356), (272, 317), (415, 315),
                (415, 277), (481, 272), (482, 316), (530, 315),
                (528, 225), (413, 227), (406, 162), (463, 158),
                (460, 116), (495, 111), (496, 65), (542, 64),
                (541, 21), (456, 21), (457, 81), (416, 81),
                (416, 120), (369, 122), (319, 123), (315, 63),
                (373, 57), (372, 23), (266, 22), (272, 122),
                (219, 124)]]

    if numero_predefini is None:
        numero_predefini = random.randint(0, len(database)-1)

    canvas.delete('all')

    transformed_database = list()
    for elem in database[numero_predefini]:
        transformed_database.append(point_classe(elem[0], elem[1]))

    # memorisation des segments
    liste_segments = list()
    for i in range(1, len(transformed_database)):
        A = transformed_database[i]
        B = transformed_database[i-1]
        liste_segments.append(segment_classe(A, B))
    A = transformed_database[0]
    B = transformed_database[-1]
    liste_segments.append(segment_classe(A, B))

    """
    # recuperer la matrice de la carte (temporaire)
    image = Image.new("RGB", (600, 400), color=(255,255,255))
    polygone = ImageDraw.Draw(image)
    polygone.polygon(database[numero_predefini], fill="black")
    carte = np.asarray(image.convert('L'))
    np.savetxt("P2/projetmatinfo/carte.txt", carte, fmt='%3d')

    # recuperer les sommets du polygone (temporaire)
    f = open('P2/projetmatinfo/sommets_polygone.txt','w')
    f.write(str(database[numero_predefini]))
    f.close()
    """
    for i in range(len(liste_segments)):
        canvas.create_line(liste_segments[i].A.x, liste_segments[i].A.y,
                           liste_segments[i].B.x, liste_segments[i].B.y,
                           fill="black", tag="segment")
    # dessiner le polygone
    
    return liste_segments

def projection_point_cercle(centre, A, rayon):
    """
    
    Arguments :
        - centre : Centre du cercle de type point_classe
        - A : Point extérieur au cercle que l'on veut projeter dessus, de type
              point_classe
        - rayon : Rayon du cercle en pixel

    Retourne
        - G1 ou G2 : L'intersection entre la droite passant par A et le centre
                     du cercle et le cercle lui-même. L'intersection la plus
                     proche de A est renvoyée

    """

    ASB = determinant_3_points(A, centre, centre)
    AB = dist(A, centre)
    d = vabs(ASB)/AB

    vAB = (centre.x-A.x, centre.y-A.y)
    vAS = (centre.x-A.x, centre.y-A.y)
    h = sc(vAS, vAB)/(AB**2)
    t = math.sqrt(rayon**2 - d**2)/AB

    #1er point d'intersection
    a = 1 - h - t
    b = h + t
    xG1 = (a*A.x+b*centre.x)
    yG1 = (a*A.y+b*centre.y)

    G1 = point_classe(xG1, yG1)
    d1 = dist(A, G1)

    #2eme point
    a = 1 - h + t
    b = h - t
    xG2 = (a*A.x+b*centre.x)
    yG2 = (a*A.y+b*centre.y)

    G2 = point_classe(xG2, yG2)
    d2 = dist(A, G2)
    """Comme le point est à l'extérieur du cercle, on prend l'intersection 
    avec la distance la plus faible"""
    if d1 > d2:
        return G2
    return G1

class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, identite):
        self.position = Point   # position en pixels
        self.direction = direction # en degrés
        self.angle = angle  # en degrés
        self.puissance = puissance    # puissance de la torche en pixels
        self.vitesse = vitesse  # vitesse de deplacement
        self.identite = identite # id d'un gardien, un nombre entier
        cnv.create_oval(self.position.x-3, self.position.y-3,
                        self.position.x+3, self.position.y+3,
                        tag="gardien"+str(self.identite),
                        fill="red")

    def move(self):
        pass
    
    def avancer(self, event, liste_segments, cnv):
        rad = self.direction * math.pi / 180
        self.position.move(math.sin(rad-math.pi/2) * self.vitesse,
                           math.cos(rad-math.pi/2) * self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(math.sin(rad-math.pi/2) * -self.vitesse,
                               math.cos(rad-math.pi/2) * -self.vitesse)
        else :
            cnv.move('gardien'+str(self.identite),
                     math.sin(rad-math.pi/2) * self.vitesse,
                     math.cos(rad-math.pi/2) * self.vitesse)
        self.eclaire()

    def reculer(self, event, liste_segments, cnv):
        rad = self.direction * math.pi / 180
        self.position.move(math.sin(rad-math.pi/2) * -self.vitesse,
                           math.cos(rad-math.pi/2) * -self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(math.sin(rad-math.pi/2) * self.vitesse,
                               math.cos(rad-math.pi/2) * self.vitesse)
        else :
            cnv.move('gardien'+str(self.identite),
                     math.sin(rad-math.pi/2) * -self.vitesse,
                     math.cos(rad-math.pi/2) * -self.vitesse)
        self.eclaire()

    def turn(self):
        pass

    def eclaire(self):
        cnv.delete("cone"+str(self.identite))
        cnv.delete("clip1"+str(self.identite))
        cnv.delete("clip2"+str(self.identite))
        cnv.delete("cercle")

        C = point_classe(self.position.x+self.puissance, self.position.y)
        C = rotation(self.position, C, self.direction)
        C1 = rotation(self.position, C, -self.angle)
        C2 = rotation(self.position, C, self.angle)

        #on veut l'intersection sur le cercle
        #projection 1
        proj1 = projection_point_cercle(self.position, C1, self.puissance)

        #projection 2
        proj2 = projection_point_cercle(self.position, C2, self.puissance)
        #Cone de lumière
        cnv.create_arc(self.position.x-self.puissance,
                       self.position.y-self.puissance, 
                       self.position.x+self.puissance,
                       self.position.y+self.puissance,
                       start=-angle_deux_points(proj1,
                                                self.position,True),
                       extent=2*self.angle,
                       tag="cone"+str(self.identite),
                       fill="yellow", outline="yellow")
        '''cnv.create_oval(self.position.x-self.puissance,
                        self.position.y-self.puissance, 
                        self.position.x+self.puissance,
                        self.position.y+self.puissance, tag="cercle")'''
        clip(cnv, proj1, proj2, self.position, self.puissance, liste_segments,
             self.identite)
        cnv.tag_raise("segment")

# parametres du jeu
width_canvas, height_canvas = 600, 400
width_frame, height_frame = 100, 400


# création de l'interface graphique
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=width_canvas, height=height_canvas, bg="white")
cnv.pack(side=tk.LEFT)
frm = tk.Frame(wnd, width=width_frame, height=height_frame)
frm.pack(side=tk.RIGHT)
liste_segments = polygone_predefini(cnv, 0)
gardien1 = Gardien(point_classe(300, 250), 180, 30, 100, 2, 1)
gardien1.eclaire()

wnd.bind("<Up>", lambda event : gardien1.avancer(event, liste_segments, cnv))
wnd.bind("<Down>", lambda event : gardien1.reculer(event, liste_segments, cnv))

wnd.mainloop()