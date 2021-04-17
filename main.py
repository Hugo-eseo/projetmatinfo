# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:23:28 2021

@author: hugob
"""
import tkinter as tk
import random
import math


def signe(n):
    """Renvoie le signe d'un nombre passé en argument"""
    if n == 0:
        return 0
    if n > 0:
        return 1
    return -1


def det2(mat):
    """Calcul le déterminant d'une matrice 2*2"""
    return(mat[0][0]*mat[1][1]-mat[1][0]*mat[0][1])


def det3(mat):
    """Calcul le déterminant d'une matrice 3*3"""
    a = mat[0][0]*det2([[mat[1][1], mat[1][2]], [mat[2][1], mat[2][2]]])
    b = mat[0][1]*det2([[mat[1][0], mat[1][2]], [mat[2][0], mat[2][2]]])
    c = mat[0][2]*det2([[mat[1][0], mat[1][1]], [mat[2][0], mat[2][1]]])
    return a-b+c


def det3pts(M, N, P):
    """Renvoie le déterimant de 3 points"""
    mat = [[M[0], N[0], P[0]], [M[1], N[1], P[1]], [1, 1, 1]]
    return det3(mat)

def dist(A, B):
    """Renvoie la distance entre deux points"""
    return(math.sqrt((B[0] - A[0])**2+(B[1] - A[1])**2))


def inter2d(A1, A2, B1, B2):
    """Calcul les coordonnées du point d'intersection de 2 droites définies
    par 4 points"""
    a, b = det3pts(B1, B2, A2), det3pts(B2, B1, A1)
    if signe(a) != signe(b):
        return None
    if a+b == 0:
        return None
    x = (a*A1[0] + b*A2[0])/(a+b)
    y = (a*A1[1] + b*A2[1])/(a+b)
    return [x, y]


class Application():
    """Crée la fenêtre de l'application"""
    # Paramètres pour les différents modes de demo
    state = 1
    nbd = 0
    nbrayons = 60
    d = list()

    def __init__(self, width, height):
        """Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        """
        self.width, self.height = width, height
        self.wnd = tk.Tk()
        self.wnd.title("Visualisation intersection 2 droites")
        self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
        self.cnv.pack()
        self.frm = tk.Frame(self.wnd, width=self.width, height=100)
        self.frm.pack(side=tk.BOTTOM)
        tk.Button(self.frm, text='Quiter', command=self.wnd.destroy).pack()
        tk.Button(self.frm, text='[DEMO] Intersection deux droites',
                  command=self.demo1).pack()
        tk.Button(self.frm, text='[DEMO] Rayon et obstacles',
                  command=self.demo2).pack()
        tk.Button(self.frm, text='[DEMO] Dessiner un polygone',
                  command=self.demo3).pack()
        self.reset_button = tk.Button(self.frm, text='Reset',
                                      command=self.reset)
        self.reset_button.pack()
        self.wnd.mainloop()

    def reset(self):
        """Reset du canvas"""
        self.cnv.delete(tk.ALL)

    def demo1(self):
        """Lancement de la demo 1"""
        self.reset_button.config(command=self.reset)
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.intersection_deux_droites_demo)

    def demo2(self):
        """Lancement de la demo 2"""
        self.cnv.delete(tk.ALL)
        self.d_to_check = [[(0, 0), (self.width, 0)],
                           [(0, 0), (0, self.height)],
                           [(self.width, 0), (self.width, self.height)],
                           [(0, self.height), (self.width, self.height)]]
        self.cnv.bind('<Button-1>', self.rayon_obsatcles_demo)
        self.reset_button.config(command=self.demo2)
        self.draw_obstacle()
        self.draw_obstacle()

    def demo3(self):
        """Lancement de la demo3 3"""
        self.reset_button.config(command=self.demo3)
        self.p_polygon = []
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.dessin_polygone_demo)
        self.cnv.bind('<Button-3>', self.fin_dessin_polygone)

    def dessin_polygone_demo(self, event):
        size = 4
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='black')
        self.p_polygon.append(event.x)
        self.p_polygon.append(event.y)
        
    def fin_dessin_polygone(self, event):
        if not self.p_polygon:
            return
        self.cnv.create_polygon(self.p_polygon, fill='grey')

    def draw_obstacle(self):
        """Dessine un obsacle quelconque sur le canas"""
        width, height = random.randint(0, 50), random.randint(100, 200)
        x, y = random.randint(0, self.width-width),\
            random.randint(0, self.height-height)
        angle = random.randint(0, 360)
        x1, y1 = x+width, y+height
        A, B, C, D = (x, y), (x1, y), (x1, y1), (x, y1)
        B, C, D = self.rotation(A, B, angle), self.rotation(A, C, angle),\
            self.rotation(A, D, angle)
        self.d_to_check.append([A, B])
        self.d_to_check.append([B, C])
        self.d_to_check.append([C, D])
        self.d_to_check.append([D, A])
        self.cnv.create_polygon(A, B, C, D, fill='green')

    def rotation(self, O, M, angle):
        """Renvoie les coordonnées du points dans la rotation de centre O
        et d'angle 'angle'"""
        angle = angle * math.pi / 180
        xM = M[0] - O[0]
        yM = M[1] - O[1]
        x = xM*math.cos(angle) + yM*math.sin(angle) + O[0]
        y = - xM*math.sin(angle) + yM*math.cos(angle) + O[1]
        return (x, y)

    def rayon_obsatcles_demo(self, event):
        """Demo : intersection rayon lumineux contre des obstacles"""
        size = 4
        angle = 360/self.nbrayons
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='yellow')
        A = (event.x, event.y)
        B = (A[0]+50, A[1])
        for i in range(self.nbrayons):
            inter = []
            for d in self.d_to_check:
                I = inter2d(d[0], d[1], A, B)
                if I is not None:
                    if dist(I, A) > dist(I, B):
                        inter.append([dist(I, A), I])
            if not inter:
                # Utilisé pour debug
                self.cnv.create_line(A, B, fill='red')
            else:
                I_p = min(inter)
                I = I_p[1]
                self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                     I[1]+size, fill='red')
                self.cnv.create_line(A, I, fill='yellow')
            B = self.rotation(A, B, angle)

    def intersection_deux_droites_demo(self, event):
        """Demo : Machine à état pour le dessin des droites"""
        size = 4
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='black')
        if self.state == 1:
            self.A = [event.x, event.y]
            self.state = 2

        elif self.state == 2:
            self.B = [event.x, event.y]
            self.cnv.create_line(self.A[0], self.A[1], self.B[0], self.B[1],
                                 fill='black')
            self.state = 1
            self.nbd += 1
            self.d.append([self.A, self.B])

        if self.nbd == 2:
            I = inter2d(self.d[0][0], self.d[0][1], self.d[1][0], self.d[1][1])
            self.d = []
            if I is not None:
                self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                     I[1]+size, fill='red')
            self.nbd = 0


Application(1000, 500)
