# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 18:35:09 2021

@author: Utilisateur
"""

import tkinter as tk

def det2(mat2): #determinant d'une matrice 2*2
    return mat2[0][0]*mat2[1][1] - mat2[1][0]*mat2[0][1]

def det3(mat3):#determinant d'une matrice 3*3
    d1 = mat3[0][0]*mat3[1][1]*mat3[2][2]
    d2 = mat3[0][1]*mat3[1][2]*mat3[2][0]
    d3 = mat3[0][2]*mat3[1][0]*mat3[2][1]
    
    f1 = mat3[0][2]*mat3[1][1]*mat3[2][0]
    f2 = mat3[0][1]*mat3[1][0]*mat3[2][2]
    f3 = mat3[0][0]*mat3[1][2]*mat3[2][1]
    return d1 + d2 + d3 - f1 - f2 - f3

def mat3_points(p1, p2, p3):
    mat = [[0]*3 for i in range(3)]
    p = p1 + p2 + p3
    print(p)
    for i in range(3):
        mat[i][0] = p[i*2]
        mat[i][1] = p[i*2+1]
        mat[i][2] = 1
    print(mat)

def abs(val):
    if val < 0:
        return -val
    return val

def p_in_seg(p, A, B):
    if dist(p, A) + dist(p, B) == dist(A, B):
        return True
    return False

def dist(A, B):
    return ((A[0]-B[0])**2 + (A[1]-B[1])**2)**0.5

class Application():

    def __init__(self, width, height):
        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=width, height=height, bg="white")
        self.cnv.pack()

        self.width = width
        self.height = height

        self.points_coords = list()
        self.points_graph = list()

        self.cnv.bind('<Button-1>', self.add_point)
        self.cnv.bind('<Button-3>', self.guardian)
        self.cnv.bind('<Button-2>', self.point_test)
        tk.Button(self.wnd, command=self.delete_points, text="Supprimer les points").pack()
        tk.Button(self.wnd, command=self.polygon, text="Afficher le polygone").pack()
        tk.Button(self.wnd, command=self.delete_all, text="Tout supprimer").pack()
        tk.Button(self.wnd, command=self.delete_polygon, text="Supprimer le polygone").pack()
        tk.Button(self.wnd, command=self.aire_polygon, text="Aire polygone").pack()

        self.wnd.mainloop()

    def add_point(self, event):
        self.points_coords.append((event.x, event.y))
        self.points_graph.append(self.cnv.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="blue", tag="point"))
        
    def delete_points(self):
        self.points_coords = list()
        self.points_graph = list()
        self.cnv.delete("point")
        print(self.points_coords, self.points_graph)

    def polygon(self):
        self.cnv.create_polygon(self.points_coords, tag="polygon", fill="white", outline="blue")
        self.cnv.delete("point")

    def delete_all(self):
        self.delete_points()
        self.delete_polygon()

    def delete_polygon(self):
        self.cnv.delete("polygon")

    def guardian(self, event):
        self.cnv.delete("guardian")
        self.guardian_coords = (event.x, event.y)
        self.cnv.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill="red", tag="guardian")

    def point_test(self, event):
        Cx, Dx = 0, self.width
        Cy, Dy = event.y
        liste_intersections = list()
        for i in range(len(self.points_coords)):
            Ax = self.points_coords[i][0]
            Ay = self.points_coords[i][1]
            if i+1 == len(self.points_coords):
                Bx = self.points_coords[0][0]
                By = self.points_coords[0][1]
            else:
                Bx = self.points_coords[i+1][0]
                By = self.points_coords[i+1][1]
            #det
    
    def aire_polygon(self):
        sommeX_Y1 = 0
        sommeY_X1 = 0
        for i in range(len(self.points_coords)):
            if i+1 == len(self.points_coords):
                sommeX_Y1 += self.points_coords[i][0] * self.points_coords[0][1]
                sommeY_X1 += self.points_coords[i][1] * self.points_coords[0][0]
            else:
                sommeX_Y1 += self.points_coords[i][0] * self.points_coords[i+1][1]
                sommeY_X1 += self.points_coords[i][1] * self.points_coords[i+1][0]
        print(abs(0.5*(sommeX_Y1-sommeY_X1)))
            
mat3_points([1,1],[2,2],[3,3])

Application(600,400)