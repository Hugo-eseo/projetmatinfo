# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:23:28 2021

@author: hugob
"""
import tkinter as tk
import random

import point_in_polygon as pip
import polygon_eclairage as pe
import intersections_rayons_obstacles as iro

from shared import point_classe, segment_classe, intersection_droites,\
    rotation


class Application():
    """Crée la fenêtre de l'application"""
    nbrayons = 60  # Nombre de rayon partants de la source lumineuse
    d = list()
    sommets_polygon = list()
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

    def __init__(self, width, height):
        """Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        """
        # Création de la fenêtre, du canvas et de la frame de commande
        self.width, self.height = width, height
        self.wnd = tk.Tk()
        self.wnd.title("Galerie d'art - Demonstrateur")
        self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
        self.cnv.pack()
        self.frm = tk.Frame(self.wnd, width=self.width, height=100, pady=10,
                            relief='ridge', bd=10)
        self.frm.pack(side=tk.BOTTOM)

        self.frm.columnconfigure(1, minsize=50)
        # Différents modes de demonstration
        tk.Label(self.frm, text="CONFIGURATION DEMONSTRATIONS")\
            .grid(row=0, column=0, columnspan=5, ipadx=10, ipady=10,
                  sticky='new')

        tk.Label(self.frm, text="Modes de démo :")\
            .grid(row=1, column=0, ipadx=10, sticky='n')

        tk.Label(self.frm, text="Options :")\
            .grid(row=1, column=3, ipadx=10, sticky='n')

        tk.Button(self.frm, text="[DEMO 1] Intersection deux droites",
                  command=self.demo1)\
            .grid(row=2, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 2] Rayons et obstacles",
                  command=self.demo2)\
            .grid(row=3, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 3] Dessiner un polygone",
                  command=self.demo3)\
            .grid(row=4, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 4] Lancer de rayons",
                  command=self.demo4)\
            .grid(row=5, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 5] Polygon éclairage",
                  command=self.demo5)\
            .grid(row=6, column=0, ipadx=10, pady=5, sticky='n')

        tk.Label(self.frm, text="Nombre d'obstacles :")\
            .grid(row=3, column=2, ipadx=10, sticky='n')
        self.nb_obstacles = tk.Scale(self.frm, from_=1, to=10,
                                     orient=tk.HORIZONTAL)
        self.nb_obstacles.set(1)
        self.nb_obstacles.grid(row=3, column=3, ipadx=10, sticky='n')

        tk.Button(self.frm, text="Sauvegarder polygon/Modifier preset",
                  command=self.save_polygon)\
            .grid(row=4, column=3, ipadx=10, pady=5, sticky='n')

        self.preset = int()
        a = tk.Radiobutton(self.frm, text='Preset 1', variable=self.preset,
                           value=1)
        a.grid(row=5, column=2, ipadx=10, sticky='n')
        a.select()
        tk.Radiobutton(self.frm, text='Preset 2', variable=self.preset,
                       value=2)\
            .grid(row=5, column=3, ipadx=10, sticky='n')
        tk.Radiobutton(self.frm, text='Preset 3', variable=self.preset,
                       value=3)\
            .grid(row=5, column=4, ipadx=10, sticky='n')

        self.wnd.mainloop()

    def reset(self):
        """Reset du canvas. Suppression de tous les éléments de dessin"""
        self.cnv.delete(tk.ALL)

    # Différents presets
    # Coordonnés des sommets du polygon déjà mémorisés

    def preset1(self):
        """Preset 1"""
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
        self.lancement_preset()

    def preset2(self):
        """Preset 2"""
        self.sommets_polygon = [(164, 302), (107, 388), (187, 371), (336, 472),
                                (427, 371), (508, 446), (737, 472), (820, 371),
                                (757, 105), (729, 328), (638, 261), (615, 116),
                                (468, 49), (334, 54), (374, 201), (269, 254),
                                (118, 115)]
        self.lancement_preset()

    def preset3(self):
        """Preset 3"""
        self.sommets_polygon = [(221, 183), (221, 221), (90, 223), (91, 109),
                                (140, 106), (143, 168), (173, 168), (176, 70),
                                (46, 65), (50, 276), (223, 274), (225, 321),
                                (81, 330), (82, 403), (116, 400), (112, 359),
                                (224, 357), (275, 356), (272, 317), (415, 315),
                                (415, 277), (481, 272), (482, 316), (530, 315),
                                (528, 225), (413, 227), (406, 162), (463, 158),
                                (460, 116), (495, 111), (496, 65), (542, 64),
                                (541, 21), (456, 21), (457, 81), (416, 81),
                                (416, 120), (369, 122), (319, 122), (315, 63),
                                (373, 57), (372, 23), (266, 22), (272, 122),
                                (219, 124)]
        self.lancement_preset()

    def lancement_preset(self, demo=False):
        """Dessin du polygon défini par les preset"""
        size = 4
        demo = True  # Pour controler le paramètre manuellement
        self.d_to_check = []
        self.cnv.delete(tk.ALL)
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        # Mémorisation des segments
        for i in range(len(self.sommets_polygon)):
            A = self.sommets_polygon[i]
            if i > 0:
                B = self.sommets_polygon[i-1]
                self.d_to_check.append([B, A])
            if demo:
                self.cnv.create_oval(A[0]-size, A[1]-size, A[0]+size,
                                     A[1]+size, fill='black')
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append([B, A])
        self.cnv.bind('<Button-1>', self.clic_source_lumière_demo)
        self.reset_button.config(command=self.demo3)

    # Mode de démonstration 5
    def demo5(self):
        pass

    def new_polygone_eclairage(self, event):
        self.cnv.delete('light')
        O = (event.x, event.y)
        polygon_eclairage = pe.polygon_eclairage(O, self.sommets_polygon,
                                                 self.cnv, True)
        self.cnv.create_polygon(polygon_eclairage, fill='yellow', tag='light')
        self.cnv.tag_raise('demo')

    # Mode de démonstration 4
    def demo4(self):
        pass

    # Mode de démonstration 3

    def demo3(self):
        """Lancement de la demo 3 : Dessiner un polygon"""
        self.reset()
        # Liste des sommets du polygon
        self.sommets_polygon = list()
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
        # Si le polygon ne contient pas au moins 3 points
        if len(self.sommets_polygon) < 3:
            return
        # Dessin du polygon
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        # Réhaussement des lettres au premier plan
        self.cnv.tag_raise('lettre')
        if getpartern:
            print(self.sommets_polygon)
        self.cnv.delete('pts')
        self.cnv.unbind('<Button-3>')
        self.cnv.bind('<Button-1>', self.clic_source_lumière_demo)

    def save_polygon(self):
        if len(self.sommets_polygon) < 3:
            return
        fenetre = Save_popup(self.wnd, self.sommets_polygon)

        pass

    def clic_source_lumière_demo(self, event):
        A = (event.x, event.y)
        '''if self.point_in_polygon_demo(A, True):
            # self.intersection_sommets_demo(event)
            self.rayon_obsatcles_demo(event)'''
        if pip.point_in_polygon(A, self.sommets_polygon, self.cnv, True):
            self.new_polygone_eclairage(event)

    # Mode de démonstration 2

    def demo2(self):
        """Lancement de la demo 2 : Rayons contre obstacles"""
        nbobstacle = self.nb_obstacles.get()
        self.reset()

        # Liste des segments à vérifier. L'algorithme cherchera les points
        # d'intersection des droites définies par deux points dans cette liste
        # Au lancement de la demo, seul les 4 coins de la fenêtre sont
        # renseignés
        self.d_to_check = [segment_classe(point_classe(0, 0),
                                          point_classe(self.width, 0)),
                           segment_classe(point_classe(0, 0),
                                          point_classe(0, self.height)),
                           segment_classe(point_classe(self.width, 0),
                                          point_classe(self.width,
                                                       self.height)),
                           segment_classe(point_classe(0, self.height),
                                          point_classe(self.width,
                                                       self.height))]

        self.cnv.bind('<Button-1>', self.rayon_obsatcles_demo)

        # On dessine le nombre obstable demandé
        for i in range(nbobstacle):
            self.draw_obstacle()

    def draw_obstacle(self):
        """Dessine un obsacle rectangulaire quelconque sur le canas"""
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
        A, B, C, D = point_classe(x, y), point_classe(x1, y),\
            point_classe(x1, y1), point_classe(x, y1)
        # Rotation autour du premier point des autres
        B, C, D = rotation(A, B, angle), rotation(A, C, angle),\
            rotation(A, D, angle)
        # Chaque côtés de l'obstacle est un nouveau segment à contrôler
        self.d_to_check.append(segment_classe(A, B))
        self.d_to_check.append(segment_classe(B, C))
        self.d_to_check.append(segment_classe(C, D))
        self.d_to_check.append(segment_classe(D, A))
        # Création du rectangle
        self.cnv.create_polygon(A.return_tuple(), B.return_tuple(),
                                C.return_tuple(), D.return_tuple(),
                                fill='green')

    def rayon_obsatcles_demo(self, event, demo=False):
        """Fonction appellée dans le mode demo2 en cas de clic"""
        point = point_classe(event.x, event.y)
        iro.intersections_rayons_obstacles(self.cnv, point, self.nbrayons,
                                           360, 0, self.d_to_check, demo)

    # Mode de démonstration 1

    def demo1(self):
        """Lancement de la demo 1 : Intersection simple entre deux droites"""
        self.reset()

        # Variables utilisé pour le mode de démonstration 1
        self.state = 1  # Utilisé par la machine à état
        self.nbd = 0
        self.A, self.B = None, None
        self.d = []

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
            self.A = point_classe(event.x, event.y)
            self.state = 2  # En attente du second point

        # State 2 : Deuxième point du segment
        elif self.state == 2:
            self.B = point_classe(event.x, event.y)
            # On trace la droite
            self.cnv.create_line(self.A.x, self.A.y, self.B.x, self.B.y,
                                 fill='black')
            # On attend une nouvelle droite
            self.state = 1
            # Compte le nombre de droite en cours de dessin
            self.nbd += 1
            # On mémorise la droite
            self.d.append(segment_classe(self.A, self.B))

        # Si l'utilisateur a dessiné deux segments
        if self.nbd == 2:
            # On cherche le point d'intersection des deux droites
            I = intersection_droites(self.d[0], self.d[1])
            # On reset la mémoire des deux droites
            self.d = []
            if I is not None:
                # Si un point d'intersection est trouvé on le dessine
                # Condition : le point d'intersection se trouve sur au moins
                # un des deux segments.
                self.cnv.create_oval(I.x-size, I.y-size, I.x+size,
                                     I.y+size, fill='red')
            self.nbd = 0


