from shared import point_classe, segment_classe 
import random



def generateur(canvas, numero_predefini):
    """
    Arguments :
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera 
                   dessiné
        - numero_preset : integer definissant quel polygone sera dessiné,
                          si il est egal à None la dataset sera selectionée
                          aleatoirement
    Affiche :
        - Un polygone predefini en fonction du numero_predefini
    Retourne :
        - Une liste de tous les segments du polygone
    """

    database = [[(221, 183), (221, 221), (90, 223), (91, 109),
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
                (219, 124)]]

    database_victoire = [(156, 153)]

    if numero_predefini is None:
        numero_predefini = random.randint(0, len(database)-1)

    canvas.delete('all')

    transformed_database = list()
    for elem in database[numero_predefini]:
        transformed_database.append(point_classe(elem[0], elem[1]))

    # memorisation des segments
    liste_segments = list()
    for i in range(1, len(transformed_database)):
        A = transformed_database[i]
        B = transformed_database[i-1]
        liste_segments.append(segment_classe(A, B))
    A = transformed_database[0]
    B = transformed_database[-1]
    liste_segments.append(segment_classe(A, B))

    # dessiner le polygone
    canvas.create_polygon(database[numero_predefini], fill='grey')
    canvas.create_rectangle(database_victoire[numero_predefini][0] - 5,
                            database_victoire[numero_predefini][1] - 5,
                            database_victoire[numero_predefini][0] + 5,
                            database_victoire[numero_predefini][1] + 5,
                            fill="red")

    return (liste_segments, database[numero_predefini],
            database_victoire[numero_predefini])

def zone_victoire(cnv, numero_predefini):
    """
    Arguments :
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera 
                   dessiné
        - numero_preset : integer definissant quel polygone sera dessiné,
                          si il est egal à None la dataset sera selectionée
                          aleatoirement
    Affiche :
        - Un polygone représentant la zone d'arrivée en fonction du numero_predefini
    Retourne :
        - Une liste de tous les segments du polygone
    """
    database = [[(220, 180), (240, 180), (240, 200), (220, 200)]]

    transformed_database = list()
    for elem in database[numero_predefini]:
        transformed_database.append(point_classe(elem[0], elem[1]))

    # mémorisation des segments
    liste_segments = list()
    for i in range(1, len(transformed_database)):
        A = transformed_database[i]
        B = transformed_database[i-1]
        liste_segments.append(segment_classe(A, B))
    A = transformed_database[0]
    B = transformed_database[-1]
    liste_segments.append(segment_classe(A, B))

    # dessiner le polygone
    cnv.create_polygon(database[numero_predefini], fill='green')

    return liste_segments