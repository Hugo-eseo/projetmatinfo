# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:23:28 2021

@author: hugob
"""
import tkinter as tk

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


def inter2d(A1, A2, B1, B2):
    """Calcul les coordonnées du point d'intersection de 2 droites définies
    par 4 points"""
    a, b = det3pts(B1, B2, A2), det3pts(B2, B1, A1)
    x = (a*A1[0] + b*A2[0])/(a+b)
    y = (a*A1[1] + b*A2[1])/(a+b)
    return [x, y]


class Application():
    '''Crée la fenêtre de l'application'''
    state = 1
    nbd = 0
    d = list()

    def __init__(self, width, height):
        '''Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        '''

        self.width, self.height = width, height
        self.wnd = tk.Tk()
        self.wnd.title("Visualisation intersection 2 droites")
        string = str(self.width) + 'x' + str(self.height)
        self.wnd.geometry(string)
        self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
        self.cnv.pack()
        self.cnv.bind('<Button-1>', self.clic)
        self.wnd.mainloop()

    def clic(self, event):
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
            self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                 I[1]+size, fill='red')
            self.nbd = 0


Application(1500, 1000)
