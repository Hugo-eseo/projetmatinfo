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


def sc(u, v):
    """Renvoie le produit scalaire entre deux vecteurs u et v"""
    return(u[0]*v[0] + u[1]*v[1])


def norme(u):
    """Renvoie la norme d'un vecteur"""
    return(math.sqrt(u[0]**2 + u[1]**2))


def vect(u, v):
    """Renvoie le produit vectoriel de deux vecteurs en dimension 2"""
    return(u[0]*v[1]-u[1]*v[0])


def pointapts(A, A1, A2):
    """Renvoie True si le point A appartient au segment [A1;A2]"""
    if math.isclose(dist(A, A1) + dist(A, A2), dist(A1, A2), rel_tol=0.01):
        return True
    return False


def inter2d(A1, A2, B1, B2, requireInt=False):
    """Calcul les coordonnées du point d'intersection de 2 droites définies
    par 4 points"""
    a, b = det3pts(B1, B2, A2), det3pts(B2, B1, A1)
    if a+b == 0:
        return None
    x = (a*A1[0] + b*A2[0])/(a+b)
    y = (a*A1[1] + b*A2[1])/(a+b)
    I = (x, y)
    if signe(a) != signe(b):
        if (x, y) != A1 and (x, y) != A2 and (x, y) != B1 and (x, y) != B2:
            return None
    if requireInt:
        if not(pointapts(I, A1, A2) and pointapts(I, B1, B2)):
            return None
    return (x, y)


