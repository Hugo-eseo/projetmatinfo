# -*- coding: utf-8 -*-
"""
Created on Mon May  3 10:20:16 2021

@author: hugof
"""

import tkinter as tk
import math

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

def dist(A, B):
    """Renvoie la distance entre deux points passés en arguments"""
    return(math.sqrt((B[0] - A[0])**2+(B[1] - A[1])**2))

class Application():
    
    def __init__(self):
        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=600, height=400)
        self.cnv.pack()
        
        self.A = (200, 250)
        self.B = (500, 310)
        self.S = (300, 200)
        self.rayon = 150

        self.cnv.create_line(self.A, self.B)
        self.cnv.create_oval(self.S[0]-self.rayon, self.S[1]-self.rayon, self.S[0]+self.rayon, self.S[1]+self.rayon)
        self.cnv.create_oval(self.S[0]-3, self.S[1]-3, self.S[0]+3, self.S[1]+3)
        
        #Calcul de d
        ASB = det3sarrus(mat3(self.A, self.S, self.B))
        AB = dist(self.A, self.B)
        d = vabs(ASB)/AB
        if d < self.rayon:
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
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="green")
            
            #1er point d'intersection
            a = 1 - h - t
            b = h + t
            xAG = (a*self.A[0]+b*self.B[0])
            yAG = (a*self.A[1]+b*self.B[1])
            
            self.cnv.create_oval(xAG-3, yAG-3, xAG+3, yAG+3, fill="red")
            
            print(xAG, yAG)
        else:
            print("La droite ne passe pas par le cercle")

        self.wnd.mainloop()

Application()