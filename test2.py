# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:37:50 2021

@author: Utilisateur
"""

import tkinter as tk
import math

def dist(A, B):
    return math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)

def abs(val):
    if val < 0:
        return -val
    return val

def p_in_seg(p, A, B):
    if dist(p, A) + dist(p, B) == dist(A, B):
        return True
    return False

def det3(mat3):#determinant d'une matrice 3*3
    d1 = mat3[0][0]*mat3[1][1]*mat3[2][2]
    d2 = mat3[0][1]*mat3[1][2]*mat3[2][0]
    d3 = mat3[0][2]*mat3[1][0]*mat3[2][1]
    
    f1 = mat3[0][2]*mat3[1][1]*mat3[2][0]
    f2 = mat3[0][1]*mat3[1][0]*mat3[2][2]
    f3 = mat3[0][0]*mat3[1][2]*mat3[2][1]
    return d1 + d2 + d3 - f1 - f2 - f3

def mat_3points(p1, p2, p3):
    mat = [[0]*3 for i in range(3)]
    p = p1 + p2 + p3
    for i in range(3):
        mat[i][0] = p[i*2]
        mat[i][1] = p[i*2+1]
        mat[i][2] = 1
    return mat

def vect(A, B):
    print(A, B, (B[0]-A[0],B[1]-A[1]))
    return (B[0]-A[0],B[1]-A[1])

def prod_scalaire2(vect1, vect2):
    return vect1[0] * vect1[1] + vect2[0] * vect2[1]

class Application():
    
    def __init__(self, width, height):
        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=width, height=height, bg="white")
        self.cnv.pack()

        self.width = width
        self.height = height
        self.rayon = 50

        self.points_droite_coords = [None,None]
        self.centre_cercle_coords = None

        self.cnv.bind('<Button-1>', self.add_point_seg1)
        self.cnv.bind('<Button-2>', self.add_centre_cercle)
        self.cnv.bind('<Button-3>', self.add_point_seg2)
        tk.Button(self.wnd, command=self.delete_points, text="Supprimer les points").pack()
        tk.Button(self.wnd, command=self.droite, text="Afficher la droite").pack()
        tk.Button(self.wnd, command=self.delete_all, text="Tout supprimer").pack()
        tk.Button(self.wnd, command=self.delete_droite, text="Supprimer la droite").pack()
        tk.Button(self.wnd, command=self.aff_cercle, text="Afficher le cercle").pack()
        tk.Button(self.wnd, command=self.aug_rayon, text="Augmenter le rayon").pack()
        tk.Button(self.wnd, command=self.dim_rayon, text="Diminuer le rayon").pack()
        tk.Button(self.wnd, command=self.aff_inter, text="Afficher les intersections").pack()
        self.rayon_label = tk.Label(self.wnd, text="Rayon: "+str(self.rayon))
        self.rayon_label.pack()

        self.wnd.mainloop()
    
    def add_point_seg1(self, event):
        self.points_droite_coords[0] = (event.x, event.y)
        self.cnv.delete("point1")
        self.cnv.delete("A")
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="blue", tag="point1")
        self.cnv.create_text(event.x, event.y-8, text="A", tag="A")

    def add_centre_cercle(self, event):
        self.centre_cercle_coords = (event.x, event.y)
        self.cnv.delete("centre_cercle")
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="green", tag="centre_cercle")
        self.cnv.create_text(event.x, event.y-8, text="S", tag="S")

    def add_point_seg2(self, event):
        self.points_droite_coords[1] = (event.x, event.y)
        self.cnv.delete("point2")
        self.cnv.delete("B")
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="blue", tag="point2")
        self.cnv.create_text(event.x, event.y-8, text="B", tag="B")

    def delete_points(self):
        self.points_droite_coords = [None,None]
        self.centre_cercle_coords = None
        self.cnv.delete("A")
        self.cnv.delete("B")
        self.cnv.delete("point1")
        self.cnv.delete("point2")
        self.cnv.delete("centre_cercle")
    
    def aug_rayon(self):
        self.rayon += 1
        self.rayon_label["text"] = "Rayon: " + str(self.rayon)
        self.aff_cercle()

    def dim_rayon(self):
        self.rayon -= 1
        self.rayon_label["text"] = "Rayon " + str(self.rayon)
        self.aff_cercle()

    def aff_cercle(self):
        self.cnv.delete("cercle")
        self.cnv.create_oval(self.centre_cercle_coords[0]-self.rayon,
                             self.centre_cercle_coords[1]-self.rayon,
                             self.centre_cercle_coords[0]+self.rayon,
                             self.centre_cercle_coords[1]+self.rayon,
                             outline="green", tag="cercle")

    def droite(self):
        self.cnv.delete("droite")
        self.cnv.create_line(self.points_droite_coords,
                             fill="purple", tag="droite")

    def delete_droite(self):
        self.cnv.delete("droite")
        self.cnv.delete("point1")
        self.cnv.delete("point2")
        self.cnv.delete("A")
        self.cnv.delete("B")
        self.points_droite_coords = [None,None]

    def delete_cercle(self):
        self.cnv.delete("centre_cercle")
        self.cnv.delete("cercle")
        self.cnv.delete("S")
        self.centre_cercle_coords = None

    def delete_all(self):
        self.delete_droite()
        self.delete_cercle()

    def aff_inter(self):
        self.cnv.delete("inter")
        if self.test_inter():
            A = (self.points_droite_coords[0][0], 400 - self.points_droite_coords[0][1])
            B = (self.points_droite_coords[1][0], 400 - self.points_droite_coords[1][1])
            S = (self.centre_cercle_coords[0], 400 - self.centre_cercle_coords[1])

            AB = dist(A, B)

            vectAS = vect(A, S)
            vectAB = vect(A, B)

            h = prod_scalaire2(vectAS, vectAB) / AB**2

            matASB = mat_3points(A, S, B)
            detASB = det3(matASB)
            d = math.sqrt(detASB**2 / AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB
            print(vectAS, vectAB, prod_scalaire2(vectAS, vectAB))
            xIB = (1 - h - t) * A[0] + (h + t) * B[0]
            yIB = (1 - h - t) * A[1] + (h + t) * B[1]

            #print(xIB, yIB)

            self.cnv.create_oval(xIB-3, (400-yIB)-3, xIB+3, (400-yIB)+3,
                                 fill="red", tag="inter")

            '''vectAS = vect(self.points_droite_coords[0],
                          self.centre_cercle_coords)
            vectAB = vect(self.points_droite_coords[0],
                          self.points_droite_coords[1])
            prod_scal = prod_scalaire2(vectAS, vectAB)
            h = prod_scal/(dist(self.points_droite_coords[0],
                               self.points_droite_coords[1])**2)
            matASB = mat_3points(self.points_droite_coords[0],
                             self.centre_cercle_coords,
                             self.points_droite_coords[1])
            detASB = det3(matASB)
            d = math.sqrt((detASB**2)/(dist(self.points_droite_coords[0],
                        self.points_droite_coords[1])**2))
            t = math.sqrt(self.rayon**2-d**2)/dist(self.points_droite_coords[0],
                        self.points_droite_coords[1])
            #Calcul 1ère intersection
            xIa = self.points_droite_coords[0][0] + vectAB[0] * (h-t)
            yIa = ((1-h+t) * self.points_droite_coords[0][1] +
                   (h-t) * self.points_droite_coords[1][1])
            self.cnv.create_oval(xIa-3, yIa-3, xIa+3, yIa+3, tag="inter",
                                 fill="red")'''

    def test_inter(self):
        matASB = mat_3points(self.points_droite_coords[0],
                             self.centre_cercle_coords,
                             self.points_droite_coords[1])
        detASB = abs(det3(matASB))
        d = detASB/dist(self.points_droite_coords[0],
                        self.points_droite_coords[1])
        if d > self.rayon:
            return False
        return True

Application(600,400)