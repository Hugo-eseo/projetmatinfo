import tkinter as tk
import math
from shared import point_classe, segment_classe
from point_in_polygon import point_in_polygon
from générateur_map import generateur, zone_victoire
import random

class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, identite, taille):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      gardien
            - direction : int representant la rotation du gardien dans le sens
                          trigonometrique
            - angle : angle d'éclairage de la lampe torche
            - puissance : distance d'éclairage de la lampe torche
            - vitesse : int representant la vitesse de deplacement du gardien
            - cnv : objet de type tkinter.Canvas dans lequel le polygone sera 
                    dessiné
            - taille : taille en pixel du point représentant le voleur
            - id : int représentant le numero d'identification du gardien
            - couleur : String contenant le code couleur tkinter
        """
        self.position = Point   # position en pixels
        self.direction = direction # en degrés
        self.angle = angle  # en degrés
        self.puissance = puissance    # puissance de la torche en pixels
        self.vitesse = vitesse  # vitesse de deplacement
        affichage = cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill=couleur, tag=f'Gardien_{id}')

    def avancer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera 
                    deplacé
        """
        rad = self.direction * math.pi / 180
        self.position.move(math.sin(rad-math.pi/2) * self.vitesse,
                           math.cos(rad-math.pi/2) * self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(math.sin(rad-math.pi/2) * -self.vitesse,
                               math.cos(rad-math.pi/2) * -self.vitesse)
        else :
            cnv.move('voleur', math.sin(rad-math.pi/2) * self.vitesse,
                     math.cos(rad-math.pi/2) * self.vitesse)
        
        self.eclaire()

    def reculer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera 
                    deplacé
        """
        rad = self.direction * math.pi / 180
        self.position.move(math.sin(rad-math.pi/2) * -self.vitesse,
                           math.cos(rad-math.pi/2) * -self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(math.sin(rad-math.pi/2) * self.vitesse,
                               math.cos(rad-math.pi/2) * self.vitesse)
        else :
            cnv.move('voleur', math.sin(rad-math.pi/2) * -self.vitesse,
                     math.cos(rad-math.pi/2) * -self.vitesse)
        
        self.eclaire()

    def turn_right(self):
        """
        Permet de faire pivoter le gardien
        """
        self.direction -= 10
        if self.direction <= 0:
            self.direction = 360
        self.eclaire()

    def turn_left(self):
        """
        Permet de faire pivoter le gardien
        """
        self.direction += 10
        if self.direction >= 360:
            self.direction = 0
        self.eclaire()

    def eclaire(self, liste_segments):
        """
        Arguments :
        liste_segments : liste d'objets de type segment
        Retourne :
        liste d'objets de type point representant le polgyone éclairé
        """
        pass

class Voleur:
    def __init__(self, Point, vitesse, cnv, taille):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      voleur
            - vitesse : int representant la vitesse de deplacement du voleur
            - cnv : objet de type tkinter.Canvas dans lequel le polygone sera 
                    dessiné
            - taille : taille en pixel du point représentant le voleur
        """
        self.position = Point   # position en pixels
        #self.direction = direction # en degrés
        self.vitesse = vitesse  # vitesse de deplacement
        self.score = 0
        self.inventaire = list()
        affichage = cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill='blue', tag='voleur')


    def avancer(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, -self.vitesse)
        if not point_in_polygon(self.position.return_tuple(), liste_points):
            self.position.move(0, +self.vitesse)
        else :
            cnv.move('voleur', 0, -self.vitesse)


    def reculer(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, self.vitesse)
        if not point_in_polygon(self.position.return_tuple(),liste_points):
            self.position.move(0, -self.vitesse)
        else :
            cnv.move('voleur', 0, self.vitesse)

    def droite(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(+self.vitesse, 0)
        if not point_in_polygon(self.position.return_tuple(), liste_points):
            self.position.move(-self.vitesse, 0)
        else :
            cnv.move('voleur', +self.vitesse, 0)

    def gauche(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(-self.vitesse, 0)
        if not point_in_polygon(self.position.return_tuple(), liste_points):
            self.position.move(self.vitesse, 0)
        else :
            cnv.move('voleur', -self.vitesse, 0)

    def interagir(self, event, liste_Boutons, liste_tableaux):
        """
        Argument :
            liste_Boutons : liste d'objets de type 'Bouton' placés dans le
                            musée
        """
        self.victoire(event)
        self.voler(event, liste_tableaux)
        for Bouton in liste_Boutons:
            if (self.position.x - Bouton.positon.x) <= 5 and \
               (self.position.y - Bouton.positon.y) <= 5:
                Bouton.switch()
        
    def voler(self, event, liste_tableaux):
        """
        Arguments :
            - Tableau : liste d'objets de type 'Tableau' placés dans le musée
        """
        global nb_tableaux_restants
        liste_a_suppr = list()
        for i in range(nb_tableaux_restants):
            if abs(self.position.x - liste_tableaux[i].localisation.x) \
                <= liste_tableaux[i].taille + 1 and \
               abs(self.position.y - liste_tableaux[i].localisation.y) \
                   <= liste_tableaux[i].taille + 1:
                liste_a_suppr.append(i)
        for i_tableau in liste_a_suppr:
            liste_tableaux[i_tableau].vol()
            self.inventaire.append(liste_tableaux[i_tableau])
            liste_tableaux.pop(i_tableau)
            nb_tableaux_restants -= 1

    def victoire(self, event):
        """
        Teste si le voleur a gagné ou non la partie
        """
        if abs(self.position.x - emplacement_victoire[0]) <= 5 \
            and abs(self.position.y - emplacement_victoire[1] <= 5)\
            and len(self.inventaire) == nb_tableaux:
            print("victoire")

class Bouton:
    def __init__(self, Point, etat, lien, taille, cnv, identifiant):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      bouton
            - etat : booleen représentant l'activation ou non du bouton
                     (True : allumé, False : éteint)
            - lien : objet de la carte pouvant etre activé a l'aide d'un
                     bouton (porte, lumière, ...)
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position = Point
        self.etat = etat
        if self.etat: couleur = "green"
        else: couleur = "red"
        self.lien = lien
        self.cnv = cnv
        affichage = self.cnv.create_rectangle(self.position.x - taille,
                                              self.position.y - taille,
                                              self.position.x + taille, 
                                              self.position.y + taille, 
                                              fill=couleur,
                                              tag=f'Bouton_{identifiant}')
    
    def switch(self):
        """
        Permet d'allumer ou d'éteindre un bouton
        """
        if self.etat:
            self.etat = False
            self.cnv.itemconfigure(f'Bouton_{id}', fill='red')
            self.lien.switch()
        else:
            self.etat = True
            self.cnv.itemconfigure(f'Bouton_{id}', fill='green')
            self.lien.switch()
    
class Tableau:
    def __init__(self, Point, cnv, taille, couleur, identifiant):
        self.localisation = Point
        self.taille = taille
        self.identifiant = identifiant
        cnv.create_rectangle(self.localisation.x - taille,
                                         self.localisation.y - taille,
                                         self.localisation.x + taille, 
                                         self.localisation.y + taille, 
                                         fill=couleur,
                                         tag=f'Tableau_{identifiant}')
    
    def vol(self):
        cnv.delete(f'Tableau_{self.identifiant}')


def creation_points_in_polygon(nb_points, liste_points, cnv):
    liste_points_in_polygon = list()
    for i in range(nb_points):
        x = random.randint(0, width_canvas)
        y = random.randint(0, height_canvas)
        z = 0
        while not point_in_polygon((x, y), liste_points, cnv):
            x = random.randint(0, width_canvas)
            y = random.randint(0, height_canvas)
            print("Tour"+str(z), " x : ", x, " | y : ", y)
            z += 1
        print(x, y)
        liste_points_in_polygon.append(point_classe(x, y))
    return liste_points_in_polygon

# parametres du jeu
width_canvas, height_canvas = 600, 400
width_frame, height_frame = 100, 400

# coordonnées de depart du voleur
x_depart, y_depart = 100, 100

# taille des differentes entités
taille = 3

# vitesse du voleur
vitesse = 5

# nombre de tableaux
nb_tableaux = 5
nb_tableaux_restants = nb_tableaux

# taille des tableaux en pixel
taille_tableaux = 4

# couleur des tableaux (à mettre sous forme de liste plus tard)
couleur_tableaux = "orange"

# création de l'interface graphique
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=width_canvas, height=height_canvas)
cnv.pack(side=tk.LEFT)
frm = tk.Frame(wnd, width=width_frame, height=height_frame)
frm.pack(side=tk.RIGHT)

# génération de la carte et de la zone de victoire
liste_segments, liste_points, emplacement_victoire = generateur(cnv, 0)

#Création des tableaux
liste_points_tableaux = creation_points_in_polygon(nb_tableaux,
                                                    liste_points, cnv)
liste_tableaux = list()
for i in range(len(liste_points_tableaux)):
    liste_tableaux.append(Tableau(liste_points_tableaux[i], cnv,
                                  taille_tableaux, couleur_tableaux, i))

#Création des boutons
liste_boutons = list()

# Création d'une instance de classe Voleur
voleur = Voleur(point_classe(x_depart, y_depart), vitesse, cnv, taille)

# liaison des actions de deplacement avec les flèches directionnelles
wnd.bind("<Up>", lambda event : voleur.avancer(event, liste_segments, cnv))
wnd.bind("<Down>", lambda event : voleur.reculer(event, liste_segments, cnv))
wnd.bind("<Right>", lambda event : voleur.droite(event, liste_segments, cnv))
wnd.bind("<Left>", lambda event : voleur.gauche(event, liste_segments, cnv))
wnd.bind("<e>", lambda event : voleur.interagir(event, liste_boutons,
                                                liste_tableaux))
wnd.bind("<space>", lambda event : voleur.voler(event, liste_tableaux))
wnd.bind("v", voleur.victoire)

wnd.mainloop()
