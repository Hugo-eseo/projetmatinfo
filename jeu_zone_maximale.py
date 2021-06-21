import tkinter as tk
from shared import point_classe, segment_classe
from polygone_predefini import polygone_predefini
from polygone_aléatoire import polygone_aleatoire
from training import entrainement
from polygon_eclairage import polygon_eclairage
import threading
from point_in_polygon import point_in_polygon_classes
from aire_multi_polygones import aire_multi_polygones


def jouer(event):
    global gardien_actuels, aire, liste_polygones
    if gardien_actuels == nombre_gardien:
        gardien_actuels = 0
        liste_polygones.clear()
        aire = 0
        cnv.delete('gardien')
    gardien = point_classe(event.x, event.y)
    if point_in_polygon_classes(gardien, segments, cnv):
        gardien_actuels += 1
        cnv.create_oval(gardien.x-taille_point, gardien.y-taille_point, gardien.x+taille_point, gardien.y+taille_point, fill='blue', tag='gardien')
        polygone_lumiere = polygon_eclairage(gardien.return_tuple(), sommets, cnv)
        liste_polygones.append(polygone_lumiere)
        score_joueur = aire_multi_polygones(liste_polygones)
        aire_joueur.set(f'Aire joueur : {int(score_joueur)}')
        wnd.update()
        if gardien_actuels == nombre_gardien:
            # calculer un positionnement presque optimal    
            indiv, _, _, liste_sommets, score_ia = entrainement(nombre_individus,
                                                            nombre_gardien,
                                                            taux_mutation,
                                                            seuil_maximal,
                                                            generations_maximum,
                                                            wnd,
                                                            cnv)
            aire_ia.set(f'Aire IA : {int(score_ia)}')
            # afficher le resultat
            if type(indiv[0]) is list:
                for gardien in indiv:
                    cnv.create_polygon(polygon_eclairage(gardien, liste_sommets, cnv), fill='yellow')
                for gardien in indiv:
                    cnv.create_oval(gardien[0]-taille_point, gardien[1]-taille_point, gardien[0]+taille_point, gardien[1]+taille_point, fill='red', tag='gardien')
            else:
                cnv.create_polygon(polygon_eclairage(indiv, liste_sommets, cnv), fill='yellow')
                cnv.create_oval(indiv[0]-taille_point, indiv[1]-taille_point, indiv[0]+taille_point, indiv[1]+taille_point, fill='red', tag='gardien')


if __name__ == '__main__':
    # parametres d'image
    width, height = 600, 400
    taille_point = 3

    # parametre de jeu
    nombre_gardien = 3

    # parametres d'ia
    generations_auto = True
    nombre_individus = 10
    taux_mutation = 0.05
    seuil_maximal = 0.9

    if generations_auto:
        generations_maximum = nombre_gardien * 15
    else:
        generations_maximum = 15

    # créer la fenêtre
    wnd = tk.Tk()
    cnv = tk.Canvas(wnd, width=width, height=height)
    cnv.pack()
    aire_joueur, aire_ia = tk.StringVar(), tk.StringVar()
    aire_joueur.set('Aire joueur : 0')
    aire_ia.set('Aire IA : 0')
    aire_joueur_label = tk.Label(wnd, textvariable=aire_joueur).pack(side=tk.BOTTOM)
    aire_ia_label = tk.Label(wnd, textvariable=aire_ia).pack(side=tk.BOTTOM)

    wnd.update()

    # dessiner le polgyone
    # segments = polygone_aleatoire(None, cnv)
    segments = polygone_predefini(cnv, None)
    f = open("P2/projetmatinfo/sommets_polygone.txt", 'r')
    sommets = eval(f.read())
    f.close()        

    # jouer
    gardien_actuels = 0
    liste_polygones = []
    cnv.bind('<Button-1>', jouer)


    wnd.mainloop()


# points qui ont l'air de bug : [175, 117] | [57, 155] (l'un ou l'autre)