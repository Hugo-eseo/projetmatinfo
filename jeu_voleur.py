import tkinter as tk
from shared import point_classe, segment_classe
from point_in_polygon import point_in_polygon_classes
import math
from générateur_map import generateur, zone_victoire

class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, id, taille):
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
        self.direction = direction # en degrés
        self.vitesse = vitesse  # vitesse de deplacement
        self.score = 0
        affichage = cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill='blue', tag='voleur')


    def avancer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, -self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(0, +self.vitesse)
        else :
            cnv.move('voleur', 0, -self.vitesse)


    def reculer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(0, -self.vitesse)
        else :
            cnv.move('voleur', 0, self.vitesse)

    def droite(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(+self.vitesse, 0)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(-self.vitesse, 0)
        else :
            cnv.move('voleur', +self.vitesse, 0)

    def gauche(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(-self.vitesse, 0)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(self.vitesse, 0)
        else :
            cnv.move('voleur', -self.vitesse, 0)

    def interagir_boutons(self, event, liste_Boutons):
        """
        Argument :
            liste_Boutons : liste d'objets de type 'Bouton' placés dans le
                            musée
        """
        for Bouton in liste_Boutons:
            if (self.position.x - Bouton.positon.x) <= 5 and \
               (self.position.y - Bouton.positon.y) <= 5:
                Bouton.switch()
        
    def voler(self, event, Tableau):
        """
        Arguments :
            - Tableau : objet de type 'Tableau' placé dans le musée
        """
        if (self.position.x - Tableau.positon.x) <= 5 and \
           (self.position.y - Tableau.positon.y) <= 5:
            Tableau.vol()

class Bouton:
    def __init__(self, Point, etat, lien, taille, cnv, id):
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
                                              fill=couleur, tag=f'Bouton_{id}')
    
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
    def __init__(self, Point, cnv, taille, couleur, id):
        self.localisation = Point
        affichage = cnv.create_rectangle(self.position.x - taille,
                                         self.position.y - taille,
                                         self.position.x + taille, 
                                         self.position.y + taille, 
                                         fill=couleur, tag=f'Tableau_{id}')
    
    def vol(self):
        cnv.delete(f'Tableau_{id}')


# parametres du jeu
width_canvas, height_canvas = 600, 400
width_frame, height_frame = 100, 400

# coordonnées de depart du voleur
x_depart, y_depart = 100, 100

# taille des differentes entités
taille = 3

# vitesse du voleur
vitesse = 5

# création de l'interface graphique
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=width_canvas, height=height_canvas)
cnv.pack(side=tk.LEFT)
frm = tk.Frame(wnd, width=width_frame, height=height_frame)
frm.pack(side=tk.RIGHT)

# génération de la carte et de la zone de victoire
liste_segments = generateur(cnv, 0)
victoire = zone_victoire(cnv, numero_predefini=0)

# Création d'une instance de classe Voleur
voleur = Voleur(point_classe(x_depart, y_depart), vitesse, cnv, taille)

# liaison des actions de deplacement avec les flèches directionnelles
wnd.bind("<Up>", lambda event : voleur.avancer(event, liste_segments, cnv))
wnd.bind("<Down>", lambda event : voleur.reculer(event, liste_segments, cnv))
wnd.bind("<Right>", lambda event : voleur.droite(event, liste_segments, cnv))
wnd.bind("<Left>", lambda event : voleur.gauche(event, liste_segments, cnv))
wnd.bind("Space>", lambda event : voleur.interagir(event, liste_Boutons))

wnd.mainloop()
