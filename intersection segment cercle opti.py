# -*- coding: utf-8 -*-
"""
Created on Mon May  3 10:20:16 2021

@author: hugof
"""

import tkinter as tk
from shared import (point_classe, segment_classe, det2, determinant_3_points,
vabs, intersection_segments, vect, sc, angle_deux_points, rotation, dist,
point_appartient_segment)
import math

precision = 0.01

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

class Application():
    
    def __init__(self, centre, rayon, nb_seg, angle):
        """
    
        Arguments :
            - centre : Centre du cercle de type point_classe
            - rayon : Rayon du cercle en pixel
            - nb_seg : Nombre de segments maximums que l'utilisateur peut poser
            - angle : Angle de la projection 

        """

        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=600, height=400, bg="lightgrey")
        self.cnv.pack()

        self.S = centre
        self.C = point_classe(300, 100)
        self.rayon = rayon
        self.nb_seg = nb_seg
        self.seg_actuel = 0
        self.angle_cone = angle
        self.arrondi_segment = 2
        self.arrondi_angle = 4
        
        self.seg_list = list()
        self.A = list()
        self.B = list()
        self.angle_A = list()
        self.angle_B = list()
        self.clip = list()
        self.inter1 = list()
        self.inter2 = list()
        self.angle_inter1 = list()
        self.angle_inter2 = list()
        for i in range(self.nb_seg):
            self.seg_list.append(None)
            self.A.append(None)
            self.B.append(None)
            self.clip.append(None)
            self.inter1.append(None)
            self.inter2.append(None)
            self.angle_inter1.append(None)
            self.angle_inter2.append(None)
            self.angle_A.append(None)
            self.angle_B.append(None)
        #Affichage du cercle et de son centre
        self.cnv.create_oval(self.S.x-self.rayon, self.S.y-self.rayon,
                             self.S.x+self.rayon, self.S.y+self.rayon)
        self.cnv.create_oval(self.S.x-3, self.S.y-3, self.S.x+3, self.S.y+3)
        #Affichage du cone, orienté vers le haut par défaut
        self.affichage_cone(None)
        '''Boutons affichant les intersections entre la droite AB du segment
        actuellement selectionné et celui du clipping'''
        tk.Button(self.wnd, text="afficher intersections",
                  command=self.affichage_intersections).pack()
        tk.Button(self.wnd, text="clipping", command=self.clipping).pack()
        #Boutons permettant de changer de segment actuellement sélectionné
        self.seg_choisi_bouton = tk.Button(self.wnd,
                                           text="Segment "+str(self.seg_actuel)
                                           ,command=self.seg_changement)
        self.seg_choisi_bouton.pack()
        #Clic gauche: choix du point A pour le segment sélectionné
        #Clic droit : choix du point B pour le segment sélectionné
        #Clic molette : choix de l'orientation de la projection
        self.cnv.bind("<1>", self.input_A)
        self.cnv.bind("<3>", self.input_B)
        self.cnv.bind("<Button-2>", self.affichage_cone)

        self.wnd.mainloop()

    def input_A(self, event):
        """

        Associe le point A du segment actuellement sélectionné à l'endroit du 
        clic

        Arguments :
            - event : évenement, permet de récupérer la position de la souris
    
        """
        
        self.A[self.seg_actuel] = point_classe(event.x, event.y)
        self.cnv.delete("pointA"+str(self.seg_actuel),
                        "segAB"+str(self.seg_actuel))
        #Si B est défini pour le segment actuellement utilisé, tracé du segment
        if self.B[self.seg_actuel] is not None:
            self.cnv.create_line(self.A[self.seg_actuel].return_tuple(),
                                 self.B[self.seg_actuel].return_tuple(),
                                 tag="segAB"+str(self.seg_actuel))
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3,
                             fill="orange", tag="pointA"+str(self.seg_actuel))

    def input_B(self, event):
        """

        Associe le point B du segment actuellement sélectionné à l'endroit du 
        clic

        Arguments :
            - event : évenement, permet de récupérer la position de la souris
    
        """
        
        self.B[self.seg_actuel] = point_classe(event.x, event.y)
        self.cnv.delete("pointB"+str(self.seg_actuel),
                        "segAB"+str(self.seg_actuel))
        #Si A est défini pour le segment actuellement utilisé, tracé du segment
        if self.A[self.seg_actuel] is not None:
            self.cnv.create_line(self.A[self.seg_actuel].return_tuple(),
                                 self.B[self.seg_actuel].return_tuple(),
                                 tag="segAB"+str(self.seg_actuel))
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3,
                             fill="orange", tag="pointB"+str(self.seg_actuel))

    def seg_changement(self):
        """
        Changement du segment actuellement sélectionné par l'utilisateur
    
        """
        self.seg_actuel += 1
        if self.seg_actuel == self.nb_seg:
            self.seg_actuel = 0
        #Mise à jour du texte du bouton
        self.seg_choisi_bouton["text"] = "Segment "+str(self.seg_actuel)

    def calcul_intersections(self, seg):
        """
        Renvoie les deux intersections entre la droite donnée par les points
        du segment seg et le cercle sous forme d'objet point_classe
        
        Arguments :
            - event : évenement, permet de récupérer la position de la souris
        
        Retourne
            - G1 et G2 : Intersections entre la droite correspondant au segment
                         et le cercle. G1 et G2 objets de type point_classe
            - (None, None) : Si il n'y a pas de points d'intersections entre
                             la droite et le cercle

        """

        ASB = determinant_3_points(self.A[seg], self.S, self.B[seg])
        AB = dist(self.A[seg], self.B[seg])
        d = vabs(ASB)/AB
        '''d étant la distance la plus proche entre le cercle et la droite AB
        si d est inférieure au rayon, il n'y a pas d'intersections possible'''
        if d < self.rayon:
            #Calcul à l'aide de la formule prouvée 
            vAB = (self.B[seg].x-self.A[seg].x, self.B[seg].y-self.A[seg].y)
            vAS = (self.S.x-self.A[seg].x, self.S.y-self.A[seg].y)
            h = sc(vAS, vAB)/(AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB

            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG1 = (a*self.A[seg].x+b*self.B[seg].x)
            yAG1 = (a*self.A[seg].y+b*self.B[seg].y)

            #2eme point
            a = 1 - h + t
            b = h - t
            xAG2 = (a*self.A[seg].x+b*self.B[seg].x)
            yAG2 = (a*self.A[seg].y+b*self.B[seg].y)

            return point_classe(xAG1, yAG1), point_classe(xAG2, yAG2)
        return None, None
    def affichage_intersections(self):
        """
        
        Affichage des deux intersections entre la droite correspondant au
        segment sélectionné et le cercle
        
        """
        if self.A[self.seg_actuel] is not None \
            and self.B[self.seg_actuel] is not None:
            #Calcul de d
            ASB = determinant_3_points(self.A[self.seg_actuel],
                                      self.S, self.B[self.seg_actuel])
            AB = dist(self.A[self.seg_actuel], self.B[self.seg_actuel])
            d = vabs(ASB)/AB
            if d < self.rayon:
                self.cnv.delete("inter")
                vAB = (self.B[self.seg_actuel].x-self.A[self.seg_actuel].x,
                       self.B[self.seg_actuel].y-self.A[self.seg_actuel].y)
                vAS = (self.S.x-self.A[self.seg_actuel].x,
                       self.S.y-self.A[self.seg_actuel].y)
                h = sc(vAS, vAB)/(AB**2)
                t = math.sqrt(self.rayon**2 - d**2)/AB
    
                #Affichage point H
                a = 1 - h
                b = h
                xAG = (a*self.A[self.seg_actuel].x+b*self.B[self.seg_actuel].x)
                yAG = (a*self.A[self.seg_actuel].y+b*self.B[self.seg_actuel].y)
                self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="green",
                                     tag="inter")
                
                #1er point d'intersection
                a = 1 - h - t
                b = h + t
                xAG = (a*self.A[self.seg_actuel].x+b*self.B[self.seg_actuel].x)
                yAG = (a*self.A[self.seg_actuel].y+b*self.B[self.seg_actuel].y)
                
                self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red",
                                     tag="inter")
                
                #2eme point
                a = 1 - h + t
                b = h - t
                xAG = (a*self.A[self.seg_actuel].x+b*self.B[self.seg_actuel].x)
                yAG = (a*self.A[self.seg_actuel].y+b*self.B[self.seg_actuel].y)
                
                self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red",
                                     tag="inter")

    def clipping(self):
        """

        Clipping: on efface la partie du cercle à effacer, puis en retrace le
        triangle correspondant à la partie lumineuse devant être affichée
        (role de clipSeg), puis on affiche de nouveau le cercle et les segments
        afin que l'utilisateur puisse les voir. Note : cette version du
        clipping n'est pas faite pour des segments qui se croisent, elle est
        destinée à être utilisée dans le cadre d'une galerie d'art dans
        laquelle les murs ne se croisent pas.

        """
        self.clipSeg()
        self.cnv.delete("cercle")
        self.cnv.create_oval(self.S.x-self.rayon, self.S.y-self.rayon,
                             self.S.x+self.rayon, self.S.y+self.rayon)
        for i in range(self.nb_seg):
            if self.A[i] is not None and self.B[i] is not None:
                self.cnv.delete("segAB"+str(i))
                self.cnv.create_line(self.A[i].return_tuple(),
                                     self.B[i].return_tuple(),
                                     tag="segAB"+str(i))
                self.cnv.delete("pointA"+str(i))
                self.cnv.create_oval(self.A[i].x-3,
                                     self.A[i].y-3,
                                     self.A[i].x+3,
                                     self.A[i].y+3,
                                     fill="orange", tag="pointA"+str(i))
                self.cnv.delete("pointB"+str(i))
                self.cnv.create_oval(self.B[i].x-3,
                                     self.B[i].y-3,
                                     self.B[i].x+3,
                                     self.B[i].y+3,
                                     fill="orange", tag="pointB"+str(i))

    def affichage_cone(self, event):
        """

        Affiche le cone de lumière (sans clipping) projeté par la lampe.

        Arguments :
            - event : évenement, permet de récupérer la position de la souris

        """

        #On supprime les cone et les effets de clipping
        self.cnv.delete("cone")
        self.cnv.delete("clip1")
        self.cnv.delete("clip2")

        if event is not None:
            C = point_classe(event.x, event.y)
        else:
            C = self.C
        C1 = rotation(self.S, C, -self.angle_cone)
        C2 = rotation(self.S, C, self.angle_cone)

        #on veut l'intersection sur le cercle
        #projection 1
        self.proj1 = projection_point_cercle(self.S, C1, self.rayon)

        #projection 2
        self.proj2 = projection_point_cercle(self.S, C2, self.rayon)
        print("proj1: ", self.proj1)
        #Cone de lumière
        self.cnv.create_arc(self.S.x-self.rayon, self.S.y-self.rayon, 
                            self.S.x+self.rayon, self.S.y+self.rayon,
                            start=-angle_deux_points(self.proj1,self.S,True),
                            extent=2*self.angle_cone,
                            tag="cone", fill="yellow", outline="yellow")

    def clipSeg(self):
        """

        Efface la partie à effacer lors du clipping et affiche le triangle de
        lumière à afficher par dessus

        """

        #Suppression des effets de clipping déjà existants
        self.cnv.delete("clip1")
        self.cnv.delete("clip2")
        self.cnv.delete("point")
        
        #Récupération des angles correspondants aux extrémités de la projection
        #lumineuse
        self.angle_proj1 = -angle_deux_points(self.proj1, self.S, True)
        self.angle_proj2 = -angle_deux_points(self.proj2, self.S, True)

        #Tri des angles dans le bon ordre -> angle_proj1 doit être le premier
        if self.angle_proj1 < 0:
            self.angle_proj1 += 360

        if self.angle_proj2 < 0:
            self.angle_proj2 += 360
        
        #Écart des angles de la projection lumineuse, si il est supérieur à 180
        #alors c'est que la projection passe par la limite 360 - 0 degré, on se
        #servira de cette information plus tard
        self.ecart_proj = vabs(self.angle_proj2 - self.angle_proj1)

        #Tri des segments : on trie les segments à clipper en premier en
        #fonction de la distance entre le centre du cercle et le milieu du
        #segment. Note: cette méthode n'est pas optimale, elle ne fonctionne
        #pas tout le temps mais c'est la plus efficace que nous avons trouvée
        milieu_list = list()
        for i in range(self.nb_seg):
            if self.A[i] is not None and self.B[i] is not None:
                milieu_list.append(dist(point_classe((self.A[i].x\
                                                      +self.B[i].x)/2,
                                        (self.A[i].y+self.B[i].y)/2), self.S))
            else:
                #si le segment n'est pas défini, on lui donne une valeur, afin
                #de ne pas avoir de problème
                milieu_list.append(100000)

        milieu_non_trie = True

        while milieu_non_trie:
            changement = False
            for i in range(self.nb_seg-1):
                if milieu_list[i] < milieu_list[i+1]:
                    milieu_list[i], milieu_list[i+1] = \
                        milieu_list[i+1], milieu_list[i]
                    self.A[i], self.A[i+1] = self.A[i+1], self.A[i]
                    self.B[i], self.B[i+1] = self.B[i+1], self.B[i]
                    changement = True
            if changement == False:
                milieu_non_trie = False
        
        #Début du clipping dans le bon ordre pour tous les segments
        for i in range(self.nb_seg):
            if self.A[i] is not None and self.B[i] is not None:
                #On calcule AS et BS correspondant aux distances entre A et le
                #centre du cercle et B et le centre du cercle
                AS = dist(self.A[i], self.S)
                BS = dist(self.B[i], self.S)
                #On définit les segments seg21 et seg22 correspondant aux
                #segments entre le centre du cercle et les extrémités de la
                #projection lumineuse
                seg21 = segment_classe(self.proj1, self.S)
                seg22 = segment_classe(self.proj2, self.S)
                #On récupère les angles correspondants aux points A et B
                self.angle_A[i] = -angle_deux_points(self.A[i], self.S, True)
                self.angle_B[i] = -angle_deux_points(self.B[i], self.S, True)

                if self.angle_A[i] < 0:
                    self.angle_A[i] += 360
                    
                if self.angle_B[i] < 0:
                    self.angle_B[i] += 360
                #On trie A et B afin que A soit placé avant B dans la rotation
                #autour du cercle. C'est-à-dire que lorsque l'on tourne dans le
                #sens trigonométrique, on verra toujours A avant B
                if self.angle_A[i] > self.angle_B[i]:
                    self.A[i], self.B[i] = self.B[i], self.A[i]
                    self.angle_A[i], self.angle_B[i] = \
                        self.angle_B[i], self.angle_A[i]
                    AS, BS = BS, AS
                #On récupère l'écart en degré entre les angles de A et B, afin
                #de savoir si l'on doit les inverser (on les inverse si passe
                #par la limite 360 - 0 degrés)
                ecart_AB = vabs(self.angle_B[i] - self.angle_A[i])
                if ecart_AB >= 180:
                    self.angle_A[i], self.angle_B[i] = \
                        self.angle_B[i], self.angle_A[i]
                    self.A[i], self.B[i] = self.B[i], self.A[i]
                    AS, BS = BS, AS

                #On récupère les intersections entre la droite AB et le cercle
                #s'il n'y en a pas alors la droite AB ne passe pas par le
                #cercle et par conséquent le segment AB non plus, s'il n'y en
                #a pas alors pas besoin de faire le clipping.
                self.inter1[i], self.inter2[i] = self.calcul_intersections(i)
                if self.inter1[i] is not None:
                    #On récupère les angles correspondant aux intersections
                    #entre la droite AB et le cercle, puis on les trie de
                    #la même manière que pour A et B
                    self.angle_inter1[i] = \
                        -angle_deux_points(self.inter1[i], self.S, True)
                    if self.angle_inter1[i] < 0:
                        self.angle_inter1[i] += 360

                    self.angle_inter2[i] = \
                        -angle_deux_points(self.inter2[i], self.S, True)
                    if self.angle_inter2[i] < 0:
                        self.angle_inter2[i] += 360

                    if self.angle_inter1[i] > self.angle_inter2[i]:
                        self.inter1[i], self.inter2[i] = self.inter2[i], \
                            self.inter1[i]
                        self.angle_inter1[i], self.angle_inter2[i] = \
                            self.angle_inter2[i], self.angle_inter1[i]
                    
                    #On récupère l'écart entre les angles de chaque
                    #intersections, si l'écart est supérieur à 180 alors
                    #l'écart des angles passe par la limite 360 - 0 degré, on
                    #inverse alors inter1 et inter2 dans ce cas
                    self.ecart = \
                        vabs(self.angle_inter2[i] - self.angle_inter1[i])
                    if self.ecart >= 180:
                        self.angle_inter2[i], self.angle_inter1[i] = \
                            self.angle_inter1[i], self.angle_inter2[i]
                        self.inter1[i], self.inter2[i] = \
                            self.inter2[i], self.inter1[i]
                    segAB = segment_classe(self.A[i], self.B[i])
                    
                    #On teste s'il faut clip : il faut que soit le segment AB
                    #soit dans le cercle (condition 1)
                    #ou alors il faut que le segment AB passe par le cercle:
                    #on regarde les intersections, si elles existent alors on
                    #on vérifie qu'elles passent bien par la cone de lumière
                    if BS < self.rayon or AS < self.rayon\
                        or (BS > self.rayon and AS > self.rayon\
                        and (self.angle_inter2[i] < self.angle_proj2 \
                        or self.angle_inter1[i] > self.angle_proj1)\
                        and (point_appartient_segment(self.inter1[i],segAB)\
                        or point_appartient_segment(self.inter2[i],segAB))) \
                        or (BS > self.rayon and AS > self.rayon \
                        and self.ecart_proj > 180 \
                        and ((self.angle_inter1[i] < self.angle_proj2\
                        and point_appartient_segment(self.inter1[i], segAB))\
                        or (self.angle_inter2[i] > self.angle_proj1\
                        and point_appartient_segment(self.inter2[i], segAB)))):

                        clip = True

                        #Malgré la condition précédente, par test, on a
                        #remarqué que dans certains cas, le clipping se
                        #produisait quand même. L'étape suivante a donc été
                        #faite par tâtonnement et n'est donc surement pas
                        #optimisée. Ce qui n'a pas été fait par manque de temps
                        #Tous les tests suivants visent à annuler le clipping
                        #quand nécessaire.
                        if vabs(BS-self.rayon) <= self.arrondi_segment \
                            and AS > self.rayon \
                            and intersection_segments(seg21, segAB) is None \
                            and intersection_segments(seg22, segAB) is None\
                            and self.angle_inter1[i] < self.angle_proj1\
                            and self.angle_inter2[i] > self.angle_proj2:

                            clip = False
                        if vabs(AS-self.rayon) <= self.arrondi_segment \
                            and BS > self.rayon \
                            and intersection_segments(seg22, segAB) is None \
                            and intersection_segments(seg21, segAB) is None\
                            and self.angle_inter1[i] < self.angle_proj1\
                            and self.angle_inter2[i] > self.angle_proj2:

                            clip = False

                        if self.ecart_proj < 180 \
                            and intersection_segments(seg21, segAB) is None \
                            and intersection_segments(seg22, segAB) is None\
                            and self.ecart < 180\
                            and self.angle_inter1[i] > self.angle_proj2\
                            and self.angle_inter2[i] > self.angle_proj2:

                            clip = False
                        if self.ecart_proj > 180 \
                            and self.angle_inter2[i] < self.angle_proj1 \
                            and self.angle_inter1[i] > self.angle_proj2 \
                            and BS > self.rayon and self.ecart < 180 \
                            and self.angle_A[i] < self.angle_proj1:

                            clip = False

                        if self.ecart_proj < 180 \
                            and self.angle_B[i] > self.angle_proj1 \
                            and self.angle_A[i] > self.angle_proj2 \
                            and ecart_AB > 180 \
                            and self.angle_inter2[i] < self.angle_proj1\
                            and self.angle_inter1[i] > self.angle_proj2:

                            clip = False

                        if self.ecart_proj < 180 \
                            and self.angle_B[i] < self.angle_proj1 \
                            and self.angle_A[i] < self.angle_proj2 \
                            and ecart_AB > 180 \
                            and self.angle_inter2[i] < self.angle_proj1\
                            and self.angle_inter1[i] > self.angle_proj2:

                            clip = False

                        if self.ecart_proj < 180 \
                            and self.angle_B[i] > self.angle_proj2 \
                            and self.angle_A[i] < self.angle_proj2 \
                            and ecart_AB < 180 \
                            and self.angle_inter2[i] < self.angle_proj1\
                            and self.angle_inter1[i] > self.angle_proj2:

                            clip = False

                        if self.ecart_proj < 180 \
                            and self.angle_B[i] > self.angle_proj1 \
                            and self.angle_A[i] < self.angle_proj1 \
                            and ecart_AB < 180 \
                            and self.angle_inter2[i] < self.angle_proj1\
                            and self.angle_inter1[i] > self.angle_proj2:

                            clip = False

                        #Lorsque le clipping doit être fait, comme AB est un
                        #segment, il ne fait pas effacer plus que le nécessaire
                        #les conditions suivantes modifient les valeurs de
                        #inter1 et inter2 afin que la plus petite partie
                        #possible ne soit effacée
                        if self.ecart_proj < 180 and self.ecart < 180:
                            #Lorsqu'il n'y a pas de problèmes aux niveau de la
                            #limite 180-0 degré alors si B est contenu dans la
                            #projection lumineuse, on remplace inter2 par B
                            if self.angle_B[i] < self.angle_proj2 \
                                and self.angle_B[i] < self.angle_inter2[i] \
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            #De même avec A, si A est dans la projection
                            #lumineuse, on remplace inter1 par A
                            if self.angle_A[i] > self.angle_proj1 \
                                and self.angle_A[i] > self.angle_inter1[i] \
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]
                        #Les conditions suivantes sont basées sur le même
                        #objectif, si A ou B est contenu dans la projection
                        #lumineuse, on remplace inter1 et/ou inter2 par
                        #A et/ou inter2.
                        elif self.ecart_proj < 180 and self.ecart >= 180:
                            if self.angle_B[i] < self.angle_proj2 \
                                and self.angle_B[i] < self.angle_inter2[i] \
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            if self.angle_B[i] < self.angle_proj2 \
                                and self.angle_B[i] > self.angle_inter2[i] \
                                and self.angle_inter2[i] < self.angle_proj1\
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            if self.angle_A[i] > self.angle_proj1 \
                                and self.angle_A[i] > self.angle_inter1[i] \
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                            if self.angle_A[i] > self.angle_proj1 \
                                and self.angle_A[i] < self.angle_inter1[i] \
                                and self.angle_inter1[i] > self.angle_proj2\
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                        if self.ecart_proj >= 180 and self.ecart < 180:
                            if self.angle_B[i] < self.angle_inter2[i] \
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            if self.angle_A[i] > self.angle_proj1 \
                                and self.angle_A[i] > self.angle_inter1[i] \
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                            if self.angle_A[i] < self.angle_proj2 \
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                        if self.ecart_proj >= 180 and self.ecart >=180:
                            if self.angle_B[i] < self.angle_proj2 \
                                and self.angle_B[i] < self.angle_inter2[i] \
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            if self.angle_B[i] > self.angle_proj2 \
                                and self.angle_B[i] > self.angle_inter2[i] \
                                and self.angle_B[i] > self.angle_proj1\
                                and BS < self.rayon:

                                self.inter2[i] = self.B[i]
                                self.angle_inter2[i] = self.angle_B[i]

                            if self.angle_A[i] > self.angle_proj1 \
                                and self.angle_A[i] > self.angle_inter1[i] \
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                            if self.angle_A[i] < self.angle_proj1 \
                                and self.angle_A[i] < self.angle_inter1[i] \
                                and self.angle_A[i] < self.angle_proj2\
                                and AS < self.rayon:

                                self.inter1[i] = self.A[i]
                                self.angle_inter1[i] = self.angle_A[i]

                        #Comme précédemment, par test, on a
                        #remarqué que dans certains cas, le clipping se
                        #produisait quand même. L'étape suivante a donc été
                        #aussi faite par tâtonnement et n'est donc pas
                        #optimisée. Ce qui n'a pas été fait par manque de temps
                        #Tous les tests suivants visent à annuler le clipping
                        #quand nécessaire.
                        if self.ecart_proj < 180 \
                            and self.angle_B[i] < self.angle_proj1 \
                            and self.angle_A[i] < self.angle_proj1 \
                            and ecart_AB < 180:

                            clip = False
                        if self.ecart_proj < 180 \
                            and self.angle_B[i] > self.angle_proj2 \
                            and self.angle_A[i] > self.angle_proj2 \
                            and ecart_AB < 180:

                            clip = False
                        if self.ecart_proj < 180 \
                            and self.angle_B[i] < self.angle_proj1 \
                            and self.angle_A[i] > self.angle_proj2 \
                            and ecart_AB > 180:

                            clip = False
                        if self.ecart_proj > 180 \
                            and self.angle_B[i] > self.angle_proj2 \
                            and self.angle_A[i] > self.angle_proj2 \
                            and ecart_AB < 180\
                            and self.angle_B[i] < self.angle_proj1:

                            clip = False

                        if self.ecart_proj < 180 \
                            and self.angle_inter1[i] < self.angle_proj1 \
                            and self.angle_inter2[i] < self.angle_proj1 \
                            and self.ecart < 180:

                            clip = False

                        if vabs(self.angle_A[i]-self.angle_B[i])\
                            <= self.arrondi_angle \
                            and self.angle_A[i]:

                            clip = False

                        #Quand tous les tests du clipping on été validé,
                        #on cherche s'il y a une intersection entre le segment
                        #correspondant à celui créé par inter1 et inter2 et un
                        #des segments correspondant aux extrêmités des
                        #projections du cône de lumière
                        if clip:
                            seg1 = segment_classe(self.inter1[i],
                                                  self.inter2[i])

                            int1p = intersection_segments(seg1, seg21)
                            int2p = intersection_segments(seg1, seg22)

                            #Si les intersections ne sont pas comprisent dans
                            #la projection lumineuse, on les projette sur un
                            #des segments extrêmes de la projection
                            #lumineuse. Toutes les conditions suivantes ont
                            #cet objectif
                            if self.ecart_proj < 180 and self.ecart < 180:
                                if self.angle_proj1 > self.angle_inter1[i] \
                                    and int1p is not None:

                                    self.angle_inter1[i] = self.angle_proj1
                                    self.inter1[i] = int1p

                                if self.angle_proj2 < self.angle_inter2[i] \
                                    and int2p is not None:

                                    self.angle_inter2[i] = self.angle_proj2
                                    self.inter2[i] = int2p

                            if self.ecart_proj < 180 and self.ecart >= 180:
                                if self.angle_proj1 > self.angle_inter1[i] \
                                    and self.angle_inter1[i] < \
                                    self.angle_proj2 and int1p is not None:

                                    self.angle_inter1[i] = self.angle_proj1
                                    self.inter1[i] = int1p

                                if self.angle_proj1 < self.angle_inter1[i] \
                                    and self.angle_inter1[i] > \
                                    self.angle_proj2 and int1p is not None:

                                    self.angle_inter1[i] = self.angle_proj1
                                    self.inter1[i] = int1p

                                if self.angle_proj2 < self.angle_inter2[i] \
                                    and self.angle_inter2[i] > \
                                    self.angle_proj1 and int2p is not None:

                                    self.angle_inter2[i] = self.angle_proj2
                                    self.inter2[i] = int2p

                                if self.angle_proj2 > self.angle_inter2[i] \
                                    and self.angle_inter2[i] < \
                                    self.angle_proj1 and int2p is not None:

                                    self.angle_inter2[i] = self.angle_proj2
                                    self.inter2[i] = int2p

                            if self.ecart_proj > 180 and self.ecart < 180:
                                if self.angle_proj2 < self.angle_inter2[i] \
                                    and self.angle_inter2[i] < \
                                    self.angle_proj1 and int2p is not None:

                                    self.angle_inter2[i] = self.angle_proj2
                                    self.inter2[i] = int2p

                                if self.angle_proj1 > self.angle_inter1[i] \
                                    and self.angle_inter1[i] > \
                                    self.angle_proj2 and int1p is not None:

                                    self.angle_inter1[i] = self.angle_proj1
                                    self.inter1[i] = int1p

                            if self.ecart_proj > 180 and self.ecart > 180:
                                if self.angle_proj1 > self.angle_inter1[i] \
                                    and self.angle_inter1[i] > \
                                    self.angle_proj2 and int1p is not None:

                                    self.angle_inter1[i] = self.angle_proj1
                                    self.inter1[i] = int1p

                                if self.angle_proj2 < self.angle_inter2[i] \
                                    and self.angle_inter2[i] < \
                                    self.angle_proj1 and int2p is not None:

                                    self.angle_inter2[i] = self.angle_proj2
                                    self.inter2[i] = int2p

                            #Afin d'effacer une partie de l'arc lumineux, on
                            #doit connaitre, l'angle de départ et un angle à
                            #effacer à partir du départ. On calcule diff,
                            #l'angle à effacer à partir du départ: celui de
                            #inter1
                            diff = vabs(self.angle_inter2[i] - \
                                        self.angle_inter1[i])

                            if diff >= 180:
                                diff = vabs(360 - self.angle_inter1[i] \
                                            + self.angle_inter2[i])
                            if diff >= 1:
                                #Afin d'éviter des problèmes, si l'angle est
                                #plus petit que 1, pas besoin de faire le
                                #clipping, on ne le verrait pas à l'oeil nu
                                #Ensuite, on efface l'arc à effacer et on
                                #trace le polygone à afficher par dessus.
                                self.cnv.create_arc(self.S.x-self.rayon,
                                                    self.S.y-self.rayon,
                                                    self.S.x+self.rayon,
                                                    self.S.y+self.rayon,
                                                    fill="lightgrey",
                                                    tag="clip1",
                                                    start=self.angle_inter1[i],
                                                    extent=diff,
                                                    outline="lightgrey")
    
                                self.cnv.create_polygon(self.S.return_tuple(),
                                                        self.inter1[i]\
                                                            .return_tuple(),
                                                        self.inter2[i]\
                                                            .return_tuple(),
                                                        fill="yellow",
                                                        outline="yellow",
                                                        tag="clip2")

Application(point_classe(300, 200), 150, 3, 40)