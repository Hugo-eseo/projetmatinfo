import tkinter as tk
import math
from shared import point_classe, segment_classe
from point_in_polygon import point_in_polygon
from générateur_map import generateur, zone_victoire
import random

class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, taille,
                 identite, app, comportement, amplitude):
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
         self.comportement = comportement
         self.amplitude = amplitude
         self.tick = 0
         affichage = self.app.cnv.create_oval(self.position.x - taille,
                                    self.position.y - taille,
                                    self.position.x + taille, 
                                    self.position.y + taille,
                                    fill="black", tag=f'Gardien{identite}')

    def reculer(self):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera 
                    deplacé
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

    def avancer(self):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera 
                    deplacé
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

    def eclaire(self):
        """
        Arguments :
        liste_segments : liste d'objets de type segment
        Retourne :
        liste d'objets de type point representant le polgyone éclairé
        """
        pass

    def agir(self):
        if self.comportement == "toupie":
            self.toupie()
        elif self.comportement == "ronde":
            self.ronde()

    def toupie(self):
        if self.app.in_game:
            self.turn_left()
            self.app.cnv.after(500, self.toupie)

    def ronde(self):
        if self.app.in_game:
            self.tick += 1
            if self.tick < self.amplitude / self.vitesse:
                self.avancer()
            else:
                self.tick = 0
                self.direction += 180
                if self.direction >= 360:
                    self.direction -= 360
            self.app.cnv.after(500, self.ronde)

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
        if self.app.in_game:
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
        if self.app.in_game:
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
        if self.app.in_game:
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
        if self.app.in_game:
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
        if self.app.in_game:
            self.victoire()
            self.voler()
            self.bouton()

    def bouton(self):
        for Bouton in self.app.liste_boutons:
            if abs(self.position.x - Bouton.position.x) <= 5 and \
               abs(self.position.y - Bouton.position.y) <= 5:
                Bouton.switch()

    def voler(self):
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

    def victoire(self):
        """
        Teste si le voleur a gagné ou non la partie
        """
        if abs(self.position.x - self.app.emplacement_victoire[0]) <= 5 \
            and abs(self.position.y - self.app.emplacement_victoire[1] <= 5)\
            and len(self.inventaire) == self.app.nb_tableaux:
            self.app.in_game = False
            tk.Label(self.app.frm, text="Vous avez gagné",
                     fg="red", font=(None, 16)).pack()
            ############
            # CREER UNE POP-UP ICI
            ############

    def defaite(self):
        self.app.in_game = False
        tk.Label(self.app.frm, text="Vous avez perdu",
                     fg="red", font=(None, 16)).pack()

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
        self.etat = True
        if self.etat: couleur = "green"
        else: couleur = "red"
        self.lien = lien
        self.identifiant = identifiant
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
            self.cnv.itemconfigure(f'Bouton_{self.identifiant}', fill='red')
            self.lien.switch()
        else:
            self.etat = True
            self.cnv.itemconfigure(f'Bouton_{self.identifiant}', fill='green')
            self.lien.switch()

class Lampe:
    def __init__(self, Point, cnv, taille, puissance, couleur, identifiant):
        self.localisation = Point
        self.taille = taille
        self.identifiant = identifiant
        self.cnv = cnv
        self.etat = True
        cnv.create_oval(self.localisation.x - taille,
                             self.localisation.y - taille,
                             self.localisation.x + taille, 
                             self.localisation.y + taille, 
                             fill=couleur,
                             tag=f'Lampe_{identifiant}')

    def switch(self):
        """
        Allume/éteint la lampe
        """
        if self.etat:
            self.etat = False
            self.eteindre()
        else:
            self.etat = True
            self.allume()

    def eteindre(self):
        """
        Éteint la lampe
        """
        self.cnv.itemconfigure(f'Lampe_{self.identifiant}', fill="black")

    def allume(self):
        """
        Allume la lampe
        """
        self.cnv.itemconfigure(f'Lampe_{self.identifiant}', fill="yellow")

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
    def __init__(self, width, height):
        self.width_canvas, self.height_canvas = width, height
        self.width_frame, self.height_frame = 100, height
        angle_gardien, puissance_gardien = 60, 50
        vitesse_gardien = 5
        x_depart, y_depart = 100, 100

        # taille des differente
        taille_gardien, taille_voleur, taille_tableau = 3, 3, 4
        # couleur des tableaux
        couleur_tableau = "orange"
        # vitesse du voleur
        vitesse = 5

        taille_lampe, couleur_lampe = 3, "yellow"
        taille_bouton = 3

        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=self.width_canvas, height=self.height_canvas)
        self.cnv.pack(side=tk.LEFT)
        self.frm = tk.Frame(self.wnd, width=self.width_frame, height=self.height_frame)
        self.frm.pack(side=tk.RIGHT)

        tk.Button(self.frm, text="Rejouer", command=self.rejouer).pack()

        self.liste_segments, self.liste_points, self.emplacement_victoire,\
        self.emplacements_gardiens, self.emplacements_lampes,\
        self.emplacements_boutons,\
        self.emplacements_tableaux = generateur(self.cnv, None)
        self.in_game = True

        self.liste_tableaux = list()
        self.liste_gardiens = list()
        self.liste_boutons = list()
        self.liste_lampes = list()

        self.nb_tableaux = len(self.emplacements_tableaux)
        for i in range(self.nb_tableaux):
            self.liste_tableaux.append(
                Tableau(point_classe(self.emplacements_tableaux[i][0],
                                     self.emplacements_tableaux[i][1]),
                        self.cnv,
                        taille_tableau, couleur_tableau, i))
        
        for i in range(len(self.emplacements_gardiens)):
            self.liste_gardiens.append(
                Gardien(point_classe(self.emplacements_gardiens[i][0],
                                     self.emplacements_gardiens[i][1]),
                        self.emplacements_gardiens[i][2], angle_gardien,
                        puissance_gardien, vitesse_gardien, taille_gardien,
                        i, self, self.emplacements_gardiens[i][3],
                        self.emplacements_gardiens[i][4]))
        
        for i in range(len(self.emplacements_lampes)):
            self.liste_lampes.append(
                Lampe(point_classe(self.emplacements_lampes[i][0],
                                   self.emplacements_lampes[i][1]),
                      self.cnv, taille_lampe, self.emplacements_lampes[i][2],
                      couleur_lampe, i))
            self.liste_boutons.append(
                Bouton(point_classe(self.emplacements_boutons[i][0],
                                    self.emplacements_boutons[i][1]),
                       self.liste_lampes[i], taille_bouton, self.cnv, i))


        voleur = Voleur(point_classe(x_depart, y_depart), vitesse, taille_voleur, self.nb_tableaux, self)

        # liaison des actions de deplacement avec les flèches directionnelles
        self.wnd.bind("<Up>", lambda event : voleur.avancer(event))
        self.wnd.bind("<Down>", lambda event : voleur.reculer(event))
        self.wnd.bind("<Right>", lambda event : voleur.droite(event))
        self.wnd.bind("<Left>", lambda event : voleur.gauche(event))
        self.wnd.bind("<e>", lambda event : voleur.interagir(event))
        self.wnd.bind("<Button-1>", affiche_truc)

        for gardien in self.liste_gardiens:
            gardien.agir()

        self.wnd.mainloop()

    def rejouer(self):
        if not self.in_game:
            self.wnd.destroy()
            self.__init__(self.width_canvas, self.height_canvas)

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

def affiche_truc(event):
    print(event.x, event.y)

if __name__ == '__main__':
    Application(600, 400)