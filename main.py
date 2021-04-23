# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:23:28 2021

@author: hugob
"""
import tkinter as tk
import random
import math

# Partie 1 : fonctions mathématiques


def signe(n):
    """Renvoie le signe d'un nombre passé en argument"""
    if n == 0:
        return 0
    if n > 0:
        return 1
    return -1


def det2(mat):
    """Renvoie le déterminant d'une matrice 2*2 passée en argument"""
    return(mat[0][0]*mat[1][1]-mat[1][0]*mat[0][1])


def det3(mat):
    """Renvoie le déterminant d'une matrice 3*3 passée en argument"""
    a = mat[0][0]*det2([[mat[1][1], mat[1][2]], [mat[2][1], mat[2][2]]])
    b = mat[0][1]*det2([[mat[1][0], mat[1][2]], [mat[2][0], mat[2][2]]])
    c = mat[0][2]*det2([[mat[1][0], mat[1][1]], [mat[2][0], mat[2][1]]])
    return a-b+c


def det3pts(M, N, P):
    """Renvoie le déterimant de 3 points passés en arguments"""
    mat = [[M[0], N[0], P[0]], [M[1], N[1], P[1]], [1, 1, 1]]
    return det3(mat)


def dist(A, B):
    """Renvoie la distance entre deux points passés en arguments"""
    return(math.sqrt((B[0] - A[0])**2+(B[1] - A[1])**2))


def sc(u, v):
    """Renvoie le produit scalaire en dimension 2 entre deux vecteurs u et v
    passés en arguments"""
    return(u[0]*v[0] + u[1]*v[1])


def norme(u):
    """Renvoie la norme d'un vecteur en dimension 2"""
    return(math.sqrt(u[0]**2 + u[1]**2))


def vect(u, v):
    """Renvoie le produit vectoriel de deux vecteurs u et v passés en arguments
    en dimension 2"""
    return(u[0]*v[1]-u[1]*v[0])


def pointapts(A, A1, A2):
    """Renvoie True si le point A appartient au segment [A1;A2]"""
    if det3pts(A, A1, A2) == 0:
        return math.isclose(dist(A, A1) + dist(A, A2), dist(A1, A2), rel_tol=0.01)
    else:
        return False

def inter2d(A1, A2, B1, B2, requireInt=False):
    """Renvoie les coordonnées du point d'intersection de 2 droites définies
    par 2 points chacunes passés en arguments. Le paramètre requireInt
    (True ou False) indique à la fonction si le point d'intersection doit se
    trouver à l'intérieur des deux segments. Désactivé si non renseigné"""
    a, b = det3pts(B1, B2, A2), det3pts(B2, B1, A1)
    if a + b == 0:
        return None
    x = (a*A1[0]+b*A2[0])/(a+b)
    y = (a*A1[1]+b*A2[1])/(a+b)
    I = (x, y)
    if signe(a) != signe(b):
        if (x, y) != A1 and (x, y) != A2 and (x, y) != B1 and (x, y) != B2:
            return None
    if requireInt:
        if not(pointapts(I, A1, A2) and pointapts(I, B1, B2)):
            return None
    return (x, y)

def angle_two_points(point, center):
    # a, b tuples of 2 
    rad = math.atan2(point[1] - center[1], point[0] - center[0])
    deg = rad * 180/math.pi
    return deg

