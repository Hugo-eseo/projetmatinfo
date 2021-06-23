import tkinter as tk
import math
from shared import point_classe, segment_classe
from point_in_polygon import point_in_polygon
from générateur_map import generateur, zone_victoire
import random


class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, taille,
                 identite, app):
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
         self.position = Point# position en pixels
         self.direction = direction # en degrés
         self.angle = angle  # en degrés
         self.puissance = puissance    # puissance de la torche en pixels
         self.vitesse = vitesse  # vitesse de deplacement
         self.identite = identite
         self.app = app
         affichage = self.app.cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill="red", tag=f'Gardien{identite}')

    def reculer(self, event):
        """

        """
        rad = self.direction * math.pi / 180
        self.position.move(round(math.sin(rad-math.pi/2) * self.vitesse),
                           round(math.cos(rad-math.pi/2) * self.vitesse))
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(round(math.sin(rad-math.pi/2) * -self.vitesse),
                               round(math.cos(rad-math.pi/2) * -self.vitesse))
        else :
            self.app.cnv.move(f'Gardien{self.identite}',
                     round(math.sin(rad-math.pi/2) * self.vitesse),
                     round(math.cos(rad-math.pi/2) * self.vitesse))

        self.eclaire()

    def avancer(self, event):
        """

        """
        rad = self.direction * math.pi / 180
        self.position.move(int(math.sin(rad-math.pi/2) * -self.vitesse),
                           int(math.cos(rad-math.pi/2) * -self.vitesse))
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(int(math.sin(rad-math.pi/2) * self.vitesse),
                               int(math.cos(rad-math.pi/2) * self.vitesse))
        else :
            self.app.cnv.move(f'Gardien{self.identite}',
                     int(math.sin(rad-math.pi/2) * -self.vitesse),
                     int(math.cos(rad-math.pi/2) * -self.vitesse))
        
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

class Voleur:
    def __init__(self, Point, vitesse, taille, nb_tableaux, app):
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
        self.nb_tableaux_restants = nb_tableaux
        self.app = app
        affichage = self.app.cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill='blue', tag='voleur')

    def avancer(self, event):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, -self.vitesse)
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(0, +self.vitesse)
        else :
            self.app.cnv.move('voleur', 0, -self.vitesse)


    def reculer(self, event):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(0, self.vitesse)
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(0, -self.vitesse)
        else :
            self.app.cnv.move('voleur', 0, self.vitesse)

    def droite(self, event):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(+self.vitesse, 0)
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(-self.vitesse, 0)
        else :
            self.app.cnv.move('voleur', +self.vitesse, 0)

    def gauche(self, event):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera 
                    deplacé
        """
        self.position.move(-self.vitesse, 0)
        if not point_in_polygon(self.position.return_tuple(), self.app.liste_points):
            self.position.move(self.vitesse, 0)
        else :
            self.app.cnv.move('voleur', -self.vitesse, 0)

    def interagir(self, event):
        """
        Argument :
            liste_Boutons : liste d'objets de type 'Bouton' placés dans le
                            musée
        """
        self.victoire(event)
        self.voler(event)
        for Bouton in self.app.liste_Boutons:
            if (self.position.x - Bouton.positon.x) <= 5 and \
               (self.position.y - Bouton.positon.y) <= 5:
                Bouton.switch()
        
    def voler(self, event):
        """
        Arguments :
            - Tableau : liste d'objets de type 'Tableau' placés dans le musée
        """
        liste_a_suppr = list()
        for i in range(self.nb_tableaux_restants):
            if abs(self.position.x - self.app.liste_tableaux[i].localisation.x) \
                <= self.app.liste_tableaux[i].taille + 1 and \
               abs(self.position.y - self.app.liste_tableaux[i].localisation.y) \
                   <= self.app.liste_tableaux[i].taille + 1:
                liste_a_suppr.append(i)
        for i_tableau in liste_a_suppr:
            self.app.liste_tableaux[i_tableau].vol()
            self.inventaire.append(self.app.liste_tableaux[i_tableau])
            self.app.liste_tableaux.pop(i_tableau)
            self.nb_tableaux_restants -= 1

    def victoire(self, event):
        """
        Teste si le voleur a gagné ou non la partie
        """
        if abs(self.position.x - self.app.emplacement_victoire[0]) <= 5 \
            and abs(self.position.y - self.app.emplacement_victoire[1] <= 5)\
            and len(self.inventaire) == self.app.nb_tableaux:
            print("victoire")

class Bouton:
    def __init__(self, Point, lien, taille, cnv, identifiant):
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
        self.cnv = cnv
        cnv.create_rectangle(self.localisation.x - taille,
                                         self.localisation.y - taille,
                                         self.localisation.x + taille, 
                                         self.localisation.y + taille, 
                                         fill=couleur,
                                         tag=f'Tableau_{identifiant}')
    
    def vol(self):
        self.cnv.delete(f'Tableau_{self.identifiant}')

class Application:
    def __init__(self, width, height, nb_tableaux):
        self.width_canvas, self.height_canvas = width, height
        self.width_frame, self.height_frame = 100, height
        self.nb_tableaux = nb_tableaux
        x_depart, y_depart = 100, 100

        # taille des differente
        taille_gardiens, taille_voleur, taille_tableaux = 3, 3, 4
        # couleur des tableaux
        couleur_tableaux = "orange"
        # vitesse du voleur
        vitesse = 5

        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=self.width_canvas, height=self.height_canvas)
        self.cnv.pack(side=tk.LEFT)
        self.frm = tk.Frame(self.wnd, width=self.width_frame, height=self.height_frame)
        self.frm.pack(side=tk.RIGHT)

        self.liste_segments, self.liste_points, self.emplacement_victoire = generateur(self.cnv, 0)

        liste_points_tableaux = self.creation_points_in_polygon(self.nb_tableaux)

        self.liste_tableaux = list()
        for i in range(len(liste_points_tableaux)):
            self.liste_tableaux.append(Tableau(liste_points_tableaux[i], self.cnv,
                                        taille_tableaux, couleur_tableaux, i))


        self.liste_Boutons = list()

        voleur = Voleur(point_classe(x_depart, y_depart), vitesse, taille_voleur, self.nb_tableaux, self)

        # liaison des actions de deplacement avec les flèches directionnelles
        self.wnd.bind("<Up>", lambda event : voleur.avancer(event))
        self.wnd.bind("<Down>", lambda event : voleur.reculer(event))
        self.wnd.bind("<Right>", lambda event : voleur.droite(event))
        self.wnd.bind("<Left>", lambda event : voleur.gauche(event))
        self.wnd.bind("<e>", lambda event : voleur.interagir(event))

        self.wnd.mainloop()

    def creation_points_in_polygon(self, nb_points):
        liste_points_in_polygon = list()
        for i in range(nb_points):
            x = random.randint(0, self.width_canvas)
            y = random.randint(0, self.height_canvas)
            z = 0
            while not point_in_polygon((x, y), self.liste_points, self.cnv):
                x = random.randint(0, self.width_canvas)
                y = random.randint(0, self.height_canvas)
                print("Tour"+str(z), " x : ", x, " | y : ", y)
                z += 1
            print(x, y)
            liste_points_in_polygon.append(point_classe(x, y))
        return liste_points_in_polygon


if __name__ == '__main__':
    Application(600, 400, 1)