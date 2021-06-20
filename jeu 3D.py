# -*- coding: utf-8 -*-
# @author : ArthurM 

import tkinter as tk
import math


def dessiner_2D(cnv, carte, taille_mur, etage):
    for i in range(hauteur):
        for j in range(largeur):

            # mur
            if carte[etage][i][j] == 1:
                cnv.create_rectangle(j * taille_mur, i * taille_mur,
                                     (j+1) * taille_mur, (i+1) * taille_mur,
                                     fill="black", outline='grey', tag='2D')
            
            # escalier
            elif carte[etage][i][j] == 2:
                cnv.create_rectangle(j * taille_mur, i * taille_mur,
                                     (j+1) * taille_mur, (i+1) * taille_mur,
                                     fill="brown", outline='grey', tag='2D')

            # porte
            elif carte[etage][i][j] == 3:
                cnv.create_rectangle(j * taille_mur, i * taille_mur,
                                     (j+1) * taille_mur, (i+1) * taille_mur,
                                     fill="grey", outline='grey', tag='2D')
            
            # bouton porte
            elif carte[etage][i][j] == 4:
                cnv.create_rectangle(j * taille_mur, i * taille_mur,
                                     (j+1) * taille_mur, (i+1) * taille_mur,
                                     fill="lightgrey", outline='grey', tag='2D')
            # vide
            else:
                cnv.create_rectangle(j * taille_mur, i * taille_mur,
                                     (j+1) * taille_mur, (i+1) * taille_mur,
                                     fill="white", outline='grey', tag='2D')

def dessine_joueur(cnv):
    global joueur_x, joueur_y, angle_joueur
    cnv.create_line(joueur_x, joueur_y, joueur_x+delta_x(angle_joueur), joueur_y+delta_y(angle_joueur), fill='yellow', tag='joueur', width=3)
    cnv.create_rectangle(joueur_x-5, joueur_y-5, joueur_x+5, joueur_y+5, fill='yellow', tag='joueur')

def delta_x(angle_joueur):
    return math.cos(angle_joueur) * 30

def delta_y(angle_joueur):
    return math.sin(angle_joueur) * 30

