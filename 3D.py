import tkinter as tk

matrice = [[1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1]]

class Third_dim():
    """Prend en arguments :
    application : la fenetre tkinter
    map : une matrice representant le territoire à passer en 3D
    gardien : la position du gardien """
    def __init__(self, application, map, gardien):
        pass

    def calcul_ratio(self):
        pass

    def affichage(self):
        """Affiche dans le canvas 'Canvas3D' la vision 3D"""
        pass


def polygone_depuis_matrice(matrice, taille_murs, mode_demo=False):
    """  Arguments : 
        - matrice est une liste de listes, toutes de meme taille, representant 
          la carte du musée. Elle est composée d'entier (int), les 0 etants les
          espaces vides et les chiffres les elements de la carte.
        - mode_demo permet l'affichage de parametres supplementaires pour debug

    Elle retourne une liste de polygones avec leur caracteristique sous la forme
    [[x1, y1, x2, y2, x3, y3, ..., 4], [x1, y1, x2, y2, x3, y3, ..., 3], ... ]
    avec par exemple 4 le codage d'une porte et 3 celui d'un bouton.
    En cas d'erreur elle retourne None """

    hauteur = len(matrice)
    largeur = len(matrice[0])
    liste_polygones = []



    # Verification si la matrice est bien formée
    for i in range(hauteur):
        if matrice[i] != largeur:
            if mode_demo:
                print("Erreur : la matrice n'est pas de la bonne forme")
            return None
    
    for i in range(hauteur):
        for j in range(largeur):
            if matrice[i][j] != 0:
                liste_polygones.append()


