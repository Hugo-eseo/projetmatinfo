# -*- coding: utf-8 -*-
# @author : ArthurM 

from shared import point_classe, segment_classe, intersection_segments, dist
from rotation import rotation


def rayon_obstacles_demo(canvas, position_gardien, nombre_rayons, 
                         angle_de_vue, direction_regard, segments_polygone,
                         demo=False):
        """
        Arguments :
            - canvas : objet de type tkinter.Canvas dans lequel le polygone sera 
                       dessiné
            - position_gardien : objet de classe 'point' contenant les coordonnées du gardien
            - nombre_rayons : integer, nombre de rayons projetés
            - angle_de_vue : integer, angle en degrés representant le champ de vision du gardien (fov)
            - direction_regard : integer, en degrés suivant le cercle trigonometrique
            - segments_polygone : liste d'objets de classe 'segment', representant le polygone
            - demo : affiche les points d'intersection pour le debug 
        Affiche :
            - les points d'intersection si demo=True
            - les rayons de lumière
            - le gardien (surement à supprimer dans le futur)
        """
        
        # Taille des points d'intersection
        size = 4

        # Angle pour la rotation
        angle = angle_de_vue/nombre_rayons

        demo = False  # Pour controler le paramètre manuellement
        # Suppression de la précédente source lumineuse
        canvas.delete('light')

        # La fonction va chercher une intersection avec les segments
        # renseignés dans self.d_to_check et le segment [AB]. Celui-ci
        # de longeur 1 est le départ des rayons de la source

        # besoin de faire un changement pour avoir la mesure en degres entre A et le placement de B.
        B = point_classe(position_gardien.x+1, position_gardien.y)
        B = rotation(position_gardien, B, direction_regard-angle_de_vue/2)   

        # Pour le nombre de rayon demandés
        for i in range(nombre_rayons):
            # On cherche toutes les intersections avec les segments renseignés
            inter = []
            wall_list = []
            for segment in segments_polygone:
                rayon_lumiere = segment_classe(position_gardien, B)
                I = intersection_segments(segment, rayon_lumiere)
                # Si il y a un point d'intersection
                if I is not None:
                    # On vérifie que ce dernier se trouve dans la direction du
                    # segment [AB]
                    if dist(I, position_gardien) > dist(I, B):
                        # Si oui on l'ajoute à la liste
                        inter.append([dist(I, position_gardien), I])
            # Si aucun point d'intersection n'est trouvé
            if not inter:
                # On trace un segment rouge pour contrôle visuel
                # Utilisé pour debug
                C = (B.x+(B.x-position_gardien.x)*50, B.y+(B.y-position_gardien.y)*50)
                canvas.create_line(position_gardien.return_tuple, C, fill='red', tag='light')
            # Sinon
            else:
                # On cherche le point d'intersection le plus proche du point A
                I_p = min(inter)
                I = I_p[1]

                # Si le mode de demo est activé on dessine ce point
                # d'intersection
                if demo:
                    if inter.count(I_p) > 1:
                        color = 'green'
                        print(inter.count(I_p))
                        canvas.create_oval(I.x-size, I.y-size, I.x+size,
                                             I.y+size, fill=color,
                                             tag='light')
                    else:
                        color = 'red'
                        canvas.create_oval(I.x-size, I.y-size, I.x+size,
                                             I.y+size, fill=color,
                                             tag='light')

                # Affichage de la source lumineuse en jaune
                canvas.create_oval(position_gardien.x-size, position_gardien.y-size, position_gardien.x+size,
                                     position_gardien.y+size, fill='yellow', tag='light')
                # Dans tous les cas on dessine le rayon lumineux jusqu'au
                # point d'intersection
                canvas.create_line(position_gardien.return_tuple(), I.return_tuple(), fill='yellow', tag='light')
            # On passe au rayon suivant en effectuant une rotation du point B
            B = rotation(position_gardien, B, angle)

