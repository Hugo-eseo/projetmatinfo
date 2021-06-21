import tkinter as tk
from shared import point_classe, segment_classe
from point_in_polygon import point_in_polygon_classes
import math
from générateur_map import generateur, zone_victoire

class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      gardien
            - direction : int representant la rotation du gardien dans le sens trigonometrique
            - angle : angle d'éclairage de la lampe torche
            - puissance : distance d'éclairage de la lampe torche
            - vitesse : int representant la vitesse de deplacement du gardien
            - cnv : objet de type tkinter.Canvas dans lequel le polygone sera 
                    dessiné
            - taille : taille en pixel du point représentant le voleur
        """
        self.position = Point   # position en pixels
        self.direction = direction # en degrés
        self.angle = angle  # en degrés
        self.puissance = puissance    # puissance de la torche en pixels
        self.vitesse = vitesse  # vitesse de deplacement

    def avancer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de tyype segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
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

    def reculer(self, event, liste_segments, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
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

    def turn(self):
        pass

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
        graphique = cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill='blue', tag='voleur')

        """
        tete = cnv.create_line(self.position.x, self.position.y,
                               self.position.x +
                               math.cos(self.direction * math.pi/180)
                               * self.vitesse,
                               self.position.y +
                               math.sin(self.direction*math.pi/180) 
                               * self.vitesse,
                               fill='blue', tag='voleur', width=3)   
        """

    def avancer(self, event, liste_segments, cnv, victoire):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
            - victoire : liste d'objets de type segment repésentant la zone à atteindre
        """
        self.position.move(0, -self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(0, +self.vitesse)
        else :
            cnv.move('voleur', 0, -self.vitesse)
        self.trouver_victoire(victoire, cnv)

    def reculer(self, event, liste_segments, cnv, victoire):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
            - victoire : liste d'objets de type segment repésentant la zone à atteindre
        """
        self.position.move(0, self.vitesse)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(0, -self.vitesse)
        else :
            cnv.move('voleur', 0, self.vitesse)
        self.trouver_victoire(victoire, cnv)

    def droite(self, event, liste_segments, cnv, victoire):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
            - victoire : liste d'objets de type segment repésentant la zone à atteindre
        """
        self.position.move(+self.vitesse, 0)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(-self.vitesse, 0)
        else :
            cnv.move('voleur', +self.vitesse, 0)
        self.trouver_victoire(victoire, cnv)

    def gauche(self, event, liste_segments, cnv, victoire):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
            - victoire : liste d'objets de type segment repésentant la zone à atteindre
        """
        self.position.move(-self.vitesse, 0)
        if not point_in_polygon_classes(self.position, liste_segments, cnv):
            self.position.move(self.vitesse, 0)
        else :
            cnv.move('voleur', -self.vitesse, 0)
        self.trouver_victoire(victoire, cnv)

    def trouver_victoire(self, zone_victoire, cnv):
        """
        Arguments :
            - zone_victoire : liste d'objets de type segment représentant la zone à atteindre
            - cnv : objet de type tkinter.Canvas dans lequel le voleur est dessiné
        """
        if point_in_polygon_classes(self.position, zones_remarquables, cnv):
            self.score += 1


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

# liaison des actions de deplacement avec les flèches directionnelles du clavier
wnd.bind("<Up>", lambda event : voleur.avancer(event, liste_segments, cnv, victoire))
wnd.bind("<Down>", lambda event : voleur.reculer(event, liste_segments, cnv, victoire))
wnd.bind("<Right>", lambda event : voleur.droite(event, liste_segments, cnv, victoire))
wnd.bind("<Left>", lambda event : voleur.gauche(event, liste_segments, cnv, victoire))

wnd.mainloop()
