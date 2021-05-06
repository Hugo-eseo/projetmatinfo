# -*- coding: utf-8 -*-
# @author : ArthurM 

from shared import point_classe, angle_deux_points, segment_classe
from point_in_polygon import point_in_polygon


def polygone_aleatoire(nombre_de_points, canvas):
        """
        Arguments : 
            - nombre_de_points : si None, le polygone à un nombre de points aleatoire compris entre 3 et 50
                                 sinon, le polygone à un nombre defini de points 
        Affiche :
            - un polygone connexe avec le nombre de points pris en argument
        Retourne :
            - Une liste d'objets de type 'segment' dans leur ordre d'apparition
        """

        liste_points, random_polygon, sommets_polygon, liste_segments = [], [], [], []
        
        width = canvas.winfo_width()
        height = canvas.info_height()

        cnv.delete('all')

        if nombre_de_points is None:
            nombre_de_points = random.randint(3, 50)
        
        for i in range(nombre_de_points):
            liste_points.append(point_classe(random.randint(1, width-1), random.randint(1, height-1)))
        
        # centre du canvas
        C = point_classe(width//2, height//2)

        for point in liste_points:
            random_polygon.append(((angle_deux_points(point, C)), point))
        
        random_polygon.sort()
        for elem in random_polygon:
            sommets_polygon.append(elem[1])

        # memorisation des segments
        for i in range(1, len(sommets_polygon)):
            A = sommets_polygon[i]
            B = sommets_polygon[i-1]
            liste_segments.append(segment_classe(A, B))
        A = sommets_polygon[0]
        B = sommets_polygon[-1]
        liste_segments.append(segment_classe(A, B))

        if not point_in_polygon_demo(C, liste_segments, canvas):
            polygone_aleatoire(nombre_de_points, canvas)

        # recuperer la matrice de la carte (temporaire)
        image = Image.new("RGB", (600, 400), color=(255,255,255))
        polygone = ImageDraw.Draw(image)
        polygone.polygon(sommets_polygon, fill="black")
        carte = np.asarray(image.convert('L'))
        np.savetxt("P2/projetmatinfo/carte.txt", carte, fmt='%3d')

        # recuperer les sommets du polygone (temporaire)
        f = open('P2/projetmatinfo/sommets_polygone.txt','w')
        f.write(str(sommets_polygon))
        f.close()

        # dessiner le polygone
        canvas.create_polygon(sommets_polygon, fill='grey')

        canvas.bind('<Button-1>', self.clic_source_lumière_demo)
        reset_button.config(command=self.demo3)

        return liste_segments