class Application():
    """Crée la fenêtre de l'application"""
    # Paramètres pour les différents modes de demo
    state = 1
    nbd = 0
    nbrayons = 60
    d = list()
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

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
        tk.Button(self.frm, text='[PRESET1] Museum',
                  command=self.preset1).pack()
        tk.Button(self.frm, text='[PRESET2] Autre',
                  command=self.preset2).pack()
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
        self.cnv.unbind('<Button-3>')

    def demo2(self):
        """Lancement de la demo 2"""
        self.cnv.delete(tk.ALL)
        self.d_to_check = [[(0, 0), (self.width, 0)],
                           [(0, 0), (0, self.height)],
                           [(self.width, 0), (self.width, self.height)],
                           [(0, self.height), (self.width, self.height)]]
        self.cnv.bind('<Button-1>', self.rayon_obsatcles_demo)
        self.cnv.unbind('<Button-3>')
        self.reset_button.config(command=self.demo2)
        self.draw_obstacle()
        self.draw_obstacle()

    def demo3(self):
        """Lancement de la demo3 3"""
        self.reset_button.config(command=self.demo3)
        self.p_polygon = []
        self.sommets_polygon = []
        self.d_to_check = []
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.dessin_polygone_demo)
        self.cnv.bind('<Button-3>', self.fin_dessin_polygone)

    def preset1(self):
        size = 4
        self.sommets_polygon = [(243, 308), (244, 286), (242, 244), (206, 242),
                                (171, 243), (145, 241), (125, 242), (99, 241),
                                (76, 242), (43, 240), (42, 221), (41, 199),
                                (40, 165), (39, 148), (38, 120), (37, 96),
                                (36, 67), (35, 37), (62, 38), (81, 36),
                                (103, 35), (105, 60), (104, 87), (82, 84),
                                (62, 83), (63, 101), (64, 129), (65, 155),
                                (66, 185), (67, 199), (86, 196), (113, 195),
                                (136, 194), (166, 193), (198, 195), (196, 169),
                                (195, 149), (152, 148), (110, 147), (106, 114),
                                (131, 113), (132, 83), (131, 52), (154, 49),
                                (174, 47), (175, 71), (174, 104), (196, 105),
                                (215, 105), (220, 80), (221, 62), (226, 32),
                                (249, 16), (276, 17), (310, 16), (342, 17),
                                (345, 36), (323, 38), (288, 37), (267, 44),
                                (267, 66), (264, 101), (287, 100), (320, 101),
                                (358, 100), (376, 95), (375, 78), (373, 56),
                                (375, 26), (407, 21), (427, 22), (438, 21),
                                (437, 58), (438, 94), (436, 116), (434, 139),
                                (432, 161), (434, 195), (432, 230), (434, 278),
                                (433, 329), (383, 336), (319, 338), (246, 340)]
        self.cnv.create_oval(264-size, 101-size, 264+size,
                             101+size, fill='red')
        self.cnv.create_oval(287-size, 100-size, 287+size,
                             100+size, fill='red')
        self.lancement_preset()

    def preset2(self):
        self.sommets_polygon = [(164, 302), (107, 388), (187, 371), (336, 472),
                                (427, 371), (508, 446), (737, 472), (820, 371),
                                (757, 105), (729, 328), (638, 261), (615, 116),
                                (468, 49), (334, 54), (374, 201), (269, 254),
                                (118, 115)]
        self.lancement_preset()

    def lancement_preset(self):
        self.d_to_check = []
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        for i in range(len(self.sommets_polygon)):
            if i > 0:
                A = self.sommets_polygon[i]
                B = self.sommets_polygon[i-1]
                self.d_to_check.append([B, A])
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append([B, A])
        self.cnv.bind('<Button-1>', self.point_in_polygon_demo)

    def dessin_polygone_demo(self, event):
        size = 4
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='black', tag='pts')
        self.p_polygon.append(event.x)
        self.p_polygon.append(event.y)
        self.sommets_polygon.append((event.x, event.y))
        if len(self.sommets_polygon) > 1:
            A = self.sommets_polygon[-1]
            B = self.sommets_polygon[-2]
            self.d_to_check.append([B, A])
        self.cnv.create_text(event.x, event.y-10,
                             text=self.alphabet[len(self.sommets_polygon)-1],
                             tag='lettre')

    def fin_dessin_polygone(self, event):
        if not self.p_polygon:
            return
        self.cnv.create_polygon(self.p_polygon, fill='grey')
        self.cnv.tag_raise('lettre')
        print(self.p_polygon)
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append([B, A])
        self.p_polygon = []
        self.cnv.delete('pts')
        self.cnv.unbind('<Button-3>')
        self.cnv.bind('<Button-1>', self.point_in_polygon_demo)

    def point_in_polygon_demo(self, event):
        size = 4
        wn = 0
        demo = True
        nbI = 0
        self.cnv.delete('light')
        if demo:
            self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                                 event.y+size, fill='green', tag='light')
        A = (event.x, event.y)
        O = (0, A[1])
        M = (self.width, A[1])
        if demo:
            self.cnv.create_line(O, M, fill='red', tag='light')
        interliste = []
        angleliste = []
        e = None
        result = 0
        nbangle = 0
        for d in self.d_to_check:
            cd = [0, 0]
            I = inter2d(d[0], d[1], O, M, True)
            if I is not None:
                if I[0] == 1000:
                    print("d :", d)
                    print("O :" ,O)
                    print("M :", M)
                    print("I :", I)
                interliste.append(I)
                u = (d[1][0] - d[0][0], d[1][1] - d[0][1])
                if interliste.count(I) > 1:
                    nbangle += 1
                    '''v = (e[1][0] - e[0][0], e[1][1] - e[0][1])
                    cosinus = sc(u, v)/(norme(u)*norme(v))
                    sinus = vect(u, v)/(norme(u)*norme(v))
                    angle = math.atan2(sinus, cosinus)*180/math.pi
                    print("Angle entre les deux segments : ", angle)
                    if angle > 0:  # Si l'angle est aigu'''
                    self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                         I[1]+size, fill='blue', tag='light')
                    '''if len(nbI) % 2 == 0:
                        wn -= result
                        print("Un angle ignoré")
                    print("Result : ", result)
                    angleliste.append(result)'''
                    print(d[0], I)
                    if d[0] == I:
                        D = d[1]
                    else:
                        D = d[0]
                    if e[0] == I:
                        E = e[1]
                    else:
                        E = e[0]
                    print(D)
                    print(E)
                    if signe(D[1]-I[1]) == signe(E[1]-I[1]):
                        wn -= result
                        print("Skiped")
                    continue
                nbI += 1
                if demo:
                    self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                         I[1]+size, fill='red', tag='light')
                if u[1] < 0:
                    # Croisement vers le haut
                    if I[0] > A[0]:
                        # A est à gauche
                        wn += 1
                        result = 1
                    else:
                        result = 0
                else:
                    # Croisement vers le bas
                    if I[0] > A[0]:
                        # A est à droite
                        wn -= 1
                        result = -1
                    else:
                        result = 0
                e = d
                print("Wining number : ", wn)
                if demo:  # Pour debug
                    self.cnv.create_text(I[0], I[1]+10, text=result,
                                         tag='light')
        '''if nbI % 2 != 0 or nbangle == nbI:
            for i in range(nbangle):
                wn -= angleliste[i]'''
        print("Nombre d'angle détécté : ", nbangle)
        print("Nombre d'intersections : ", nbI)
        print("Wining number : ", wn)
        if wn != 0:
            print("Liste des intersections : ", interliste)
            self.rayon_obsatcles_demo(event)

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
        demo = False
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='yellow', tag='light')
        A = (event.x, event.y)
        B = (A[0]+1, A[1])
        for i in range(self.nbrayons):
            inter = []
            for d in self.d_to_check:
                I = inter2d(d[0], d[1], A, B)
                if I is not None:
                    if dist(I, A) > dist(I, B):
                        inter.append([dist(I, A), I])
            if not inter:
                # Utilisé pour debug
                self.cnv.create_line(A, B, fill='red', tag='light')
            else:
                I_p = min(inter)
                I = I_p[1]
                if demo:
                    self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                         I[1]+size, fill='red', tag='light')
                self.cnv.create_line(A, I, fill='yellow', tag='light')
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