class Save_popup(tk.Toplevel):
    """Crée une fenêtre popup permettant de sauvegarder le polygon dessiné"""
    width, height = 500, 300
    fichier_config = "config.txt"

    def __init__(self, parent, polygon):
        """Prend en argument la fenêtre parent"""

        super().__init__(parent)
        self.title("Sauvegarder un polygon")
        tk.Label(self, text="Sauvegarder le polygon ci-dessous :")\
            .pack(pady=10)
        self.lift()
        self.minsize(self.width, self.height)

        self.polygon = polygon

        # On récupère le point le plus proche de x=0 et le point le plus
        # proche de y = 0
        min_x, max_x = min(polygon)[0], max(polygon)[0]
        min_y, max_y = min(polygon, key=lambda t: t[1])[1],\
            max(polygon, key=lambda t: t[1])[1]

        # On translate le polygon dans le coin supérieur gauche et
        # redimensionne le polygon par 0.5
        polygonr = list()
        for i in range(len(polygon)):
            polygonr.append(((polygon[i][0]-min_x)*0.5,
                            (polygon[i][1]-min_y)*0.5))

        # On affiche le polygon réduit dans un canvas
        self.cnv = tk.Canvas(self, width=(max_x-min_x)*0.5,
                             height=(max_y-min_y)*0.5)
        self.cnv.pack()
        self.cnv.create_polygon(polygonr, fill='grey')

        self.frm = tk.Frame(self, width=self.width, height=100, pady=10,
                            relief='ridge', bd=10)
        self.frm.pack(side=tk.BOTTOM)

        tk.Label(self.frm, text="Options d'enregistrement :")\
            .grid(row=0, column=0, columnspan=3, ipadx=10, ipady=5,
                  sticky='new')

        tk.Button(self.frm, text="Enregistrer le polygon sous",
                  command=self.save_as)\
            .grid(row=1, column=1, ipadx=10, sticky='n', ipady=5)

        self.reponse_b1 = tk.Label(self.frm, text="")
        self.reponse_b1.grid(row=2, column=1, ipadx=10, sticky='n', ipady=5)

        tk.Label(self.frm, text="Modifier le polygon d'un preset :")\
            .grid(row=3, column=1, ipadx=10, sticky='n', ipady=5)

        self.preset = tk.IntVar()
        a = tk.Radiobutton(self.frm, text='Preset 1', variable=self.preset,
                           value=1)
        a.grid(row=4, column=0, ipadx=10, sticky='n', ipady=5)
        a.select()
        tk.Radiobutton(self.frm, text='Preset 2', variable=self.preset,
                       value=2)\
            .grid(row=4, column=1, ipadx=10, sticky='n', ipady=5)
        tk.Radiobutton(self.frm, text='Preset 3', variable=self.preset,
                       value=3)\
            .grid(row=4, column=2, ipadx=10, sticky='n', ipady=5)
        tk.Button(self.frm, text="Modifier le preset", command=self.edit)\
            .grid(row=5, column=1, ipadx=10, sticky='n', ipady=5)

        self.reponse_b2 = tk.Label(self.frm, text="")
        self.reponse_b2.grid(row=6, column=1, ipadx=10, sticky='n', ipady=5)

    def save_as(self):
        LST_Types = [("Fichier texte", ".txt"), ("Autres types", ".*")]
        emplacement_fichier = tk.\
            filedialog.asksaveasfilename(title="Enregistrer sous",
                                         filetypes=LST_Types,
                                         defaultextension=".txt")
        if emplacement_fichier:
            with open(emplacement_fichier, 'w') as f:
                f.write(str(self.polygon))
            self.reponse_b1.config(text="Fichier correctement enregistré",
                                   fg='green')
        else:
            self.reponse_b1.config(text="Aucun fichier enregistré",
                                   fg='red')
        self.lift()

    def edit(self):
        LST_Types = [("Fichier texte", ".txt"), ("Autres types", ".*")]
        emplacement_fichier = tk.\
            filedialog.askopenfilename(title="Ouvrir",
                                       filetypes=LST_Types,
                                       defaultextension=".txt")
        if emplacement_fichier:
            try:
                lignes_fichier = list()
                with open(self.fichier_config, 'r') as f:
                    for line in f:
                        lignes_fichier.append(line)
                string = "Preset" + str(self.preset.get()) + (":") +\
                    emplacement_fichier + "\n"
                lignes_fichier[self.preset.get()-1] = string
                with open(self.fichier_config, 'w') as f:
                    for line in lignes_fichier:
                        f.write(line)

            except FileNotFoundError:
                print(self.preset)
                with open(self.fichier_config, 'w') as f:
                    for i in range(1, 4):
                        emplacement = str()
                        if i == self.preset.get():
                            emplacement = emplacement_fichier
                        string = "Preset" + str(i) + (":") + emplacement + "\n"
                        f.write(string)
            self.reponse_b2.config(text="Preset correctement modifié",
                                   fg='green')
        else:
            self.reponse_b2.config(text="Aucun preset modifié",
                                   fg='red')
        self.lift()


Application(1000, 500)
