import tkinter as tk
from shared import point_classe, segment_classe
from polygone_predefini import polygone_predefini
from polygone_aléatoire import polygone_aleatoire
from training import entrainement
from polygon_eclairage import polygon_eclairage
from point_in_polygon import point_in_polygon_classes
from aire_multi_polygones import aire_multi_polygones
from aire_polygone import aire_polygone


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
        aire_joueur.set(f'Aire joueur : {int(score_joueur)}   ({round(score_joueur/aire_totale * 100, 2)}%)')
        wnd.update()
        if gardien_actuels == nombre_gardien:
            # calculer un positionnement presque optimal 
            if mode_1v1:
                generations_maximum = nombre_gardien * 30
                seuil_maximal = score_joueur/aire_totale * 1.0001
                print(seuil_maximal)
            indiv, _, _, liste_sommets, score_ia = entrainement(nombre_individus,
                                                            nombre_gardien,
                                                            taux_mutation,
                                                            seuil_maximal,
                                                            generations_maximum,
                                                            wnd,
                                                            cnv,
                                                            sommets)
            aire_ia.set(f'Aire IA : {int(score_ia)}   ({round(score_ia/aire_totale * 100, 2)}%)')
            # afficher le resultat
            if type(indiv[0]) is list:
                for gardien in indiv:
                    cnv.create_polygon(polygon_eclairage(gardien, liste_sommets, cnv), fill='yellow')
                for gardien in indiv:
                    cnv.create_oval(gardien[0]-taille_point, gardien[1]-taille_point, gardien[0]+taille_point, gardien[1]+taille_point, fill='red', tag='ia')
            else:
                cnv.create_polygon(polygon_eclairage(indiv, liste_sommets, cnv), fill='yellow')
                cnv.create_oval(indiv[0]-taille_point, indiv[1]-taille_point, indiv[0]+taille_point, indiv[1]+taille_point, fill='red', tag='ia')
            cnv.tag_raise('gardien')


if __name__ == '__main__':
    # parametres d'image
    width, height = 600, 400
    taille_point = 3

    # parametres de jeu
    map_aleatoire = False
    nombre_gardien = 2

    # parametres d'ia
    generations_auto = True
    mode_1v1 = True
    nombre_individus = 25
    taux_mutation = 0.05
    seuil_maximal = 1

    if generations_auto:
        generations_maximum = nombre_gardien * 20
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
    if map_aleatoire is True:
        segments, sommets = polygone_aleatoire(None, cnv)
    else:
        segments, sommets = polygone_predefini(cnv, None)       

    # calcul de l'aire de l'entièreté musée
    aire_totale = aire_polygone(sommets)

    # jouer
    gardien_actuels = 0
    liste_polygones = []
    cnv.bind('<Button-1>', jouer)

    wnd.mainloop()