def dessiner_rayon_2D(cnv, carte):
    global angle_joueur, distance_max

    width = cnv.winfo_width()
    height = cnv.winfo_height()

    cnv3D.delete('decor')
    angle_rayon = angle_joueur - 35 * (math.pi/180)
    if angle_rayon < 0:
        angle_rayon += 2*math.pi
    elif angle_rayon > 2*math.pi:
        angle_rayon -= 2*math.pi

    for rayon in range(140):
        distance_horizontale = 100000000
        x_horizontal = joueur_x
        y_horizontal = joueur_y
        cpt = 0

        # lines horizontales
        if angle_rayon == math.pi or angle_rayon == 0:
            rayon_x = joueur_x
            rayon_y = joueur_y
            cpt = largeur
        elif angle_rayon > math.pi:
            rayon_y = (joueur_y // taille_mur) * taille_mur - 0.0001 # 0.0001 avoid the Division by 0 Error
            rayon_x = (joueur_y-rayon_y) * (-1/math.tan(angle_rayon)) + joueur_x
            yo = -taille_mur
            xo = -yo * (-1/math.tan(angle_rayon))
        else:
            rayon_y = (joueur_y // taille_mur) * taille_mur + taille_mur 
            rayon_x = (joueur_y-rayon_y) * (-1/math.tan(angle_rayon)) + joueur_x 
            yo = taille_mur
            xo = -yo * (-1/math.tan(angle_rayon))

        while cpt < largeur:
            carte_x = int(rayon_x // taille_mur)
            carte_y = int(rayon_y // taille_mur)
            if carte_x < largeur and carte_y < hauteur and carte_y >= 0 and carte_x >= 0:
                
                # mur
                if carte[etage][carte_y][carte_x] == 1:
                    type_mur = 'mur'
                    x_horizontal = rayon_x
                    y_horizontal = rayon_y
                    distance_horizontale = distance((joueur_x, joueur_y), (x_horizontal, y_horizontal))
                    cpt = largeur
                
                # porte
                elif carte[etage][carte_y][carte_x] == 3:
                    type_mur = 'porte'
                    x_horizontal = rayon_x
                    y_horizontal = rayon_y
                    distance_horizontale = distance((joueur_x, joueur_y), (x_horizontal, y_horizontal))
                    cpt = largeur

                else: 
                    rayon_x += xo
                    rayon_y += yo
                    cpt += 1
            else:
                rayon_x += xo
                rayon_y += yo
                cpt += 1

        # lignes verticales 

        distance_vecticale = 10000000
        x_vectical = joueur_x
        y_vectical = joueur_y
        cpt = 0

        if angle_rayon == math.pi/2 or angle_rayon == 3*math.pi/2:
            rayon_x = joueur_x
            rayon_y = joueur_y
            cpt = hauteur

        elif angle_rayon > math.pi/2 and angle_rayon < 3*math.pi/2:
            rayon_x = (joueur_x // taille_mur) * taille_mur - 0.0001 # 0.0001 avoid the Division by 0 Error
            rayon_y = (joueur_x-rayon_x) * (-math.tan(angle_rayon)) + joueur_y
            xo = -taille_mur
            yo = -xo * (-math.tan(angle_rayon))
        else:
            rayon_x = (joueur_x // taille_mur) * taille_mur + taille_mur 
            rayon_y = (joueur_x-rayon_x) * (-math.tan(angle_rayon)) + joueur_y 
            xo = taille_mur
            yo = -xo * (-math.tan(angle_rayon))

        while cpt < hauteur:
            carte_x = int(rayon_x // taille_mur)
            carte_y = int(rayon_y // taille_mur)
            if carte_x < largeur and carte_y < hauteur and carte_y >= 0 and carte_x >= 0:

                # mur
                if carte[etage][carte_y][carte_x] == 1:
                    type_mur = 'mur'
                    x_vectical = rayon_x
                    y_vectical = rayon_y
                    distance_vecticale = distance((joueur_x, joueur_y), (x_vectical, y_vectical))
                    cpt = hauteur

                # porte
                elif carte[etage][carte_y][carte_x] == 3:
                    type_mur = 'porte'
                    x_vectical = rayon_x
                    y_vectical = rayon_y
                    distance_vecticale = distance((joueur_x, joueur_y), (x_vectical, y_vectical))
                    cpt = hauteur

                else:
                    rayon_x += xo
                    rayon_y += yo
                    cpt += 1
            else:
                rayon_x += xo
                rayon_y += yo
                cpt += 1
    
        if distance_horizontale > distance_vecticale:
            distance_max = distance_vecticale
            cnv.create_line(joueur_x, joueur_y, x_vectical, y_vectical, fill="yellow", width=3, tag='joueur')
        else:
            distance_max = distance_horizontale
            cnv.create_line(joueur_x, joueur_y, x_horizontal, y_horizontal, fill="yellow", width=3, tag='joueur')

        angle_projection = angle_joueur - angle_rayon
        if angle_projection > 2*math.pi:
            angle_projection -= 2*math.pi
        if angle_projection < 0:
            angle_projection += 2*math.pi
        
        # dessin des murs
        distance_max *= math.cos(angle_projection)
        ratio = 50 * height / distance_max 
        if ratio > height:
            ratio = height
        decalage = height // 2  - ratio // 2
        if distance_horizontale > distance_vecticale:
            if type_mur == "porte":
                couleur = "brown"
            else:
                couleur = "grey30"
        else:
            if type_mur == "porte":
                couleur = "brown"
            else:
                couleur = "grey20"
        
        facteur_etrange = 3
        cnv3D.create_line(rayon*facteur_etrange, decalage, rayon*facteur_etrange, ratio+decalage, fill=couleur, width=5, tag='decor')

        angle_rayon += (math.pi/180)/2
        
        if angle_rayon < 0:
            angle_rayon += 2*math.pi
        elif angle_rayon > 2*math.pi:
            angle_rayon -= 2*math.pi

def distance(a, b):
    # a, b tuples of 2
    part1 = b[0] - a[0]
    part2 = b[1] - a[1]
    dist = math.sqrt(part1**2 + part2**2)
    return dist

def move_up(event):
    global joueur_y, joueur_x, angle_joueur, etage
    carte_localisation_avant = (int(joueur_x // taille_mur), int(joueur_y // taille_mur))

    joueur_x -= math.sin(angle_joueur-math.pi/2) * 10
    joueur_y += math.cos(angle_joueur-math.pi/2) * 10
    carte_localisation_apres = (int(joueur_x // taille_mur), int(joueur_y // taille_mur))

    # vide
    if carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 0 :
        cnv.delete('joueur')
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)

    # escalier
    elif carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 2 and carte[etage][carte_localisation_avant[1]][carte_localisation_avant[0]] == 0:
        if etage == 0:
            etage += 1
        else:
            etage = 0
        cnv.delete('all')
        dessiner_2D(cnv, carte, taille_mur, etage)
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)

    # bouton porte
    elif carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 4:
        cnv.delete('all')
        for i in range(hauteur):
            for j in range(largeur):
                if carte[etage][i][j] == 3:
                    carte[etage][i][j] = 0
        dessiner_2D(cnv, carte, taille_mur, etage)
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)

    # mur
    else:
        joueur_x += math.sin(angle_joueur-math.pi/2) * 10
        joueur_y -= math.cos(angle_joueur-math.pi/2) * 10

    
def move_down(event):
    global joueur_x, joueur_y, angle_joueur, etage

    carte_localisation_avant = (int(joueur_x // taille_mur), int(joueur_y // taille_mur))

    joueur_x += math.sin(angle_joueur-math.pi/2) * 10
    joueur_y -= math.cos(angle_joueur-math.pi/2) * 10
    carte_localisation_apres = (int(joueur_x // taille_mur), int(joueur_y // taille_mur))

    # vide
    if carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 0:
        cnv.delete('joueur')
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)
    
    # escalier
    elif carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 2 and carte[etage][carte_localisation_avant[1]][carte_localisation_avant[0]] == 0:
        if etage == 0:
            etage += 1
        else:
            etage = 0
        cnv.delete('all')
        dessiner_2D(cnv, carte, taille_mur, etage)
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)

    # bouton porte
    elif carte[etage][carte_localisation_apres[1]][carte_localisation_apres[0]] == 4:
        cnv.delete('all')
        for i in range(hauteur):
            for j in range(largeur):
                if carte[etage][i][j] == 3:
                    carte[etage][i][j] = 0
        dessiner_2D(cnv, carte, taille_mur, etage)
        dessine_joueur(cnv)
        dessiner_rayon_2D(cnv, carte)

    # mur
    else:
        joueur_x -= math.sin(angle_joueur-math.pi/2) * 10
        joueur_y += math.cos(angle_joueur-math.pi/2) * 10

def turn_left(event):
    global angle_joueur
    cnv.delete('joueur')
    angle_joueur -= 0.2
    dessine_joueur(cnv)
    dessiner_rayon_2D(cnv, carte)
    if angle_joueur < 0:
        angle_joueur = 2*math.pi

def turn_right(event):
    global angle_joueur
    cnv.delete('joueur')
    angle_joueur += 0.2
    dessine_joueur(cnv)
    dessiner_rayon_2D(cnv, carte)
    if angle_joueur > 2*math.pi:
        angle_joueur = 0


carte =       [[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],

               [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]



largeur, hauteur = len(carte[0][0]), len(carte[0])
taille_mur = 512 // max(largeur, hauteur) 
joueur_x, joueur_y = taille_mur*5.5, taille_mur*1.5
etage = 0
angle_joueur = -3.14/2

cnv_size_x = taille_mur * largeur
cnv_size_y = taille_mur * hauteur

wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=cnv_size_x, height=cnv_size_y)
cnv3D = tk.Canvas(wnd, width=cnv_size_x, height=cnv_size_y, bg='burlywood4')
cnv3D.create_rectangle(0, 0, cnv_size_x, cnv_size_y//2, width=0, fill='grey40')
cnv.pack(side=tk.LEFT)
cnv3D.pack(side=tk.RIGHT)

dessiner_2D(cnv, carte, taille_mur, etage)
dessine_joueur(cnv)
dessiner_rayon_2D(cnv, carte)

wnd.bind("<Up>", move_up)
wnd.bind("<Down>", move_down)
wnd.bind("<Right>", turn_right)
wnd.bind("<Left>", turn_left)

wnd.mainloop()