class Application():
    """Crée la fenêtre de l'application"""
    nbrayons = 300  # Nombre de rayon partants de la source lumineuse
    d = list()
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

    def __init__(self, width, height, three_dim=False):
        """Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        """
        # Création de la fenêtre, du canvas et de la frame de commande
        self.width, self.height = width, height
        self.three_dim = three_dim
        self.loc_gardien, self.angle_facing = [], 0
        self.wnd = tk.Tk()
        self.wnd.title("Galerie d'art - Demonstrateur")
        if self.three_dim:
            self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
            self.cnv.pack(side=tk.LEFT)
            self.cnv3d = tk.Canvas(self.wnd, width=self.width, height=self.height, bg='green')
            self.cnv3d.pack(side=tk.RIGHT)
            # Création du ciel
            self.cnv3d.create_rectangle(0, 0, self.width+3, self.height//2, fill='lightblue', width=0)
            self.frm = tk.Frame(self.wnd, width=2*self.width, height=100)
            self.frm.pack(side=tk.BOTTOM)
        else:
            self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
            self.cnv.pack()
            self.frm = tk.Frame(self.wnd, width=2*self.width, height=100)
            self.frm.pack(side=tk.BOTTOM)

        # Différents modes de demonstration
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
        tk.Button(self.frm, text='[PRESET3] Random poly',
                  command=self.polygon_random).pack()
        self.reset_button = tk.Button(self.frm, text='Reset',
                  command=self.reset)
        self.reset_button.pack()
        self.text_var = tk.StringVar()
        self.text_var.set('Aire : 0')
        self.aire_label = tk.Label(self.frm, textvariable=self.text_var).pack()
        self.wnd.mainloop()

    def reset(self):
        """Reset du canvas. Suppression de tous les éléments de dessin. Bug au niveau du reset de l'aire"""
        self.text_var.set('Aire : 0')
        self.cnv.delete(tk.ALL)
        
    # Différents presets
    # Coordonnés des sommets du polygon déjà mémorisés

    def preset1(self):
        """Preset 1"""
        self.sommets_polygon = [(221, 183), (221, 221), (90, 223), (91, 109),
                                (140, 106), (143, 168), (173, 168), (176, 70),
                                (46, 65), (50, 276), (223, 274), (225, 321),
                                (81, 330), (82, 403), (116, 400), (112, 359),
                                (224, 357), (275, 356), (272, 317), (415, 315),
                                (415, 277), (481, 272), (482, 316), (530, 315),
                                (528, 225), (413, 227), (406, 162), (463, 158),
                                (460, 116), (495, 111), (496, 65), (542, 64),
                                (541, 21), (456, 21), (457, 81), (416, 81),
                                (416, 120), (369, 122), (319, 123), (315, 63),
                                (373, 57), (372, 23), (266, 22), (272, 122),
                                (219, 124)]
        self.lancement_preset(mechant=True)

    def preset2(self):
        """Preset 2"""
        self.sommets_polygon = [(164, 302), (107, 388), (187, 371), (336, 472),
                                (427, 371), (508, 446), (737, 472), (820, 371),
                                (757, 105), (729, 328), (638, 261), (615, 116),
                                (468, 49), (334, 54), (374, 201), (269, 254),
                                (118, 115)]
        self.lancement_preset()
    
    def polygon_random(self, full_random=True):
        """ Crée un polygone aléatoire avec un nombre de points defini"""
        liste_points, random_polygon, self.sommets_polygon = [], [], []
        if full_random:
            nb_points = random.randint(3, 50)
        else:
            nb_points = 30
        for i in range(nb_points):
            liste_points.append((random.randint(1, self.width-1), random.randint(1, self.height-1)))
        C = (self.width//2, self.height//2)
        for point in liste_points:
            random_polygon.append(((angle_two_points(point, C)), point))
        random_polygon.sort()
        for elem in random_polygon:
            self.sommets_polygon.append(elem[1])
        self.lancement_preset()
        if not self.point_in_polygon_demo(C):
            self.polygon_random()
        
    def lancement_preset(self, mechant=False):
        """Dessin du polygon défini par les preset"""
        self.d_to_check = []
        self.cnv.delete(tk.ALL)
        couleur = ('')
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        # Mémorisation des segments
        for i in range(len(self.sommets_polygon)):
            if i > 0:
                A = self.sommets_polygon[i]
                B = self.sommets_polygon[i-1]
                if i > 5 and i < 9:
                    self.d_to_check.append([B, A, 'coloré'])
                else:
                    self.d_to_check.append([B, A])
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append([B, A])
        if mechant:
            mechant = (300, 300)
            taille_mechant = 5
            self.cnv.create_rectangle(mechant[0]-taille_mechant, mechant[1]-taille_mechant, mechant[0]+taille_mechant, mechant[1]+taille_mechant, fill='red')
            self.d_to_check.append([(mechant[0]-taille_mechant, mechant[1]-taille_mechant), (mechant[0]-taille_mechant, mechant[1]+taille_mechant), 'mechant'])
            self.d_to_check.append([(mechant[0]-taille_mechant, mechant[1]+taille_mechant), (mechant[0]+taille_mechant, mechant[1]+taille_mechant), 'mechant'])
            self.d_to_check.append([(mechant[0]+taille_mechant, mechant[1]+taille_mechant), (mechant[0]+taille_mechant, mechant[1]-taille_mechant), 'mechant'])
            self.d_to_check.append([(mechant[0]+taille_mechant, mechant[1]-taille_mechant), (mechant[0]-taille_mechant, mechant[1]-taille_mechant), 'mechant'])
        self.cnv.bind('<Button-1>', self.clic_source_lumière_demo)
        self.reset_button.config(command=self.demo3)

    # Mode de démonstration 5

    def polygone_eclairage(self, inter_in_order):
        self.points_coords = []
        self.cnv.delete('lightpolygon')
        for intersection in inter_in_order:
            if intersection[1] == "AHEAD":
                inter_in_order.remove(intersection)
        
        for elem in inter_in_order:
            self.points_coords.append(elem[0])
        self.cnv.create_polygon(self.points_coords, fill='yellow', tag='lightpolygon')
        self.cnv.tag_raise('light')
        self.aire_polygon()
        """
        for i in range(len(inter_in_order)-1):
            self.cnv.create_polygon(self.A, inter_in_order[i][0],
                                    inter_in_order[i+1][0], fill='yellow',
                                    tag='lightpolygon')
            i += 1
        self.cnv.create_polygon(self.A, inter_in_order[-1][0],
                                inter_in_order[0][0], fill='yellow',
                                tag='lightpolygon')
        self.cnv.tag_raise('light')
        """

    # Mode de démonstration 4

    def intersection_sommets_demo(self, event, demo=True):
        """Docstring"""
        # Taille des points d'intersection
        size = 4
        # Suppression de la précédente source lumineuse
        self.cnv.delete('light')
        # Affichage de la source lumineuse en jaune
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='white', tag='light')
        self.liste_inter_def = []
        for sommet in self.sommets_polygon:
            self.A = (event.x, event.y)
            self.B = sommet
            # On cherche toutes les intersections avec les segments renseignés
            inter = []
            count = 0
            for d in self.d_to_check:
                I = inter2d(d[0], d[1], self.A, self.B)
                # Si il y a un point d'intersection
                if I is not None:
                    # On élimine les doublons
                    if inter.count([dist(I, self.A), I]) == 1:
                        continue
                    # On vérifie que ce dernier se trouve dans la direction du
                    # segment [AB]
                    u = (sommet[0] - self.A[0], sommet[1] - self.A[1])
                    v = (I[0] - self.A[0], I[1] - self.A[1])
                    if signe(u[0]) == signe(v[0]) and signe(u[1]) == signe(v[1]):
                        inter.append([dist(I, self.A), I])
            # On cherche le point d'intersection le plus proche du point A
            I_p = min(inter)
            I = I_p[1]
            C = (I[0]+((self.B[0]-self.A[0])/dist(self.A, self.B)),
                 I[1]+((self.B[1]-self.A[1])/dist(self.A, self.B)))
            status, color, I_p = self.find_status(I_p, inter, C)
            I = I_p[1]
            self.liste_inter_def.append([I, status])
            if demo:
                self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size, I[1]+size,
                                    fill=color, tag='light')
                self.cnv.create_line(self.A, I, fill='white', tag='light')

        inter_in_order = []
        for d in self.d_to_check:
            pts_sur_segment = []
            for intersection in self.liste_inter_def:
                I = intersection[0]
                if pointapts(I, d[0], d[1]):
                    pts_sur_segment.append([dist(d[0], I), intersection])
            if not pts_sur_segment:
                continue
            pts_sur_segment.sort()
            for intersection in pts_sur_segment:
                count += 1
                I = intersection[1][0]
                inter_in_order.append(intersection[1])
                self.liste_inter_def.remove(intersection[1])
                if demo:
                    self.cnv.create_text(I[0], I[1]+10, text=count, tag='light')
        self.polygone_eclairage(inter_in_order)

    def find_status(self, I_p, inter, C, selfcall=False, demo=True):
        size = 4
        for sommet in self.sommets_polygon:
            if math.isclose(sommet[0], I_p[1][0], rel_tol=0.01) and\
                math.isclose(sommet[1], I_p[1][1], rel_tol=0.01) and\
                    not self.point_in_polygon_demo(C):
                if not selfcall:
                    return "EQUALS", "green", I_p
                return "BEYOND", "blue", I_p
        if not self.point_in_polygon_demo(C):
            if not selfcall:
                return "AHEAD", "red", I_p
            return "BEYOND", "blue", I_p
        else:
            I = I_p[1]
            self.liste_inter_def.append([I, "EQUALS"])
            if demo:
                self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size, I[1]+size,
                                    fill="green", tag='light')
            inter.remove(I_p)
            I_p = min(inter)
            I = I_p[1]
            C = (I[0]+((self.B[0]-self.A[0])/dist(self.A, self.B)),
                 I[1]+((self.B[1]-self.A[1])/dist(self.A, self.B)))
            return self.find_status(I_p, inter, C, True)

    # Mode de démonstration 3

    def demo3(self):
        """Lancement de la demo 3 : Dessiner un polygon"""
        self.reset_button.config(command=self.demo3)
        # Liste des sommets du polygon
        self.sommets_polygon = []
        # Liste des segments qui serviront pour trouver les intersection
        # (Principe expliqué en commentaire à la demo2)
        self.d_to_check = []
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.dessin_polygone_demo)
        self.cnv.bind('<Button-3>', self.fin_dessin_polygone)

    def dessin_polygone_demo(self, event):
        """Pour chaque clic, on dessine le point correspondant"""
        # Taille des points du polygon
        size = 4
        # A chaque clic, au affiche le point correspondant
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='black', tag='pts')
        # On l'ajoute à la liste des sommets du polygon
        self.sommets_polygon.append((event.x, event.y))
        # Dès que le deuxième point est crée, on enregistre les coordonnées
        # des points de chaque segments du polygon
        if len(self.sommets_polygon) > 1:
            A = self.sommets_polygon[-1]
            B = self.sommets_polygon[-2]
            self.d_to_check.append([B, A])
        # On affiche une lettre à côté du point
        i = (len(self.sommets_polygon)-1)//26
        # On ajoute un ' à chaque tour d'alphabet
        lettre = self.alphabet[(len(self.sommets_polygon) % 26)-1] + i*"'"
        self.cnv.create_text(event.x, event.y-10,
                             text=lettre, tag='lettre')

    def fin_dessin_polygone(self, event, getpartern=False):
        """Dessine le polygon avec les points déssinés par l'utilisateur
        Prend un paramètre facultatif supplémentaire en argument :
        getpatern : si True, affiche dans la console la liste des points
        du polygon"""
        # Si le polygon ne contient aucun point
        if not self.sommets_polygon:
            return
        # Dessin du polygon
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        # Réhaussement des lettres au premier plan
        self.cnv.tag_raise('lettre')
        if getpartern:
            print(self.sommets_polygon)
        # On ajoute à la liste des segments celui formé par le dernier et le
        # premier point
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append([B, A])
        self.cnv.delete('pts')
        self.cnv.unbind('<Button-3>')
        self.cnv.bind('<Button-1>', self.clic_source_lumière_demo)

    def clic_source_lumière_demo(self, event):
        A = (event.x, event.y)
        if self.point_in_polygon_demo(A):
            # self.intersection_sommets_demo(event)
            self.rayon_obsatcles_demo(event)

    def point_in_polygon_demo(self, A, demo=False):
        """ Fonction permettant de vérifier si un point est dans le
        polygon dessiné. Prend un paramètre supplémentaire demo pour
        l'affichage ou non des données de construction"""
        # Cette fonction se base sur l'algorithme présenté sur cet article
        # https://towardsdatascience.com/is-the-point-inside-the-polygon-574b86472119
        # Taille des points d'intersections
        size = 4
        # Winding number
        # Utilisé pour déterminer si un point est dans le polygon ou non
        wn = 0
        demo = False  # Pour controler le paramètre manuellement
        # Si mode de demo: affichage du point sur le clic de l'utilisateur
        if demo:
            self.cnv.delete("demo")
            self.cnv.create_oval(A[0]-size, A[1]-size, A[0]+size,
                                 A[1]+size, fill='green', tag='demo')
            # Compte le nombre d'intersections
            nbI = 0
        O = (0, A[1])
        M = (self.width, A[1])
        if demo:
            # Construction de la droite horizontale à la hauteur du point A
            self.cnv.create_line(O, M, fill='red', tag='demo')
            print("\n\n========================================")
            print("Lancement de l'algorithme de détection")
        # Liste contenant les coordonnées des intersections de la droite
        # horizontale avec les segments du polygon
        interliste = []
        # Pour mémoriser la droite précédente
        e = None
        # Pour chaque point d'intersection, on vérifie si il augmente,
        # diminue, ou n'influence pas le winding number. Le résultat
        # de la précédente intersection est conservé dans cette varibale
        result = 0
        if demo:
            # Compte le nombre de sommets étant point d'intersection
            # pour affichage ultérieur dans la console
            nbsommets = 0
        # On parcours la liste des segments du polygon
        for d in self.d_to_check:
            # On cherche si il y a une intersection avec la droite horizontale
            # On souhaite cette fois-ci que le point d'intersection
            # appartienne aux deux segments, d'où l'argument True (cf fonction)
            I = inter2d(d[0], d[1], O, M, True)
            if demo:
                print("#############################################")
                print("Recherche d'intersections avec le segment", d)
            if I is not None:
                if demo:
                    print("Une intersection trouvée en : ", I)
                # On mémorise chaque intersection
                interliste.append(I)
                # Vecteur directeur de la droite définie par le segment du
                # polygon considéré
                u = (d[1][0] - d[0][0], d[1][1] - d[0][1])
                # Si l'intersection a déjà été enregistrée, c'est qu'il
                # s'agit d'un sommet du polygon
                if interliste.count(I) > 1:
                    if demo:
                        # On le compte
                        nbsommets += 1
                        # On change la couleur du point d'intersection
                        self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                             I[1]+size, fill='blue',
                                             tag='demo')
                        print("Sommet détecté en", I)
                    # On cherche les points D et E, les deux autres points
                    # définissants les deux segments formant le sommet
                    if d[0] == I:
                        D = d[1]
                    else:
                        D = d[0]
                    if e[0] == I:
                        E = e[1]
                    else:
                        E = e[0]
                    # Si ces deux points sont tous les deux au dessus ou
                    # en dessous de I, le sommet doit être ignoré dans le
                    # calcul du winding number
                    if signe(D[1]-I[1]) == signe(E[1]-I[1]):
                        # On retire donc le résultat de la précédente
                        # intersection (correspondant au sommet), chaque sommet
                        # étant détecté deux fois
                        wn -= result
                        if demo:
                            print("Sommet ignoré")
                    # Dans tous les cas (où il s'agit d'un sommet), on passe
                    # au segment suivant
                    continue
                if demo:
                    nbI += 1
                if demo:
                    # On affiche l'intersection
                    self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                         I[1]+size, fill='red', tag='demo')
                # Pour chaque intersection, on met à jour le winding number
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
                # On mémorise le segment précédent
                e = d
                if demo:
                    print("Résultat : ", result)
                    print("Wining number : ", wn)
                    # Affichage du résultat de chaque intersection
                    self.cnv.create_text(I[0], I[1]+10, text=result,
                                         tag='demo')
        if demo:
            print("#############################################")
            print("Nombre total de sommets détécté : ", nbsommets)
            print("Nombre d'intersections : ", nbI)
            print("Wining number final : ", wn)
            print("Liste des intersections : ", interliste)
        # Si le winding number est différent de 0, alors le point se trouve
        # dans le polygon
        if wn != 0:
            return True
        return False

    # Mode de démonstration 2

    def demo2(self):
        """Lancement de la demo 2 : Rayons contre obstacles"""
        nbobstacle = 2
        self.cnv.delete(tk.ALL)
        # Liste des segments à vérifier. L'algorithme cherchera les points
        # d'intersection des droites définies par deux points dans cette liste
        # Au lancement de la demo, seul les 4 coins de la fenêtre sont
        # renseignés
        self.d_to_check = [[(0, 0), (self.width, 0)],
                           [(0, 0), (0, self.height)],
                           [(self.width, 0), (self.width, self.height)],
                           [(0, self.height), (self.width, self.height)]]

        self.cnv.bind('<Button-1>', self.rayon_obsatcles_demo)
        self.cnv.unbind('<Button-3>')
        self.reset_button.config(command=self.demo2)

        # On dessine le nombre obstable demandé
        for i in range(nbobstacle):
            self.draw_obstacle()

    def draw_obstacle(self):
        """Dessine un obsacle rectangulaire quelconque sur le canvas"""
        # Choix aléatoire de la hauteur et largeur de l'obstacle
        width, height = random.randint(10, 60), random.randint(100, 200)
        # Choix aléatoire de ses coordonnées
        maxi = max(width, height)
        x, y = random.randint(maxi, self.width-maxi),\
            random.randint(maxi, self.height-maxi)
        # Choix aléatoire de son angle d'inclinaison
        angle = random.randint(0, 360)
        # Définition des 4 points de l'obstacle
        x1, y1 = x+width, y+height
        A, B, C, D = (x, y), (x1, y), (x1, y1), (x, y1)
        # Rotation autour du premier point des autres
        B, C, D = self.rotation(A, B, angle), self.rotation(A, C, angle),\
            self.rotation(A, D, angle)
        # Chaque côtés de l'obstacle est un nouveau segment à contrôler
        self.d_to_check.append([A, B])
        self.d_to_check.append([B, C])
        self.d_to_check.append([C, D])
        self.d_to_check.append([D, A])
        # Création du rectangle
        self.cnv.create_polygon(A, B, C, D, fill='green')

    def rotation(self, O, M, angle):
        """Renvoie les coordonnées du points M dans la rotation de centre O
        et d'angle 'angle'"""
        # Angle converti en radian
        angle = angle * math.pi / 180
        xM = M[0] - O[0]
        yM = M[1] - O[1]
        x = xM*math.cos(angle) + yM*math.sin(angle) + O[0]
        y = - xM*math.sin(angle) + yM*math.cos(angle) + O[1]
        return (x, y)

    def rayon_obsatcles_demo(self, event, key=False, demo=False):
        """Demo : intersection rayon lumineux contre des obstacles
        Prend un paramètre supplémentaire demo pour l'affichage ou non
        des points d'intersection"""

        self.wnd.bind('<Up>', self.move_up)
        self.wnd.bind('<Down>', self.move_down)
        self.wnd.bind('<Left>', self.turn_left)
        self.wnd.bind('<Right>', self.turn_right)
        
        # Taille des points d'intersection
        size = 4
        # Angle pour la rotation
        angle = 60/self.nbrayons
        angleT = 0
        demo = False  # Pour controler le paramètre manuellement
        # Suppression de la précédente source lumineuse
        self.cnv.delete('light')
        if self.three_dim:
            self.cnv3d.delete('light')
        # La fonction va chercher une intersection avec les segments
        # renseignés dans self.d_to_check et le segment [AB]. Celui-ci
        # de longeur 1 est le départ des rayons de la source
        if self.loc_gardien is None or key is False:
            self.loc_gardien = [event.x, event.y]
        # besoin de faire un changement pour avoir la mesure en degres entre A et le placement de B.
        B = (self.loc_gardien[0]+1, self.loc_gardien[1])
        B = self.rotation(self.loc_gardien, B, self.angle_facing-30)   
        # Pour le nombre de rayon demandés
        for i in range(self.nbrayons):
            # On cherche toutes les intersections avec les segments renseignés
            inter = []
            wall_list = []
            for d in self.d_to_check:
                I = inter2d(d[0], d[1], self.loc_gardien, B)
                # Si il y a un point d'intersection
                if I is not None:
                    # On vérifie que ce dernier se trouve dans la direction du
                    # segment [AB]
                    if dist(I, self.loc_gardien) > dist(I, B):
                        # Si oui on l'ajoute à la liste
                        inter.append([dist(I, self.loc_gardien), I])
                        wall_list.append([dist(I, self.loc_gardien), d])
            # Si aucun point d'intersection n'est trouvé
            if not inter:
                # On trace un segment rouge pour contrôle visuel
                # Utilisé pour debug
                C = (B[0]+(B[0]-self.loc_gardien[0])*50, B[1]+(B[1]-self.loc_gardien[1])*50)
                self.cnv.create_line(self.loc_gardien, C, fill='red', tag='light')
            # Sinon
            else:
                # On cherche le point d'intersection le plus proche du point A
                I_p = min(inter)
                I = I_p[1]
                wall_list.sort()
                wall = wall_list[0][1]

                # Si le mode de demo est activé on dessine ce point
                # d'intersection
                if demo:
                    if inter.count(I_p) > 1:
                        color = 'green'
                        print(inter.count(I_p))
                        self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                             I[1]+size, fill=color,
                                             tag='light')
                    else:
                        color = 'red'
                    # self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                    #                     I[1]+size, fill=color, tag='light')
                # Affichage de la source lumineuse en jaune
                self.cnv.create_oval(self.loc_gardien[0]-size, self.loc_gardien[1]-size, self.loc_gardien[0]+size,
                                     self.loc_gardien[1]+size, fill='yellow', tag='light')
                # Dans tous les cas on dessine le rayon lumineux jusqu'au
                # point d'intersection
                self.cnv.create_line(self.loc_gardien, I, fill='yellow', tag='light')
                if self.three_dim:
                    distanceM = dist(self.loc_gardien, I)
                    self.draw3d(distanceM, angleT, wall)
            # On passe au rayon suivant en effectuant une rotation du point B
            B = self.rotation(self.loc_gardien, B, angle)
            angleT += angle
        
    def draw3d(self, distanceM, angle, wall):
        liste_couleurs = ['RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4']
        couleur1 = random.choice(liste_couleurs[0:2])
        couleur2 = random.choice(liste_couleurs[2:4])
        # Correction de l'effet fisheye
        distanceM *= math.cos((angle-30) * math.pi/180)
        lineH = 30*self.width / distanceM
        if lineH > self.width:
            lineH = self.width
        lineOff = self.height // 2 - lineH // 2
        # Rangement des points du mur
        if wall[0][0] > wall[1][0]:
            wall[0], wall[1] = wall[1], wall[0]
        # Éclairage
        if len(wall) == 3:
            if wall[2] == 'mechant':
                if (wall[1][0] - wall[0][0]) != 0:
                    wall_pente = (wall[1][1] - wall[0][1]) / (wall[1][0] - wall[0][0])
                    if wall_pente < 1 and wall_pente > -1:
                        self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill=couleur2, tag='light')
                    else:
                        self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill=couleur1, tag='light')
                else:
                    self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill=couleur1, tag='light')
            elif wall[2] == 'coloré':
                if (wall[1][0] - wall[0][0]) != 0:
                    wall_pente = (wall[1][1] - wall[0][1]) / (wall[1][0] - wall[0][0])
                    if wall_pente < 1 and wall_pente > -1:
                        self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill='red2', tag='light')
                    else:
                        self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill='red', tag='light')
                else:
                    self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                        lineOff+lineH, width=2, fill='red', tag='light')
        else:
            if (wall[1][0] - wall[0][0]) != 0:
                wall_pente = (wall[1][1] - wall[0][1]) / (wall[1][0] - wall[0][0])
                if wall_pente < 1 and wall_pente > -1:
                    self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                    lineOff+lineH, width=2, fill='grey20', tag='light')
                else:
                    self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                    lineOff+lineH, width=2, fill='grey30', tag='light')
            else:
                self.cnv3d.create_line((self.width-1)-angle*10, lineOff, (self.width-1)-angle*10,
                                    lineOff+lineH, width=2, fill='grey30', tag='light')

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
        self.text_var.set(f'Aire : {int(abs(0.5*(sommeX_Y1-sommeY_X1)))}')
        
    # Mode de démonstration 1

    def demo1(self):
        """Lancement de la demo 1 : Intersection simple entre deux droites"""
        # Variables utilisé pour le mode de démonstration 1
        self.state = 1  # Utilisé par la machine à état
        self.nbd = 0
        self.d = []

        self.reset_button.config(command=self.reset)
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.intersection_deux_droites_demo)
        self.cnv.unbind('<Button-3>')

    def intersection_deux_droites_demo(self, event):
        """Demo : Machine à état pour le dessin des droites"""
        size = 4  # Taille des points dessinés
        # Clic gauche : dessin du point sur le clic
        self.cnv.create_oval(event.x-size, event.y-size, event.x+size,
                             event.y+size, fill='black')
        # State 1 : Premier point du segment
        if self.state == 1:
            self.A = [event.x, event.y]
            self.state = 2  # En attente du second point

        # State 2 : Deuxième point du segment
        elif self.state == 2:
            self.B = [event.x, event.y]
            # On trace la droite
            self.cnv.create_line(self.A[0], self.A[1], self.B[0], self.B[1],
                                 fill='black')
            # On attend une nouvelle droite
            self.state = 1
            # Compte le nombre de droite en cours de dessin
            self.nbd += 1
            # On mémorise la droite
            self.d.append([self.A, self.B])

        # Si l'utilisateur a dessiné deux segments
        if self.nbd == 2:
            # On cherche le point d'intersection des deux droites
            I = inter2d(self.d[0][0], self.d[0][1], self.d[1][0], self.d[1][1])
            # On reset la mémoire des deux droites
            self.d = []
            if I is not None:
                # Si un point d'intersection est trouvé on le dessine
                # Condition : le point d'intersection se trouve sur au moins
                # un des deux segments.
                self.cnv.create_oval(I[0]-size, I[1]-size, I[0]+size,
                                     I[1]+size, fill='red')
            self.nbd = 0

    def move_up(self, event):
        self.loc_gardien[1] -= math.sin(self.angle_facing * math.pi/180) * 5
        self.loc_gardien[0] += math.cos(self.angle_facing * math.pi/180) * 5
        if self.point_in_polygon_demo(self.loc_gardien):
            self.rayon_obsatcles_demo(event, key=True)
        else:
            self.loc_gardien[1] += math.sin(self.angle_facing * math.pi/180) * 5
            self.loc_gardien[0] -= math.cos(self.angle_facing * math.pi/180) * 5
    
    def move_down(self, event):
        self.loc_gardien[1] += math.sin(self.angle_facing * math.pi/180) * 5
        self.loc_gardien[0] -= math.cos(self.angle_facing * math.pi/180) * 5
        if self.point_in_polygon_demo(self.loc_gardien):
            self.rayon_obsatcles_demo(event, key=True)
        else:
            self.loc_gardien[1] -= math.sin(self.angle_facing * math.pi/180) * 5 
            self.loc_gardien[0] += math.cos(self.angle_facing * math.pi/180) * 5
            
    def turn_left(self, event):
        self.angle_facing += 10
        if self.angle_facing == 360:
            self.angle_facing = 0
        self.rayon_obsatcles_demo(event, key=True)
    
    def turn_right(self, event):
        self.angle_facing -= 10
        if self.angle_facing == -360:
            self.angle_facing = 0
        self.rayon_obsatcles_demo(event, key=True)

Application(600, 400, three_dim=True)

'''v = (e[1][0] - e[0][0], e[1][1] - e[0][1])
cosinus = sc(u, v)/(norme(u)*norme(v))
sinus = vect(u, v)/(norme(u)*norme(v))
angle = math.atan2(sinus, cosinus)*180/math.pi
print("Angle entre les deux segments : ", angle)
if angle > 0:  # Si l'angle est aigu'''
