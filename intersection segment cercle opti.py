# -*- coding: utf-8 -*-
"""
Created on Mon May  3 10:20:16 2021

@author: hugof
"""

import tkinter as tk
import math

precision = 0.01

def dist2(point1, point2):
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
        if abs(dist2(point, segment.A) + dist2(point, segment.B) -
               dist2(segment.A, segment.B)) < precision:
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

class point_classe():
    """Docstring"""

    def __init__(self, x, y):
        """Prend en argument les coordonées x et y du point"""
        self.x, self.y = x, y

    def __str__(self):
        string = "(" + str(self.x) + "," + str(self.y) + ")"
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

    def __str__(self):
        string = "[" + str(self.A) + "," + str(self.B) + "]"
        return string

    def return_tuple(self):
        return [self.A.return_tuple(), self.B.return_tuple()]

def vabs(val):
    if val < 0:
        return -val
    return val

def dist(A, B):
    """Renvoie la distance entre deux points passés en arguments"""
    return(math.sqrt((B[0] - A[0])**2+(B[1] - A[1])**2))

def mat3(A, B, C):
    """Renvoie une matrice 3*3, de 3 points passés en paramètres"""
    return [[A[0],A[1],1],[B[0],B[1],1],[C[0],C[1],1]]
    #return [[A[0],B[0],C[0]],[A[1],B[1],C[1]],[0,0,0]]
def det2(mat):
    """Renvoie le déterminant d'une matrice 2*2 passée en argument"""
    return(mat[0][0]*mat[1][1]-mat[1][0]*mat[0][1])

def vect(u, v):
    """Renvoie le produit vectoriel de deux vecteurs u et v passés en arguments
    en dimension 2"""
    return(u[0]*v[1]-u[1]*v[0])

def det3(mat):
    """Renvoie le déterminant d'une matrice 3*3 passée en argument"""
    a = mat[0][0]*det2([[mat[1][1], mat[1][2]], [mat[2][1], mat[2][2]]])
    b = mat[0][1]*det2([[mat[1][0], mat[1][2]], [mat[2][0], mat[2][2]]])
    c = mat[0][2]*det2([[mat[1][0], mat[1][1]], [mat[2][0], mat[2][1]]])
    return a-b+c

def det3sarrus(mat):
    d1 = mat[0][0]*mat[1][1]*mat[2][2]
    d2 = mat[0][1]*mat[1][2]*mat[2][0]
    d3 = mat[0][2]*mat[1][0]*mat[0][1]
    
    d4 = mat[0][2]*mat[1][1]*mat[2][0]
    d5 = mat[0][1]*mat[1][0]*mat[2][2]
    d6 = mat[0][0]*mat[1][2]*mat[2][1]
    
    return d1 + d2 + d3 - d4 - d5 - d6

def sc(u, v):
    """Renvoie le produit scalaire en dimension 2 entre deux vecteurs u et v
    passés en arguments"""
    return(u[0]*v[0] + u[1]*v[1])

def rotation(O, M, angle):
        """Renvoie les coordonnées du points M dans la rotation de centre O
        et d'angle 'angle'"""
        # Angle converti en radian
        angle = angle * math.pi / 180
        xM = M[0] - O[0]
        yM = M[1] - O[1]
        x = xM*math.cos(angle) + yM*math.sin(angle) + O[0]
        y = - xM*math.sin(angle) + yM*math.cos(angle) + O[1]
        return (x, y)

def angle_two_points(point, center):
    # a, b tuples of 2 
    rad = math.atan2(point[1] - center[1], point[0] - center[0])
    deg = rad * 180/math.pi
    return deg

