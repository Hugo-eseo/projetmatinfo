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

        self.cnv.create_oval(self.S[0]-self.rayon, self.S[1]-self.rayon, self.S[0]+self.rayon, self.S[1]+self.rayon)
        self.cnv.create_oval(self.S[0]-3, self.S[1]-3, self.S[0]+3, self.S[1]+3)
        
        tk.Button(self.wnd, text="afficher intersections", command=self.affichage_intersections).pack()
        tk.Button(self.wnd, text="clipping", command=self.clipping).pack()
        self.cnv.bind("<1>", self.input_A)
        self.cnv.bind("<3>", self.input_B)
        self.cnv.bind("<Button-2>", self.affichage_cone2)

        self.wnd.mainloop()
    
    def input_A(self, event):
        self.A = (event.x, event.y)
        self.cnv.delete("pointA", "segAB")
        self.cnv.create_line(self.A, self.B, tag="segAB")
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="orange", tag="pointA")
        #self.affichage_cone(None)
    
    def input_B(self, event):
        self.B = (event.x, event.y)
        self.cnv.delete("pointB", "segAB")
        self.cnv.create_line(self.A, self.B, tag="segAB")
        self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="orange", tag="pointB")
        #self.affichage_cone(None)
    
    def calcul_intersections(self):
        ASB = det3(mat3(self.A, self.S, self.B))
        AB = dist(self.A, self.B)
        d = vabs(ASB)/AB
        if d < self.rayon:
            self.cnv.delete("inter")
            print("La droite passe par le cercle, d = ",d)
            vAB = (self.B[0]-self.A[0], self.B[1]-self.A[1])
            vAS = (self.S[0]-self.A[0], self.S[1]-self.A[1])
            h = sc(vAS, vAB)/(AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB
            
            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG1 = (a*self.A[0]+b*self.B[0])
            yAG1 = (a*self.A[1]+b*self.B[1])
            
            #2eme point
            a = 1 - h + t
            b = h - t
            xAG2 = (a*self.A[0]+b*self.B[0])
            yAG2 = (a*self.A[1]+b*self.B[1])
            
            return (xAG1, yAG1),(xAG2, yAG2)
        return None, None
    def affichage_intersections(self):
        #Calcul de d
        ASB = det3(mat3(self.A, self.S, self.B))
        AB = dist(self.A, self.B)
        d = vabs(ASB)/AB
        if d < self.rayon:
            self.cnv.delete("inter")
            print("La droite passe par le cercle, d = ",d)
            vAB = (self.B[0]-self.A[0], self.B[1]-self.A[1])
            vAS = (self.S[0]-self.A[0], self.S[1]-self.A[1])
            h = sc(vAS, vAB)/(AB**2)
            t = math.sqrt(self.rayon**2 - d**2)/AB
            
            #Affichage point H
            a = 1 - h
            b = h
            xAG = (a*self.A[0]+b*self.B[0])
            yAG = (a*self.A[1]+b*self.B[1])
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="green", tag="inter")
            
            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG = (a*self.A[0]+b*self.B[0])
            yAG = (a*self.A[1]+b*self.B[1])
            
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red", tag="inter")
            
            #2eme point
            a = 1 - h + t
            b = h - t
            xAG = (a*self.A[0]+b*self.B[0])
            yAG = (a*self.A[1]+b*self.B[1])
            
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red", tag="inter")
            
            print(xAG, yAG)
        else:
            print("La droite ne passe pas par le cercle")
    
    def affichage_cone(self, event):
        self.cnv.delete("clip")
        if event is not None:
            self.C = (event.x, event.y)
        self.C1 = rotation(self.S, self.C, -30)
        self.C2 = rotation(self.S, self.C, 30)
        
        #on veut l'intersection sur le cercle
        #projection 1
        self.cnv.delete("Cone1")
        proj1 = projection_point_cercle(self.S, self.C1, self.rayon)
        self.cnv.create_oval(proj1[0]-3, proj1[1]-3, proj1[0]+3, proj1[1]+3, fill="blue", tag="Cone1")
        
        #projection 2
        self.cnv.delete("Cone2")
        proj2 = projection_point_cercle(self.S, self.C2, self.rayon)
        self.cnv.create_oval(proj2[0]-3, proj2[1]-3, proj2[0]+3, proj2[1]+3, fill="blue", tag="Cone2")
        
        self.cnv.delete("Arc_cone")
        self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon, 
                            self.S[0]+self.rayon, self.S[1]+self.rayon,
                            start=-angle_two_points(proj1, self.S), extent=60,
                            tag="Arc_cone", fill="yellow")
        #Faire le clipping -> utiliser le même cercle
        #On trouve les intersections
        inter1, inter2 = self.calcul_intersections()
        #On rajoute un triangle "blanc par dessus"
        if inter1 is not None:
            #Calcul des angles entre les 2 intersections (segment et cercle)
            angle_inter1 = -angle_two_points(inter1, self.S)
            if angle_inter1 < 0:
                angle_inter1 = 360 + angle_inter1
            
            angle_inter2 = -angle_two_points(inter2, self.S)
            if angle_inter2 < 0:
                angle_inter2 = 360 + angle_inter2
            
            self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon,
                                    self.S[0]+self.rayon, self.S[1]+self.rayon,
                                    fill="lightgrey", tag="clip1", start=angle_inter1,
                                    extent=angle_inter2-angle_inter1,
                                    outline="")
            inter1p = point_classe(inter1[0], inter1[1])
            inter2p = point_classe(inter2[0], inter2[1])
            '''self.cnv.create_oval(inter1[0]-2, inter1[1]-2, inter1[0]+2, inter1[1]+2, fill="cyan", tag="clip")
            self.cnv.create_oval(inter2[0]-2, inter2[1]-2, inter2[0]+2, inter2[1]+2, fill="cyan", tag="clip")'''
            
            sp = point_classe(self.S[0], self.S[1])
            proj1p = point_classe(proj1[0], proj1[1])
            proj2p = point_classe(proj2[0], proj2[1])
            
            seg1 = segment_classe(inter1p, inter2p)
            '''seg1t = seg1.return_tuple()
            self.cnv.create_line(seg1t[0], seg1t[1], tag="clip", fill="red")'''
            
            seg21 = segment_classe(proj1p, sp)
            '''seg21t = seg21.return_tuple()
            self.cnv.create_line(seg21t[0], seg21t[1], tag="clip", fill="red")'''
            
            seg22 = segment_classe(proj2p, sp)
            '''seg22t = seg22.return_tuple()
            self.cnv.create_line(seg22t[0], seg22t[1], tag="clip", fill="red")'''
            
            int1p = intersection_segments(seg1, seg21)
            int2p = intersection_segments(seg1, seg22)
            print(int1p, int2p)
            '''print(int1p)
            
            int1 = int1p.return_tuple()'''
            
            '''#Calcul des angles entre les 2 intersections (segment et cercle)
            angle_inter1 = angle_two_points(inter1, self.S)
            angle_inter2 = angle_two_points(inter2, self.S)
            if angle_inter1 < angle_inter2:
                print("problème")
                inter1, inter2 = inter2, inter1
                angle_inter1, angle_inter2 = angle_inter2, angle_inter1'''
            
            #self.cnv.create_oval(int1[0]-2, int1[1]-2, int1[0]+2, int1[1]+2, fill="cyan", tag="clip")
            if int1p is not None:
                print("un truc devrait s'afficher là")
                int1 = int1p.return_tuple()
                self.cnv.create_polygon(self.S[0], self.S[1], int1[0], int1[1],
                                        inter2[0], inter2[1], fill="yellow",
                                        width=0, tag="clip")
                self.cnv.create_line(self.S[0], self.S[1], inter2[0], inter2[1],
                                     fill="yellow", tag="clip")
            if int2p is not None:
                print("un truc devrait s'afficher là")
                int2 = int2p.return_tuple()
                self.cnv.create_polygon(self.S[0], self.S[1], int2[0], int2[1],
                                        inter1[0], inter1[1], fill="yellow",
                                        width=0, tag="clip")
                self.cnv.create_line(self.S[0], self.S[1], inter1[0], inter1[1],
                                     fill="yellow", tag="clip")
        
    def clipping(self):
        self.clip1Seg()
        self.clip2Seg()
        self.cnv.delete("cercle")
        self.cnv.create_oval(self.S[0]-self.rayon, self.S[1]-self.rayon, self.S[0]+self.rayon, self.S[1]+self.rayon)
        self.cnv.delete("segAB")
        self.cnv.create_line(self.A, self.B, tag="segAB")
        self.cnv.delete("pointA")
        self.cnv.create_oval(self.A[0]-3, self.A[1]-3, self.A[0]+3, self.A[1]+3, fill="orange", tag="pointA")
        self.cnv.delete("pointB")
        self.cnv.create_oval(self.B[0]-3, self.B[1]-3, self.B[0]+3, self.B[1]+3, fill="orange", tag="pointB")
    
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
        '''self.cnv.create_oval(self.proj1[0]-3, self.proj1[1]-3, self.proj1[0]+3, self.proj1[1]+3, fill="blue", tag="cone")
        self.cnv.create_text(self.proj1[0], self.proj1[1]-10, text="proj1", tag="cone")'''
        
        #projection 2
        self.proj2 = projection_point_cercle(self.S, self.C2, self.rayon)
        '''self.cnv.create_oval(self.proj2[0]-3, self.proj2[1]-3, self.proj2[0]+3, self.proj2[1]+3, fill="blue", tag="cone")
        self.cnv.create_text(self.proj2[0], self.proj2[1]-10, text="proj2", tag="cone")'''
        #Cone de lumière
        self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon, 
                            self.S[0]+self.rayon, self.S[1]+self.rayon,
                            start=-angle_two_points(self.proj1, self.S), extent=60,
                            tag="cone", fill="yellow", outline="yellow")
    def clip1(self):
        self.cnv.delete("clip1")
        ASB = det3(mat3(self.A, self.S, self.B))
        AB = dist(self.A, self.B)
        d = vabs(ASB)/AB
        if d < self.rayon:
            #Intersections entre le cercle et la droite
            self.inter1, self.inter2 = self.calcul_intersections()
            self.angle_inter1 = -angle_two_points(self.inter1, self.S)
            if self.angle_inter1 < 0:
                self.angle_inter1 += 360
            
            self.angle_inter2 = -angle_two_points(self.inter2, self.S)
            if self.angle_inter2 < 0:
                self.angle_inter2 += 360
            
            self.angle_proj1 = -angle_two_points(self.proj1, self.S)
            self.angle_proj2 = -angle_two_points(self.proj2, self.S)
            
            if self.angle_inter1 > self.angle_inter2:
                self.inter1, self.inter2 = self.inter2, self.inter1
                self.angle_inter1, self.angle_inter2 = self.angle_inter2, self.angle_inter1
            
            if self.angle_proj1 < 0:
                self.angle_proj1 += 360
                
            if self.angle_proj2 < 0:
                self.angle_proj2 += 360
            
            diff = vabs(self.angle_inter2 - self.angle_inter1) 
            self.ecart = vabs(self.angle_inter2 - self.angle_inter1)
            if self.ecart >= 180:
                print("ECHANGE")
                self.angle_inter2, self.angle_inter1 = self.angle_inter1, self.angle_inter2
                self.inter1, self.inter2 = self.inter2, self.inter1
                diff = vabs(360 - self.angle_inter1 + self.angle_inter2)
            
            self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon,
                                    self.S[0]+self.rayon, self.S[1]+self.rayon,
                                    fill="lightgrey", tag="clip1", start=self.angle_inter1,
                                    extent=diff,
                                    outline="")
            '''self.cnv.create_text(self.inter1[0], self.inter1[1]-9, text="inter1", tag="clip1")
            self.cnv.create_text(self.inter2[0], self.inter2[1]-9, text="inter2", tag="clip1")'''
    
    def clip1Seg(self):
        self.cnv.delete("clip1")
        self.clip = False
        #Calcul de AS, BS et d
        AS = dist(self.A, self.S)
        BS = dist(self.B, self.S)
        ASB = det3(mat3(self.A, self.S, self.B))
        AB = dist(self.A, self.B)
        d = vabs(ASB)/AB
        if d < self.rayon or BS < self.rayon or AS < self.rayon:
            self.clip = True
            #Intersections entre le cercle et la droite
            self.inter1, self.inter2 = self.calcul_intersections()
            self.angle_inter1 = -angle_two_points(self.inter1, self.S)
            if self.angle_inter1 < 0:
                self.angle_inter1 += 360
            
            self.angle_inter2 = -angle_two_points(self.inter2, self.S)
            if self.angle_inter2 < 0:
                self.angle_inter2 += 360
            
            if self.angle_inter1 > self.angle_inter2:
                self.inter1, self.inter2 = self.inter2, self.inter1
                self.angle_inter1, self.angle_inter2 = self.angle_inter2, self.angle_inter1
                
            self.ecart = vabs(self.angle_inter2 - self.angle_inter1)
            if self.ecart >= 180:
                self.angle_inter2, self.angle_inter1 = self.angle_inter1, self.angle_inter2
                self.inter1, self.inter2 = self.inter2, self.inter1
            
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
            
            
            self.angle_A = -angle_two_points(self.A, self.S)
            self.angle_B = -angle_two_points(self.B, self.S)
            
            
            if self.angle_A < 0:
                self.angle_A += 360
                
            if self.angle_B < 0:
                self.angle_B += 360
            
            if self.angle_A > self.angle_B:
                self.A, self.B = self.B, self.A
                self.angle_A, self.angle_B = self.angle_B, self.angle_A
                AS, BS = BS, AS
            
            ecart_AB = vabs(self.angle_B - self.angle_A)
            if ecart_AB >= 180:
                self.angle_A, self.angle_B = self.angle_B, self.angle_A
                self.A, self.B = self.B, self.A
                AS, BS = BS, AS
            
            print("Angle A : ", self.angle_A, "\nAngle B : ", self.angle_B)
            print("Angle inter1: ", self.angle_inter1, "\nAngle_inter2: ", self.angle_inter2)
            print("ecart_proj: ", self.ecart_proj, "\nAngle_proj2: ", self.angle_proj2, "\nAngle_proj1: ", self.angle_proj1)
            print("self.ecart: ", self.ecart, "\nBS=", BS)
            if self.ecart_proj < 180 and self.ecart < 180:
                if self.angle_B < self.angle_proj2 and self.angle_B < self.angle_inter2 and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                    print("VALIDE")
                if self.angle_A > self.angle_proj1 and self.angle_A > self.angle_inter1 and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
                print("IF 1 passé")
            elif self.ecart_proj < 180 and self.ecart >= 180:
                if self.angle_B < self.angle_proj2 and self.angle_B < self.angle_inter2 and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                if self.angle_B < self.angle_proj2 and self.angle_B > self.angle_inter2 and self.angle_inter2 < self.angle_proj1\
                    and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                
                if self.angle_A > self.angle_proj1 and self.angle_A > self.angle_inter1 and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
                if self.angle_A > self.angle_proj1 and self.angle_A < self.angle_inter1 and self.angle_inter1 > self.angle_proj2\
                    and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
                
            if self.ecart_proj >= 180 and self.ecart < 180:
                if self.angle_B < self.angle_proj2 and self.angle_B < self.angle_inter2 and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                if self.angle_B > self.angle_proj2 and self.angle_B < self.angle_inter2 and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                if self.angle_A > self.angle_proj1 and self.angle_A > self.angle_inter1 and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
                if self.angle_A < self.angle_proj1 and self.angle_A > self.angle_inter1 and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
            if self.ecart_proj >= 180 and self.ecart >=180:
                if self.angle_B < self.angle_proj2 and self.angle_B < self.angle_inter2 and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                if self.angle_B > self.angle_proj2 and self.angle_B > self.angle_inter2 and self.angle_B > self.angle_proj1\
                    and BS < self.rayon:
                    self.inter2 = self.B
                    self.angle_inter2 = self.angle_B
                
                if self.angle_A > self.angle_proj1 and self.angle_A > self.angle_inter1 and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
                if self.angle_A < self.angle_proj1 and self.angle_A < self.angle_inter1 and self.angle_A < self.angle_proj2\
                    and AS < self.rayon:
                    self.inter1 = self.A
                    self.angle_inter1 = self.angle_A
            print(self.ecart)
            '''if self.ecart_proj < 180 and self.angle_B > self.angle_proj2 and self.angle_A > self.angle_proj2 and ecart_AB < 180:
                self.clip = False
            if self.ecart_proj < 180 and self.angle_B < self.angle_proj1 and self.angle_A < self.angle_proj1 and ecart_AB < 180:
                self.clip = False
            if self.ecart_proj >= 180 and self.angle_B > self.angle_proj2 and self.angle_A > self.angle_proj2 \
                and self.angle_B < self.angle_proj1 and self.angle_A < self.angle_proj1 and ecart_AB < 180:
                self.clip = False
            if self.ecart_proj < 180 and self.ecart > 180 and self.angle_A > self.angle_proj2 and self.angle_B < self.angle_proj1:
                self.clip = False
            if self.ecart_proj < 180 and self.angle_inter1 < self.angle_proj1 and self.angle_inter2 < self.angle_proj1 and ecart_AB < 180:
                self.clip = False'''
            
            if self.ecart_proj < 180 and self.angle_B < self.angle_proj1 and self.angle_A < self.angle_proj1 and ecart_AB < 180:
                self.clip = False
            if self.ecart_proj < 180 and self.angle_B > self.angle_proj2 and self.angle_A > self.angle_proj2 and ecart_AB < 180:
                self.clip = False
            if self.ecart_proj < 180 and self.angle_B < self.angle_proj1 and self.angle_A > self.angle_proj2 and ecart_AB > 180:
                self.clip = False
            if self.ecart_proj > 180 and self.angle_B > self.angle_proj2 and self.angle_A > self.angle_proj2 and ecart_AB < 180\
                and self.angle_B < self.angle_proj1:
                self.clip = False
            if self.ecart_proj < 180 and self.angle_inter1 > self.angle_proj2 \
                and self.angle_inter2 > self.angle_proj2:
                self.clip = False
            if self.ecart_proj < 180  and self.angle_inter1 < self.angle_proj1 \
                and self.angle_inter2 < self.angle_proj1:
                self.clip = False
            if self.angle_A == self.angle_B and self.angle_A == self.angle_S:
                self.clip = False
            diff = vabs(self.angle_inter2 - self.angle_inter1)
            self.ecart = vabs(self.angle_inter2 - self.angle_inter1)
            if self.ecart >= 180:
                diff = vabs(360 - self.angle_inter1 + self.angle_inter2)
            
            if self.clip:
                self.cnv.create_arc(self.S[0]-self.rayon, self.S[1]-self.rayon,
                                    self.S[0]+self.rayon, self.S[1]+self.rayon,
                                    fill="white", tag="clip1", start=self.angle_inter1,
                                    extent=diff,
                                    outline="")
            self.cnv.delete("point")
            self.cnv.create_text(self.A[0]-5, self.A[1]-5, text="A", tag="point")
            self.cnv.create_text(self.B[0]-5, self.B[1]-5, text="B", tag="point")
            self.cnv.create_text(self.inter1[0]-5, self.inter1[1]-5, text="inter1", tag="point")
            self.cnv.create_text(self.inter2[0]-5, self.inter2[1]-5, text="inter2", tag="point")
    def clip2(self):
        self.cnv.delete("clip2")
        #On cherche les intersections entre nos différents segments
        inter1p = point_classe(self.inter1[0], self.inter1[1])
        inter2p = point_classe(self.inter2[0], self.inter2[1])
        '''self.cnv.create_oval(self.inter1[0]-2, self.inter1[1]-2, self.inter1[0]+2, self.inter1[1]+2, fill="cyan", tag="clip2")
        self.cnv.create_oval(self.inter2[0]-2, self.inter2[1]-2, self.inter2[0]+2, self.inter2[1]+2, fill="cyan", tag="clip2")'''
        
        sp = point_classe(self.S[0], self.S[1])
        proj1p = point_classe(self.proj1[0], self.proj1[1])
        proj2p = point_classe(self.proj2[0], self.proj2[1])
        
        seg1 = segment_classe(inter1p, inter2p)
        '''seg1t = seg1.return_tuple()
        self.cnv.create_line(seg1t[0], seg1t[1], tag="clip2", fill="red")'''
        
        seg21 = segment_classe(proj1p, sp)
        '''seg21t = seg21.return_tuple()
        self.cnv.create_line(seg21t[0], seg21t[1], tag="clip2", fill="red")'''
        
        seg22 = segment_classe(proj2p, sp)
        '''seg22t = seg22.return_tuple()
        self.cnv.create_line(seg22t[0], seg22t[1], tag="clip2", fill="red")'''
        
        int1p = intersection_segments(seg1, seg21)
        int2p = intersection_segments(seg1, seg22)
        
        angle_proj1 = -angle_two_points(self.proj1, self.S)
        angle_proj2 = angle_two_points(self.proj2, self.S)
        
        if angle_proj1 < 0:
            angle_proj1 += 360
            
        if angle_proj2 < 0:
            angle_proj2 += 360
        
        if self.angle_inter1 < self.angle_inter2 or self.ecart >= 180:
            self.inter1, self.inter2 = self.inter2, self.inter1
            self.angle_inter1, self.angle_inter2 = self.angle_inter2, self.angle_inter1
        
        if int1p is not None and int1p != "Infinite" and int2p is not None and int2p != "Infinite":
            int1 = int1p.return_tuple()
            int2 = int2p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int1[0], int1[1],
                                    int2[0], int2[1], fill="yellow",
                                    width=0, tag="clip2")
        
        elif int1p is not None and int1p != "Infinite":
            print("Un truc s'affiche")
            int1 = int1p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int1[0], int1[1],
                                    self.inter1[0], self.inter1[1], fill="yellow",
                                    width=0, tag="clip2")    
        elif int2p is not None and int2p != "Infinite":
            print("Un truc s'affiche")
            int2 = int2p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int2[0], int2[1],
                                    self.inter2[0], self.inter2[1], fill="yellow",
                                    width=0, tag="clip2")
        if int2p == "Infinite" or int1p == "Infinite":
            self.cnv.delete("clip1")
    
    def clip2Seg(self):
        self.cnv.delete("clip2")
        if self.clip:
            sp = point_classe(self.S[0], self.S[1])
            proj1p = point_classe(self.proj1[0], self.proj1[1])
            proj2p = point_classe(self.proj2[0], self.proj2[1])
            
            inter1p = point_classe(self.inter1[0], self.inter1[1])
            inter2p = point_classe(self.inter2[0], self.inter2[1])
            
            seg1 = segment_classe(inter1p, inter2p)
            seg21 = segment_classe(proj1p, sp)
            seg22 = segment_classe(proj2p, sp)
            
            int1p = intersection_segments(seg1, seg21)
            int2p = intersection_segments(seg1, seg22)
            
            print("self.ecart: ", self.ecart)
            
            if self.ecart_proj < 180 and self.ecart < 180:
                if self.angle_proj1 > self.angle_inter1:
                    self.angle_inter1 = self.angle_proj1
                    self.inter1 = int1p.return_tuple()
                if self.angle_proj2 < self.angle_inter2:
                    self.angle_inter2 = self.angle_proj2
                    self.inter2 = int2p.return_tuple()
            if self.ecart_proj < 180 and self.ecart >= 180:
                if self.angle_proj1 > self.angle_inter1 and self.angle_inter1 < self.angle_proj2:
                    self.angle_inter1 = self.angle_proj1
                    self.inter1 = int1p.return_tuple()
                if self.angle_proj1 < self.angle_inter1 and self.angle_inter1 > self.angle_proj2:
                    self.angle_inter1 = self.angle_proj1
                    self.inter1 = int1p.return_tuple()
                if self.angle_proj2 < self.angle_inter2 and self.angle_inter2 > self.angle_proj1:
                    self.angle_inter2 = self.angle_proj2
                    self.inter2 = int2p.return_tuple()
                if self.angle_proj2 > self.angle_inter2 and self.angle_inter2 < self.angle_proj1:
                    self.angle_inter2 = self.angle_proj2
                    self.inter2 = int2p.return_tuple()
            if self.ecart_proj > 180 and self.ecart < 180:
                if self.angle_proj2 < self.angle_inter2 and self.angle_inter2 < self.angle_proj1:
                    self.angle_inter2 = self.angle_proj2
                    self.inter2 = int2p.return_tuple()
                if self.angle_proj1 > self.angle_inter1 and self.angle_inter1 > self.angle_proj2:
                    self.angle_inter1 = self.angle_proj1
                    self.inter1 = int1p.return_tuple()
            if self.ecart_proj > 180 and self.ecart > 180:
                if self.angle_proj1 > self.angle_inter1 and self.angle_inter1 > self.angle_proj2:
                    self.angle_inter1 = self.angle_proj1
                    self.inter1 = int1p.return_tuple()
                if self.angle_proj2 < self.angle_inter2 and self.angle_inter2 < self.angle_proj1:
                    self.angle_inter2 = self.angle_proj2
                    self.inter2 = int2p.return_tuple()
            
            self.cnv.create_polygon(self.S[0], self.S[1], self.inter1[0], self.inter1[1],
                                        self.inter2[0], self.inter2[1], fill="yellow",
                                        outline="yellow", tag="clip2")
        '''
        if int1p is not None and int1p != "Infinite" and int2p is not None and int2p != "Infinite":
            int1 = int1p.return_tuple()
            int2 = int2p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int1[0], int1[1],
                                    int2[0], int2[1], fill="yellow",
                                    width=0, tag="clip2")
        
        elif int1p is not None and int1p != "Infinite":
            print("Un truc s'affiche")
            int1 = int1p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int1[0], int1[1],
                                    self.inter1[0], self.inter1[1], fill="yellow",
                                    width=0, tag="clip2")    
        elif int2p is not None and int2p != "Infinite":
            print("Un truc s'affiche")
            int2 = int2p.return_tuple()
            self.cnv.create_polygon(self.S[0], self.S[1], int2[0], int2[1],
                                    self.inter2[0], self.inter2[1], fill="yellow",
                                    width=0, tag="clip2")
        if int2p == "Infinite" or int1p == "Infinite":
            self.cnv.delete("clip1")'''
        
Application()