def projection_point_cercle(centre, A, rayon):
    """Renvoie la projection sur le cercle d'un point extérieur à celui ci"""
    
    ASB = det3(mat3(A, centre, centre))
    AB = dist(A, centre)
    d = vabs(ASB)/AB
    
    vAB = (centre[0]-A[0], centre[1]-A[1])
    vAS = (centre[0]-A[0], centre[1]-A[1])
    h = sc(vAS, vAB)/(AB**2)
    t = math.sqrt(rayon**2 - d**2)/AB
    
    #1er point d'intersection
    a = 1 - h - t
    b = h + t
    xG1 = (a*A[0]+b*centre[0])
    yG1 = (a*A[1]+b*centre[1])
    
    d1 = dist(A, (xG1, yG1))
    
    #2eme point
    a = 1 - h + t
    b = h - t
    xG2 = (a*A[0]+b*centre[0])
    yG2 = (a*A[1]+b*centre[1])
    
    d2 = dist(A, (xG2, yG2))
    if d1 > d2:
        return (xG2, yG2)
    return (xG1, yG1)

class Application():
    
    def __init__(self):
        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=600, height=400, bg="lightgrey")
        self.cnv.pack()
        
        self.A = (0, 0)
        self.B = (0, 0)
        self.S = (300, 200)
        self.C = (300, 100)
        self.rayon = 150
        self.nb_seg = 3
        self.seg_actuel = 0
        
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
        
        self.cnv.create_oval(self.S[0]-self.rayon, self.S[1]-self.rayon, self.S[0]+self.rayon, self.S[1]+self.rayon)
        self.cnv.create_oval(self.S[0]-3, self.S[1]-3, self.S[0]+3, self.S[1]+3)
        
        tk.Button(self.wnd, text="afficher intersections", command=self.affichage_intersections).pack()
        tk.Button(self.wnd, text="clipping", command=self.clipping).pack()
        
        self.seg_choisi_bouton = tk.Button(self.wnd, text="Segment "+str(self.seg_actuel), command=self.seg_changement)
        self.seg_choisi_bouton.pack()
        
        self.cnv.bind("<1>", self.input_A)
        self.cnv.bind("<3>", self.input_B)
        self.cnv.bind("<Button-2>", self.affichage_cone2)

        self.wnd.mainloop()
    
    def input_A(self, event):
        self.A[self.seg_actuel] = (event.x, event.y)
        self.cnv.delete("pointA"+str(self.seg_actuel), "segAB"+str(self.seg_actuel))
        if self.B[self.seg_actuel] is not None:
            self.cnv.create_line(self.A[self.seg_actuel], self.B[self.seg_actuel], tag="segAB"+str(self.seg_actuel))
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="orange", tag="pointA"+str(self.seg_actuel))
    
    def input_B(self, event):
        self.B[self.seg_actuel] = (event.x, event.y)
        self.cnv.delete("pointB"+str(self.seg_actuel), "segAB"+str(self.seg_actuel))
        if self.A[self.seg_actuel] is not None:
            self.cnv.create_line(self.A[self.seg_actuel], self.B[self.seg_actuel], tag="segAB"+str(self.seg_actuel))
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="orange", tag="pointB"+str(self.seg_actuel))
    
    def seg_changement(self):
        self.seg_actuel += 1
        if self.seg_actuel == self.nb_seg:
            self.seg_actuel = 0
        self.seg_choisi_bouton["text"] = "Segment "+str(self.seg_actuel)
    
    def calcul_intersections(self, seg):
        ASB = det3(mat3(self.A[seg], self.S, self.B[seg]))
        AB = dist(self.A[seg], self.B[seg])
        d = vabs(ASB)/AB
        if d < self.rayon:
            print("La droite passe par le cercle, d = ",d)
            vAB = (self.B[seg][0]-self.A[seg][0], self.B[seg][1]-self.A[seg][1])
            vAS = (self.S[0]-self.A[seg][0], self.S[1]-self.A[seg][1])
            h = sc(vAS, vAB)/(AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB
            
            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG1 = (a*self.A[seg][0]+b*self.B[seg][0])
            yAG1 = (a*self.A[seg][1]+b*self.B[seg][1])
            
            #2eme point
            a = 1 - h + t
            b = h - t
            xAG2 = (a*self.A[seg][0]+b*self.B[seg][0])
            yAG2 = (a*self.A[seg][1]+b*self.B[seg][1])
            
            return (xAG1, yAG1),(xAG2, yAG2)
        return None, None
    def affichage_intersections(self):
        #Calcul de d
        ASB = det3(mat3(self.A[self.seg_actuel], self.S, self.B[self.seg_actuel]))
        AB = dist(self.A[self.seg_actuel], self.B[self.seg_actuel])
        d = vabs(ASB)/AB
        if d < self.rayon:
            self.cnv.delete("inter")
            print("La droite passe par le cercle, d = ",d)
            vAB = (self.B[self.seg_actuel][0]-self.A[self.seg_actuel][0], self.B[self.seg_actuel][1]-self.A[self.seg_actuel][1])
            vAS = (self.S[0]-self.A[self.seg_actuel][0], self.S[1]-self.A[self.seg_actuel][1])
            h = sc(vAS, vAB)/(AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB
            
            #Affichage point H
            a = 1 - h
            b = h
            xAG = (a*self.A[self.seg_actuel][0]+b*self.B[self.seg_actuel][0])
            yAG = (a*self.A[self.seg_actuel][1]+b*self.B[self.seg_actuel][1])
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="green", tag="inter")
            
            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG = (a*self.A[self.seg_actuel][0]+b*self.B[self.seg_actuel][0])
            yAG = (a*self.A[self.seg_actuel][1]+b*self.B[self.seg_actuel][1])
            
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red", tag="inter")
            
            #2eme point
            a = 1 - h + t
            b = h - t
            xAG = (a*self.A[self.seg_actuel][0]+b*self.B[self.seg_actuel][0])
            yAG = (a*self.A[self.seg_actuel][1]+b*self.B[self.seg_actuel][1])
            
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red", tag="inter")
            
            print(xAG, yAG)
        else:
            print("La droite ne passe pas par le cercle")

    def clipping(self):
        self.clip1Seg()
        #self.clip2Seg()
        self.cnv.delete("cercle")
        self.cnv.create_oval(self.S[0]-self.rayon, self.S[1]-self.rayon, self.S[0]+self.rayon, self.S[1]+self.rayon)
        for i in range(self.nb_seg):
            self.cnv.delete("segAB"+str(i))
            self.cnv.create_line(self.A[i], self.B[i], tag="segAB"+str(i))
            self.cnv.delete("pointA"+str(i))
            self.cnv.create_oval(self.A[self.seg_actuel][0]-3, self.A[self.seg_actuel][1]-3,
                                 self.A[self.seg_actuel][0]+3, self.A[self.seg_actuel][1]+3,
                                 fill="orange", tag="pointA"+str(i))
            self.cnv.delete("pointB"+str(i))
            self.cnv.create_oval(self.B[self.seg_actuel][0]-3, self.B[self.seg_actuel][1]-3,
                                 self.B[self.seg_actuel][0]+3, self.B[self.seg_actuel][1]+3,
                                 fill="orange", tag="pointB"+str(i))

    def affichage_cone2(self, event):
        self.cnv.delete("cone")
        self.cnv.delete("clip1")
        self.cnv.delete("clip2")
        if event is not None:
            self.C = (event.x, event.y)
        self.C1 = rotation(self.S, self.C, -30)
        self.C2 = rotation(self.S, self.C, 30)

        #on veut l'intersection sur le cercle
        #projection 1
        self.proj1 = projection_point_cercle(self.S, self.C1, self.rayon)
        
        #projection 2
        self.proj2 = projection_point_cercle(self.S, self.C2, self.rayon)
        #Cone de lumière
        self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon, 
                            self.S[0]+self.rayon, self.S[1]+self.rayon,
                            start=-angle_two_points(self.proj1, self.S), extent=60,
                            tag="cone", fill="yellow", outline="yellow")
    
    def clip1Seg(self):
        self.cnv.delete("clip1")
        self.cnv.delete("clip2")
        self.cnv.delete("point")
        self.angle_proj1 = -angle_two_points(self.proj1, self.S)
        self.angle_proj2 = -angle_two_points(self.proj2, self.S)

        if self.angle_proj1 < 0:
            self.angle_proj1 += 360

        if self.angle_proj2 < 0:
            self.angle_proj2 += 360

        if self.angle_proj1 > self.angle_proj2:
            self.proj1, self.proj2 = self.proj2, self.proj1
            self.angle_proj1, self.angle_proj2 = self.angle_proj2, self.angle_proj1

        self.ecart_proj = vabs(self.angle_proj2 - self.angle_proj1)
        if self.ecart_proj >= 180:
            self.angle_proj1, self.angle_proj2 = self.angle_proj2, self.angle_proj1
            self.proj1, self.proj2 = self.proj2, self.proj1
        
        #Tri des segments
        d_list = list()
        for i in range(self.nb_seg):
            ASB = det3(mat3(self.A[i], self.S, self.B[i]))
            AB = dist(self.A[i], self.B[i])
            d_list.append(vabs(ASB)/AB)
        
        d_non_trie = True
        
        while d_non_trie:
            changement = False
            for i in range(self.nb_seg-1):
                if d_list[i] < d_list[i+1]:
                    d_list[i], d_list[i+1] = d_list[i+1], d_list[i]
                    self.A[i], self.A[i+1] = self.A[i+1], self.A[i]
                    self.B[i], self.B[i+1] = self.B[i+1], self.B[i]
                    changement = True
            if changement == False:
                d_non_trie = False
        #Calcul de AS, BS et d
        for i in range(self.nb_seg):
            self.clip[i] = False
            if self.A[i] is not None and self.B[i] is not None:
                AS = dist(self.A[i], self.S)
                BS = dist(self.B[i], self.S)
                ASB = det3(mat3(self.A[i], self.S, self.B[i]))
                AB = dist(self.A[i], self.B[i])
                d = vabs(ASB)/AB
                if d < self.rayon or BS < self.rayon or AS < self.rayon:
                    self.clip[i] = True
                    #Intersections entre le cercle et la droite
                    self.inter1[i], self.inter2[i] = self.calcul_intersections(i)
                    self.angle_inter1[i] = -angle_two_points(self.inter1[i], self.S)
                    if self.angle_inter1[i] < 0:
                        self.angle_inter1[i] += 360
        
                    self.angle_inter2[i] = -angle_two_points(self.inter2[i], self.S)
                    if self.angle_inter2[i] < 0:
                        self.angle_inter2[i] += 360
        
                    if self.angle_inter1[i] > self.angle_inter2[i]:
                        self.inter1[i], self.inter2[i] = self.inter2[i], self.inter1[i]
                        self.angle_inter1[i], self.angle_inter2[i] = self.angle_inter2[i], self.angle_inter1[i]
        
                    self.ecart = vabs(self.angle_inter2[i] - self.angle_inter1[i])
                    if self.ecart >= 180:
                        self.angle_inter2[i], self.angle_inter1[i] = self.angle_inter1[i], self.angle_inter2[i]
                        self.inter1[i], self.inter2[i] = self.inter2[i], self.inter1[i]
        
                    self.angle_A[i] = -angle_two_points(self.A[i], self.S)
                    self.angle_B[i] = -angle_two_points(self.B[i], self.S)
        
        
                    if self.angle_A[i] < 0:
                        self.angle_A[i] += 360
                        
                    if self.angle_B[i] < 0:
                        self.angle_B[i] += 360
        
                    if self.angle_A[i] > self.angle_B[i]:
                        self.A[i], self.B[i] = self.B[i], self.A[i]
                        self.angle_A[i], self.angle_B[i] = self.angle_B[i], self.angle_A[i]
                        AS, BS = BS, AS
        
                    ecart_AB = vabs(self.angle_B[i] - self.angle_A[i])
                    if ecart_AB >= 180:
                        self.angle_A[i], self.angle_B[i] = self.angle_B[i], self.angle_A[i]
                        self.A[i], self.B[i] = self.B[i], self.A[i]
                        AS, BS = BS, AS
        
                    if self.ecart_proj < 180 and self.ecart < 180:
                        if self.angle_B[i] < self.angle_proj2 and self.angle_B[i] < self.angle_inter2[i] and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
                        if self.angle_A[i] > self.angle_proj1 and self.angle_A[i] > self.angle_inter1[i] and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
                    elif self.ecart_proj < 180 and self.ecart >= 180:
                        if self.angle_B[i] < self.angle_proj2 and self.angle_B[i] < self.angle_inter2[i] and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
                        if self.angle_B[i] < self.angle_proj2 and self.angle_B[i] > self.angle_inter2[i] and self.angle_inter2[i] < self.angle_proj1\
                            and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
        
                        if self.angle_A[i] > self.angle_proj1 and self.angle_A[i] > self.angle_inter1[i] and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
                        if self.angle_A[i] > self.angle_proj1 and self.angle_A[i] < self.angle_inter1[i] and self.angle_inter1[i] > self.angle_proj2\
                            and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
        
                    if self.ecart_proj >= 180 and self.ecart < 180:
                        if self.angle_B[i] < self.angle_inter2[i] and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
        
                        if self.angle_A[i] > self.angle_proj1 and self.angle_A[i] > self.angle_inter1[i] and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
        
                    if self.ecart_proj >= 180 and self.ecart >=180:
                        if self.angle_B[i] < self.angle_proj2 and self.angle_B[i] < self.angle_inter2[i] and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
                        if self.angle_B[i] > self.angle_proj2 and self.angle_B[i] > self.angle_inter2[i] and self.angle_B[i] > self.angle_proj1\
                            and BS < self.rayon:
                            self.inter2[i] = self.B[i]
                            self.angle_inter2[i] = self.angle_B[i]
        
                        if self.angle_A[i] > self.angle_proj1 and self.angle_A[i] > self.angle_inter1[i] and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
                        if self.angle_A[i] < self.angle_proj1 and self.angle_A[i] < self.angle_inter1[i] and self.angle_A[i] < self.angle_proj2\
                            and AS < self.rayon:
                            self.inter1[i] = self.A[i]
                            self.angle_inter1[i] = self.angle_A[i]
        
                    if self.ecart_proj < 180 and self.angle_B[i] < self.angle_proj1 and self.angle_A[i] < self.angle_proj1 and ecart_AB < 180:
                        self.clip[i] = False
                    if self.ecart_proj < 180 and self.angle_B[i] > self.angle_proj2 and self.angle_A[i] > self.angle_proj2 and ecart_AB < 180:
                        self.clip[i] = False
                    if self.ecart_proj < 180 and self.angle_B[i] < self.angle_proj1 and self.angle_A[i] > self.angle_proj2 and ecart_AB > 180:
                        self.clip[i] = False
                    if self.ecart_proj > 180 and self.angle_B[i] > self.angle_proj2 and self.angle_A[i] > self.angle_proj2 and ecart_AB < 180\
                        and self.angle_B[i] < self.angle_proj1:
                        self.clip[i] = False
                    if self.ecart_proj < 180 and self.angle_inter1[i] > self.angle_proj2 \
                        and self.angle_inter2[i] > self.angle_proj2 and self.ecart < 180:
                        self.clip[i] = False
                    if self.ecart_proj < 180  and self.angle_inter1[i] < self.angle_proj1 \
                        and self.angle_inter2[i] < self.angle_proj1 and self.ecart < 180:
                        self.clip[i] = False
                    if round(self.angle_A[i]) == round(self.angle_B[i]) and self.angle_A[i]:
                        self.clip[i] = False

                    if self.clip[i]:
                        sp = point_classe(self.S[0], self.S[1])
                        proj1p = point_classe(self.proj1[0], self.proj1[1])
                        proj2p = point_classe(self.proj2[0], self.proj2[1])
            
                        inter1p = point_classe(self.inter1[i][0], self.inter1[i][1])
                        inter2p = point_classe(self.inter2[i][0], self.inter2[i][1])
            
                        seg1 = segment_classe(inter1p, inter2p)
                        seg21 = segment_classe(proj1p, sp)
                        seg22 = segment_classe(proj2p, sp)
            
                        int1p = intersection_segments(seg1, seg21)
                        int2p = intersection_segments(seg1, seg22)
            
                        if self.ecart_proj < 180 and self.ecart < 180:
                            if self.angle_proj1 > self.angle_inter1[i]:
                                self.angle_inter1[i] = self.angle_proj1
                                self.inter1[i] = int1p.return_tuple()
                            if self.angle_proj2 < self.angle_inter2[i]:
                                self.angle_inter2[i] = self.angle_proj2
                                self.inter2[i] = int2p.return_tuple()
                        if self.ecart_proj < 180 and self.ecart >= 180:
                            if self.angle_proj1 > self.angle_inter1[i] and self.angle_inter1[i] < self.angle_proj2:
                                self.angle_inter1[i] = self.angle_proj1
                                self.inter1[i] = int1p.return_tuple()
                            if self.angle_proj1 < self.angle_inter1[i] and self.angle_inter1[i] > self.angle_proj2:
                                self.angle_inter1[i] = self.angle_proj1
                                self.inter1[i] = int1p.return_tuple()
                            if self.angle_proj2 < self.angle_inter2[i] and self.angle_inter2[i] > self.angle_proj1:
                                self.angle_inter2[i] = self.angle_proj2
                                self.inter2[i] = int2p.return_tuple()
                            if self.angle_proj2 > self.angle_inter2[i] and self.angle_inter2[i] < self.angle_proj1:
                                self.angle_inter2[i] = self.angle_proj2
                                self.inter2[i] = int2p.return_tuple()
                        if self.ecart_proj > 180 and self.ecart < 180:
                            if self.angle_proj2 < self.angle_inter2[i] and self.angle_inter2[i] < self.angle_proj1:
                                self.angle_inter2[i] = self.angle_proj2
                                self.inter2[i] = int2p.return_tuple()
                            if self.angle_proj1 > self.angle_inter1[i] and self.angle_inter1[i] > self.angle_proj2:
                                self.angle_inter1[i] = self.angle_proj1
                                self.inter1[i] = int1p.return_tuple()
                        if self.ecart_proj > 180 and self.ecart > 180:
                            if self.angle_proj1 > self.angle_inter1[i] and self.angle_inter1[i] > self.angle_proj2:
                                self.angle_inter1[i] = self.angle_proj1
                                self.inter1[i] = int1p.return_tuple()
                            if self.angle_proj2 < self.angle_inter2[i] and self.angle_inter2[i] < self.angle_proj1:
                                self.angle_inter2[i] = self.angle_proj2
                                self.inter2[i] = int2p.return_tuple()
            
                        diff = vabs(self.angle_inter2[i] - self.angle_inter1[i])
                        self.ecart = vabs(self.angle_inter2[i] - self.angle_inter1[i])
                        if self.ecart >= 180:
                            diff = vabs(360 - self.angle_inter1[i] + self.angle_inter2[i])
                        
                        self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon,
                                            self.S[0]+self.rayon, self.S[1]+self.rayon,
                                            fill="lightgrey", tag="clip1", start=self.angle_inter1[i],
                                            extent=diff,
                                            outline="lightgrey")
                        self.cnv.create_polygon(self.S[0], self.S[1], self.inter1[i][0], self.inter1[i][1],
                                            self.inter2[i][0], self.inter2[i][1], fill="yellow",
                                            outline="yellow", tag="clip2")
                    self.cnv.create_text(self.A[i][0]-5, self.A[i][1]-5, text="A"+str(i), tag="point")
                    self.cnv.create_text(self.B[i][0]-5, self.B[i][1]-5, text="B"+str(i), tag="point")

    def clip2Seg(self):
        self.cnv.delete("clip2")
        for i in range(self.nb_seg):
            if self.clip[i]:
                self.cnv.create_polygon(self.S[0], self.S[1], self.inter1[i][0], self.inter1[i][1],
                                            self.inter2[i][0], self.inter2[i][1], fill="yellow",
                                            outline="yellow", tag="clip2")
        
Application()